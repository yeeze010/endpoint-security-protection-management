# Design System Master

## Product

计算机终端安全防护管理系统 is a Swiss endpoint security operations console for endpoint inventory, policy rollout, alerts, evidence, and compliance reporting. Endpoint data is hidden until login.

## Visual System

- Direction: light, gridded, role-aware operational console.
- Surfaces: neutral `#f7f7f8`, white panels, crisp 1px rules.
- Accent: Yves Klein Blue `#002fa7` for primary actions and focus.
- Typography: Chinese-first Segoe UI / PingFang SC / Microsoft YaHei stack.
- Motion: minimal action feedback only; respect `prefers-reduced-motion`.

## Required UX Rules

- Login form uses real labels, role selection, username/password autocomplete, and async feedback.
- Navigation exposes `aria-current` and a keyboard-visible focus state.
- Buttons, links, checkboxes, selects, and inputs must have 44px touch targets where interactive.
- Status must combine text with border/shape/color.
- Mobile sidebar uses a scrim and does not hide content behind fixed UI.
- Forms need visible labels and inline actionable feedback.

## Audit Checklist

- Accessibility: labels, skip link, focus-visible, contrast, role state.
- Touch & Interaction: 44px controls, disabled states, button feedback.
- Performance: no decorative motion; stable layout dimensions.
- Layout/Responsive: `100dvh`, mobile nav, single-column forms.
- Forms & Feedback: inline notices and validation.
- Charts & Data: report/metric data uses readable textual summaries.
