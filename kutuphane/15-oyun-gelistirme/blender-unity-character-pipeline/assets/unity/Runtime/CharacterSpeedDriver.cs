using UnityEngine;

namespace CharacterPipeline
{
    /// <summary>
    /// Feeds the Animator "Speed" parameter (m/s) from actual movement so the
    /// locomotion blend tree (thresholds = real clip speeds from Blender) plays
    /// in sync with the ground — no foot sliding for in-place clips.
    /// For root-motion characters leave this off; the Animator moves the body.
    /// </summary>
    [RequireComponent(typeof(Animator))]
    public class CharacterSpeedDriver : MonoBehaviour
    {
        public float damping = 0.1f;
        static readonly int SpeedId = Animator.StringToHash("Speed");
        Animator _animator;
        Vector3 _lastPos;

        void Awake() { _animator = GetComponent<Animator>(); _lastPos = transform.position; }

        void Update()
        {
            var delta = transform.position - _lastPos;
            delta.y = 0f;
            _lastPos = transform.position;
            float speed = Time.deltaTime > 0f ? delta.magnitude / Time.deltaTime : 0f;
            _animator.SetFloat(SpeedId, speed, damping, Time.deltaTime);
        }
    }
}
