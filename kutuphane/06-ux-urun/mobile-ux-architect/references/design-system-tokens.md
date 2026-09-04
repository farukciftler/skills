# Mobile Design System Tokens & Form UX

## Token Hierarchy
1. **Primitive Tokens**: `color-blue-500: #0066FF`, `space-16: 16px`, `radius-12: 12px`.
2. **Semantic Tokens**: `color-bg-primary`, `color-text-secondary`, `color-border-error`.
3. **Component Tokens**: `button-primary-bg`, `tabbar-icon-active`.

## Form UX & Keyboard Avoidance
- Automatically scroll active text field above the soft keyboard view (`KeyboardAvoidingView` / `adjustResize`).
- Set appropriate keyboard types (`email-address`, `numeric`, `phone-pad`, `decimal-pad`).
- Enable auto-fill / OTP input attributes (`one-time-code`, `username`, `current-password`).
