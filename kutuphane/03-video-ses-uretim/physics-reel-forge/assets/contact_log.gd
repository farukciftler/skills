# contact_log.gd — record every collision the simulation produces, so audio can
# be synthesised offline from the physics itself.
#
# Install: Project Settings → Globals → Autoload, add as "ContactLog".
# Register bodies:  ContactLog.track(body, "wood", 0.22)
# The log is written when the scene quits, to the path in REEL_EVENTS_PATH
# (default: user://events.json).
#
# WHY NOT get_contact_impulse(): Godot's PhysicsDirectBodyState3D.get_contact_impulse()
# reports a zero vector on the first frame of a contact, which is the only frame
# a bouncy body may have — so the loudest impacts report silence. Reported values
# have also been inconsistent across versions. Instead this derives impact energy
# from the relative normal velocity captured on the tick BEFORE the solver ran,
# which is both reliable and the physically meaningful quantity:
#
#     E = 0.5 * m_eff * v_rel_normal^2,   m_eff = m1*m2/(m1+m2)
#
# That is the kinetic energy actually available to excite vibration, and it is
# what the synthesiser's mode amplitudes scale from.

extends Node

const COOLDOWN_TICKS := 3          # per pair; stops one contact firing repeatedly
const MIN_ENERGY := 0.02           # below this, a settling pile becomes a hiss
const MAX_EVENTS := 20000          # safety valve
const ROLL_MIN_ANGULAR := 4.0      # rad/s before a contact counts as rolling
const ROLL_INTERVAL_TICKS := 12

var _events: Array[Dictionary] = []
var _tracked: Dictionary = {}      # body -> {material, size, prev_vel, prev_ang}
var _cooldown: Dictionary = {}     # pair key -> tick
var _roll_last: Dictionary = {}
var _tick: int = 0
var _tick_rate: float = 60.0
var _frame_span: float = 0.0


func _ready() -> void:
	_tick_rate = float(Engine.physics_ticks_per_second)
	process_priority = -100        # sample velocities before body scripts run


## Register a body so its collisions are logged.
## material must be a key in assets/materials.json; size is the characteristic
## dimension in metres and sets the fundamental frequency.
func track(body: RigidBody3D, material: String, size: float) -> void:
	if body == null or not is_instance_valid(body):
		return
	body.contact_monitor = true
	if body.max_contacts_reported < 4:
		body.max_contacts_reported = 4
	_tracked[body] = {
		"material": material,
		"size": size,
		"prev_vel": body.linear_velocity,
		"prev_ang": body.angular_velocity,
	}
	if not body.body_shape_entered.is_connected(_on_entered):
		body.body_shape_entered.connect(_on_entered.bind(body))


## Static geometry needs a material too, so a wooden cube hitting a metal plate
## can be logged as the louder of the two rather than always as wood.
func set_static_material(node: Node, material: String, size: float = 0.5) -> void:
	node.set_meta("reel_material", material)
	node.set_meta("reel_size", size)


func _physics_process(_delta: float) -> void:
	_tick += 1
	# Snapshot velocities BEFORE this tick's solver changes them. This snapshot is
	# what makes the energy estimate correct — after the solve, the approach
	# velocity is already gone.
	for body in _tracked.keys():
		if not is_instance_valid(body):
			_tracked.erase(body)
			continue
		var rec: Dictionary = _tracked[body]
		rec["prev_vel"] = body.linear_velocity
		rec["prev_ang"] = body.angular_velocity
	_scan_rolling()


