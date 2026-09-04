# reel_params.gd — bridge between batch_render.py and the scene.
#
# batch_render.py exports REEL_SEED, REEL_PARAMS_JSON and REEL_PARAM_<KEY> for
# every recipe parameter. This autoload reads them so a scene can be swept
# without editing scene files — which is the whole point of the sweep workflow.
#
# Install: Project Settings → Globals → Autoload, add this as "Reel".
# Then in any scene:   var links := Reel.get_int("link_count", 24)
#                      var rng := Reel.make_rng()

extends Node

var seed_value: int = 12345
var params: Dictionary = {}


func _ready() -> void:
	var env_seed := OS.get_environment("REEL_SEED")
	if env_seed != "" and env_seed.is_valid_int():
		seed_value = env_seed.to_int()

	var raw := OS.get_environment("REEL_PARAMS_JSON")
	if raw != "":
		var parsed: Variant = JSON.parse_string(raw)
		if parsed is Dictionary:
			params = parsed
		else:
			push_warning("REEL_PARAMS_JSON was not a JSON object; ignoring.")

	# Seeding the global RNG too, so any stray randf() call is also reproducible.
	seed(seed_value)
	print("[reel] seed=%d params=%d" % [seed_value, params.size()])


## A dedicated RNG. Prefer this over global randf() — an explicitly owned
## generator keeps one system's random draws from shifting another's sequence
## when code changes, which is what silently breaks reproducibility.
func make_rng() -> RandomNumberGenerator:
	var rng := RandomNumberGenerator.new()
	rng.seed = seed_value
	return rng


## A separate stream per subsystem (spawner, colour, jitter) so tweaking one
## does not change the others' output for the same seed.
func make_stream(label: String) -> RandomNumberGenerator:
	var rng := RandomNumberGenerator.new()
	rng.seed = hash(str(seed_value) + ":" + label)
	return rng


func has(key: String) -> bool:
	return params.has(key) or OS.get_environment("REEL_PARAM_" + key.to_upper()) != ""


func _raw(key: String) -> String:
	if params.has(key):
		return str(params[key])
	return OS.get_environment("REEL_PARAM_" + key.to_upper())


func get_float(key: String, fallback: float) -> float:
	var v := _raw(key)
	return v.to_float() if v.is_valid_float() else fallback


func get_int(key: String, fallback: int) -> int:
	var v := _raw(key)
	return v.to_int() if v.is_valid_int() else fallback


func get_string(key: String, fallback: String) -> String:
	var v := _raw(key)
	return v if v != "" else fallback


func get_bool(key: String, fallback: bool) -> bool:
	var v := _raw(key).to_lower()
	if v in ["1", "true", "yes"]:
		return true
	if v in ["0", "false", "no"]:
		return false
	return fallback


func get_vec3(prefix: String, fallback: Vector3) -> Vector3:
	return Vector3(
		get_float(prefix + "_x", fallback.x),
		get_float(prefix + "_y", fallback.y),
		get_float(prefix + "_z", fallback.z)
	)
