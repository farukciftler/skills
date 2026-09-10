using System;
using UnityEngine;
using UnityEngine.Events;

namespace CharacterPipeline
{
    /// <summary>
    /// Single receiver for every animation event the Blender pipeline writes.
    /// Clip events call OnAnimEvent("FootstepLeft" | "Hit" | ...). Subscribe from
    /// gameplay code (Fired) or wire the UnityEvent in the Inspector.
    /// </summary>
    [DisallowMultipleComponent]
    public class CharacterAnimEvents : MonoBehaviour
    {
        [Serializable] public class StringEvent : UnityEvent<string> { }

        public StringEvent onEvent = new StringEvent();
        public event Action<string> Fired;

        public void OnAnimEvent(string eventName)
        {
            Fired?.Invoke(eventName);
            onEvent.Invoke(eventName);
        }
    }
}
