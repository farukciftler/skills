// PlatformerAnimatorDriver — feeds the uca platformer Animator Controller from a Rigidbody2D.
// Parameters: Speed (|vx|), VelY (vy), Grounded (collider cast), Attack/Hurt (triggers), Dead (bool).
// Your movement script moves the body; this only READS physics and drives animation + facing.
using UnityEngine;
using UnityEngine.Events;

namespace UCA
{
    [DisallowMultipleComponent]
    [RequireComponent(typeof(Animator))]
    public class PlatformerAnimatorDriver : MonoBehaviour
    {
        [Tooltip("Body to read velocity from (defaults to the one on this GameObject)")]
        public Rigidbody2D body;
        [Tooltip("Layers that count as ground")]
        public LayerMask groundLayers = ~0;
        [Tooltip("How far below the collider the ground check reaches (units)")]
        public float groundProbe = 0.06f;
        [Tooltip("Flip the sprite toward the horizontal velocity (art faces RIGHT)")]
        public bool flipWithVelocity = true;
        public float flipDeadZone = 0.05f;
        public UnityEvent onAttackHit = new UnityEvent();
        public UnityEvent onDeathFinished = new UnityEvent();

        static readonly int SpeedId = Animator.StringToHash("Speed");
        static readonly int VelYId = Animator.StringToHash("VelY");
        static readonly int GroundedId = Animator.StringToHash("Grounded");
        static readonly int AttackId = Animator.StringToHash("Attack");
        static readonly int HurtId = Animator.StringToHash("Hurt");
        static readonly int DeadId = Animator.StringToHash("Dead");

        Animator _anim;
        SpriteRenderer _sr;
        Collider2D _col;
        ContactFilter2D _filter;
        readonly RaycastHit2D[] _hits = new RaycastHit2D[4];

        public bool IsGrounded { get; private set; }

        void Awake()
        {
            _anim = GetComponent<Animator>();
            _sr = GetComponent<SpriteRenderer>();
            if (body == null) body = GetComponent<Rigidbody2D>();
            _col = GetComponent<Collider2D>();
            _filter = new ContactFilter2D { useLayerMask = true, layerMask = groundLayers, useTriggers = false };
        }

        void Update()
        {
#if UNITY_6000_0_OR_NEWER
            Vector2 v = body != null ? body.linearVelocity : Vector2.zero;
#else
            Vector2 v = body != null ? body.velocity : Vector2.zero;
#endif
            IsGrounded = _col == null || _col.Cast(Vector2.down, _filter, _hits, groundProbe) > 0;
            _anim.SetFloat(SpeedId, Mathf.Abs(v.x));
            _anim.SetFloat(VelYId, v.y);
            _anim.SetBool(GroundedId, IsGrounded);
            if (flipWithVelocity && _sr != null && Mathf.Abs(v.x) > flipDeadZone) _sr.flipX = v.x < 0f;
        }

        public void TriggerAttack() => _anim.SetTrigger(AttackId);
        public void TriggerHurt() => _anim.SetTrigger(HurtId);
        public void SetDead(bool dead) => _anim.SetBool(DeadId, dead);

        // Animation Event receivers (names written by the sheet generator / importer)
        public void OnAttackHit() => onAttackHit.Invoke();
        public void OnDeathFinished() => onDeathFinished.Invoke();
    }
}
