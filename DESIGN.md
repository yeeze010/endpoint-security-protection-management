# Design

> Auto-generated and maintained by frontend-god-mode.
> Source of truth for typography, color, motion, layout, and component tokens.
> Read this BEFORE touching the UI in any subsequent session.

## Aesthetic direction

Swiss endpoint security operations console: light, gridded, role-aware, built for endpoint inventory, policy rollout, alerts, evidence, and compliance reporting.

## Dials

- DESIGN_VARIANCE: 5 / 10
- MOTION_INTENSITY: 3 / 10
- VISUAL_DENSITY: 7 / 10

## Type stack

- Display: Segoe UI / PingFang SC / Microsoft YaHei
- Body: Segoe UI / PingFang SC / Microsoft YaHei
- Mono: inherited unless code-like content appears
- Loaded via: CSS font stack

Banned in this project: marketing landing pages, toy security language, AI labels, decorative gradients, endpoint data before login.

## Color tokens

```css
:root {
  --bg: #f7f7f8;
  --surface: #ffffff;
  --surface-muted: #eef2f6;
  --text: #111827;
  --muted: #667085;
  --line: #d7dbe0;
  --accent: #002fa7;
  --success: #15803d;
  --warning: #b45309;
  --danger: #b42318;
}
```

## Motion

- Buttons and links use a 1px pressed state.
- Async login uses explicit disabled state and working label.
- Banned: ornamental animation, bounce, hidden hover-only affordances.

## Layout

- Login screen is the only unauthenticated screen.
- Sidebar groups operations by monitoring, protection control, and acceptance governance.
- Role switcher is in the topbar after login.
- Endpoint detail, alert handling, policy rollout, and reporting remain direct work surfaces.

## Component inventory

Vue custom: login card, sidebar nav groups, role switcher, status cards, PageHeader, endpoint asset cards, policy cards, alert detail, report export form.

## Brand voice

- Product name: 计算机终端安全防护管理系统.
- Tone: operational, precise, audit-friendly.
- Banned: vague “smart security” language, fabricated AI agent claims, decorative copy.

## Accessibility floor

- Login form uses real labels and autocomplete.
- Navigation links expose `aria-current`.
- Focus-visible rings remain on buttons, links, inputs, selects, and textareas.

## Last updated

2026-06-26 by Worker B: authentication gate, role switching, endpoint security role definitions, and interaction feedback.
