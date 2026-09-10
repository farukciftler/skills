// PlatformerAnimationDriver.cs
// Place anywhere under Assets/ (NOT in an Editor folder).
// Feeds the Animator Controller built by PixelCharacterImporter and receives its
// animation events. It does not move the character - your controller does; this
// only reads the Rigidbody2D and your state flags and turns them into animation.
//
// Contract (parameter names must match the importer):
//   floats Speed, VelocityY | bools Grounded, WallSliding, Crouching, Dead | triggers Dash, Attack, Hurt

using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

[DisallowMultipleComponent]
[RequireComponent(typeof(Animator), typeof(SpriteRenderer))]
public class PlatformerAnimationDriver : MonoBehaviour
{
    [Header("Sources")]
    public Rigidbody2D body;
    [Tooltip("Checks ground with a thin box under the collider. Turn off and set Grounded yourself if your controller already knows.")]
    public bool autoGroundCheck = true;
    public LayerMask groundMask = ~0;
    [Tooltip("Airborne time before the Animator is told Grounded=false. Hides 1-frame fall flicker on steps and slopes. Jumps bypass it.")]
    public float ungroundedGrace = 0.06f;

    [Header("Facing")]
    [Tooltip("Art faces right. Flip is done with SpriteRenderer.flipX so the centered pivot stays put.")]
    public bool faceByVelocity = true;
    public float faceThreshold = 0.1f;
    [Tooltip("Optional child holding hitboxes/VFX; its localScale.x is mirrored because flipX does not move children.")]
    public Transform mirroredChildren;

    [Header("Animation events")]
    public UnityEvent onFootstep = new UnityEvent(), onLand = new UnityEvent(), onJumpDust = new UnityEvent(),
        onDashStart = new UnityEvent(), onAttackHit = new UnityEvent(), onAttackEnd = new UnityEvent(),
        onDeathComplete = new UnityEvent();

    public bool Grounded { get; set; }
    public bool WallSliding { get; set; }
    public bool Crouching { get; set; }
    public bool Dead { get; private set; }
    public int Facing { get; private set; } = 1;

    static readonly int SpeedId = Animator.StringToHash("Speed");
    static readonly int VelYId = Animator.StringToHash("VelocityY");
    static readonly int GroundedId = Animator.StringToHash("Grounded");
    static readonly int WallId = Animator.StringToHash("WallSliding");
    static readonly int CrouchId = Animator.StringToHash("Crouching");
    static readonly int DeadId = Animator.StringToHash("Dead");
    static readonly int DashId = Animator.StringToHash("Dash");
    static readonly int AttackId = Animator.StringToHash("Attack");
    static readonly int HurtId = Animator.StringToHash("Hurt");

    Animator anim;
    SpriteRenderer sr;
    Collider2D col;
    float airTime;
    static readonly List<Collider2D> hits = new List<Collider2D>(8);

    void Awake()
    {
        anim = GetComponent<Animator>();
        sr = GetComponent<SpriteRenderer>();
        if (!body) body = GetComponent<Rigidbody2D>();
        col = body ? body.GetComponent<Collider2D>() : GetComponent<Collider2D>();
    }

    void Update()
    {
        Vector2 v = Vector2.zero;
        if (body)
        {
#if UNITY_6000_0_OR_NEWER
            v = body.linearVelocity;
#else
            v = body.velocity;
#endif
        }
        if (autoGroundCheck && col) Grounded = CheckGround();

        airTime = Grounded ? 0f : airTime + Time.deltaTime;
        bool animGrounded = Grounded || (airTime < ungroundedGrace && v.y <= 0.1f);

        anim.SetFloat(SpeedId, Mathf.Abs(v.x));
        anim.SetFloat(VelYId, v.y);
        anim.SetBool(GroundedId, animGrounded);
        anim.SetBool(WallId, WallSliding && !animGrounded);
        anim.SetBool(CrouchId, Crouching && animGrounded);
        anim.SetBool(DeadId, Dead);

        if (faceByVelocity && !Dead && !WallSliding && Mathf.Abs(v.x) > faceThreshold)
            SetFacing(v.x > 0 ? 1 : -1);
    }

    bool CheckGround()
    {
        Bounds b = col.bounds;
        var point = new Vector2(b.center.x, b.min.y - 0.03f);
        var size = new Vector2(b.size.x * 0.9f, 0.04f);
        var filter = new ContactFilter2D { useLayerMask = true, layerMask = groundMask, useTriggers = false };
        int n = Physics2D.OverlapBox(point, size, 0f, filter, hits);
        for (int i = 0; i < n; i++)
            if (hits[i] != col && !hits[i].transform.IsChildOf(transform)) return true;
        return false;
    }

    public void SetFacing(int dir)
    {
        if (dir == 0) return;
        Facing = dir > 0 ? 1 : -1;
        sr.flipX = Facing < 0;
        if (mirroredChildren)
        {
            var s = mirroredChildren.localScale;
            s.x = Mathf.Abs(s.x) * Facing;
            mirroredChildren.localScale = s;
        }
    }

    public void PlayAttack() { if (!Dead) anim.SetTrigger(AttackId); }
    public void PlayDash() { if (!Dead) anim.SetTrigger(DashId); }
    public void PlayHurt() { if (!Dead) anim.SetTrigger(HurtId); }

    public void Die()
    {
        Dead = true;
        anim.ResetTrigger(AttackId);
        anim.ResetTrigger(DashId);
        anim.ResetTrigger(HurtId);
    }

    public void Revive()
    {
        Dead = false;
        anim.Rebind();
        anim.Update(0f);
    }

    // ---- Animation event receivers (names are baked into the clips) ----
    // Every event needs a receiver on this GameObject or Unity logs an error.
    void OnFootstep() => onFootstep?.Invoke();
    void OnLand() => onLand?.Invoke();
    void OnJumpDust() => onJumpDust?.Invoke();
    void OnDashStart() => onDashStart?.Invoke();
    void OnAttackHit() => onAttackHit?.Invoke();
    void OnAttackEnd() => onAttackEnd?.Invoke();
    void OnDeathComplete() => onDeathComplete?.Invoke();
}