func _on_entered(_body_rid: RID, other: Node, _other_shape: int,
		_local_shape: int, body: RigidBody3D) -> void:
	if _events.size() >= MAX_EVENTS:
		return
	if not _tracked.has(body):
		return

	var key := _pair_key(body, other)
	if _cooldown.get(key, -999) > _tick - COOLDOWN_TICKS:
		return
	_cooldown[key] = _tick

	var rec: Dictionary = _tracked[body]
	var v_self: Vector3 = rec["prev_vel"]
	var m_self: float = maxf(body.mass, 0.001)

	var v_other := Vector3.ZERO
	var m_other := INF                       # static bodies are infinitely massive
	if _tracked.has(other):
		v_other = _tracked[other]["prev_vel"]
		m_other = maxf((other as RigidBody3D).mass, 0.001)

	var v_rel := (v_self - v_other).length()
	var m_eff := m_self if is_inf(m_other) else (m_self * m_other) / (m_self + m_other)
	var energy := 0.5 * m_eff * v_rel * v_rel
	if energy < MIN_ENERGY:
		return

	# The harder material dominates what the collision sounds like: a wooden cube
	# landing on a steel plate rings the plate, it does not thud like wood.
	var material: String = rec["material"]
	var size: float = rec["size"]
	if other.has_meta("reel_material"):
		if _hardness(other.get_meta("reel_material")) > _hardness(material):
			material = other.get_meta("reel_material")
			size = other.get_meta("reel_size")
	elif _tracked.has(other):
		var o: Dictionary = _tracked[other]
		if _hardness(o["material"]) > _hardness(material):
			material = o["material"]
			size = o["size"]

	_events.append({
		"t": snappedf(float(_tick) / _tick_rate, 0.0001),
		"energy": snappedf(energy, 0.001),
		"material": material,
		"size": snappedf(size, 0.001),
		"x": snappedf(body.global_position.x, 0.01),
		"kind": "impact",
	})


func _scan_rolling() -> void:
	for body in _tracked.keys():
		if not is_instance_valid(body) or _events.size() >= MAX_EVENTS:
			continue
		var ang: float = (_tracked[body]["prev_ang"] as Vector3).length()
		if ang < ROLL_MIN_ANGULAR:
			continue
		if body.get_contact_count() == 0:
			continue
		if _roll_last.get(body, -999) > _tick - ROLL_INTERVAL_TICKS:
			continue
		_roll_last[body] = _tick
		var rec: Dictionary = _tracked[body]
		_events.append({
			"t": snappedf(float(_tick) / _tick_rate, 0.0001),
			"energy": snappedf(minf(ang / 20.0, 1.5), 0.001),
			"material": rec["material"],
			"size": rec["size"],
			"x": snappedf(body.global_position.x, 0.01),
			"kind": "roll",
			"duration": snappedf(float(ROLL_INTERVAL_TICKS) / _tick_rate, 0.001),
		})


func _pair_key(a: Node, b: Node) -> int:
	var ia := a.get_instance_id()
	var ib := b.get_instance_id()
	return hash(mini(ia, ib) * 31 + maxi(ia, ib))


func _hardness(material: String) -> int:
	match material:
		"metal": return 7
		"porcelain": return 6
		"glass": return 5
		"stone": return 4
		"wood": return 3
		"plastic": return 2
		"cardboard": return 1
		"rubber": return 0
	return 3


## Call before quitting. batch_render.py expects the file to exist afterwards.
func flush() -> void:
	var path := OS.get_environment("REEL_EVENTS_PATH")
	if path == "":
		path = "user://events.json"
	var payload := {
		"sample_rate": 48000,
		"duration": snappedf(float(_tick) / _tick_rate, 0.001),
		"seed": int(OS.get_environment("REEL_SEED")) if OS.get_environment("REEL_SEED") != "" else 0,
		"physics_ticks_per_second": _tick_rate,
		"events": _events,
	}
	var f := FileAccess.open(path, FileAccess.WRITE)
	if f == null:
		push_error("ContactLog: cannot write %s" % path)
		return
	f.store_string(JSON.stringify(payload))
	f.close()
	print("[ContactLog] %d events over %.2fs → %s" %
		[_events.size(), float(_tick) / _tick_rate, path])
	if _events.is_empty():
		push_warning("ContactLog: no events. Check that track() was called and "
			+ "that MIN_ENERGY is not above the impacts in this scene.")


func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_CLOSE_REQUEST or what == NOTIFICATION_PREDELETE:
		flush()
