// ThirdPersonAnimatorDriver — feeds the uca 3D Animator Controller from a CharacterController.
// Speed = planar m/s (blend-tree thresholds are the authored clip speeds), VelY, Grounded (with coyote grace).
using UnityEngine;
using UnityEngine.Events;

namespace UCA
{
    [DisallowMultipleComponent]
    [RequireComponent(typeof(Animator))]
    public class ThirdPersonAnimatorDriver : MonoBehaviour
    {
        public CharacterController controller;
        [Tooltip("Seconds of air before Grounded turns false (stairs/slopes flicker otherwise)")]
        public float groundedGrace = 0.12f;
        [Tooltip("Damping for the Speed parameter (seconds)")]
        public float speedDamp = 0.1f;
        public UnityEvent onAttackHit = new UnityEvent();
        public UnityEvent onDeathFinished = new UnityEvent();

        static readonly int SpeedId = Animator.StringToHash("Speed");
        static readonly int VelYId = Animator.StringToHash("VelY");
        static readonly int GroundedId = Animator.StringToHash("Grounded");
        static readonly int AttackId = Animator.StringToHash("Attack");
        static readonly int HurtId = Animator.StringToHash("Hurt");
        static readonly int DeadId = Animator.StringToHash("Dead");

        Animator _anim;
        Vector3 _lastPos;
        float _air;

        void Awake()
        {
            _anim = GetComponent<Animator>();
            _anim.applyRootMotion = false;   // clips are in-place; your controller moves the character
            if (controller == null) controller = GetComponent<CharacterController>();
            _lastPos = transform.position;
        }

        void Update()
        {
            float dt = Mathf.Max(Time.deltaTime, 1e-5f);
            Vector3 v = controller != null ? controller.velocity : (transform.position - _lastPos) / dt;
            _lastPos = transform.position;
            bool g = controller == null || controller.isGrounded;
            _air = g ? 0f : _air + dt;
            _anim.SetFloat(SpeedId, new Vector2(v.x, v.z).magnitude, speedDamp, dt);
            _anim.SetFloat(VelYId, v.y);
            _anim.SetBool(GroundedId, _air < groundedGrace);
        }

        public void TriggerAttack() => _anim.SetTrigger(AttackId);
        public void TriggerHurt() => _anim.SetTrigger(HurtId);
        public void SetDead(bool dead) => _anim.SetBool(DeadId, dead);
        public void OnAttackHit() => onAttackHit.Invoke();
        public void OnDeathFinished() => onDeathFinished.Invoke();
    }
}
