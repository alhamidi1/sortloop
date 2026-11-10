---
version: alpha
name: SortLoop
description: A material intake workbench inspired by sorting trays and recycling labels.
colors:
  primary: '#174F46'
  background: '#F3F6F3'
  surface: '#FFFFFF'
  ink: '#20372F'
  muted: '#586B63'
  accent: '#E3AB87'
  line: '#D8E2DB'
typography:
  display:
    fontFamily: 'Trebuchet MS, sans-serif'
  sans:
    fontFamily: 'Arial, sans-serif'
  mono:
    fontFamily: 'ui-monospace, monospace'
rounded:
  DEFAULT: '16px'
  sm: '8px'
spacing:
  section-gap: '32px'
  page-max: '1200px'
components:
  button:
    height: '44px'
  card:
    rounded: '16px'
---
## Overview
Product register; English interface for small collection operators, desktop intake and phone photography. No Japan-specific market. Signature: large pale mint inspection tray with crop corners and a real material photograph. Avoid generic analytics dashboards and invented metrics. Shared tokens in dist/style.css mirror this document; no independent theme adapters.
## Colors
Forest primary communicates operational confidence, white work surfaces, mineral background and peach trial label. Error text uses #9D3426. Scrollbar thumb uses muted, track background, hover primary, active ink. Forced colors use system controls.
## Typography
Trebuchet display for generous, rounded headlines; Arial body for legibility; monospace for station labels and measured values. Fonts are local to avoid font-swap shifts.
## Layout
1200px content, 32px gaps; two-column inspection workbench becoming a single column below 800px. Natural document scrolling. 44px controls. Reserve photo and feedback geometry.
## Elevation & Depth
Borders and tonal surfaces distinguish panels. No decorative gradients. Modest shadow only on the inspection photograph.
## Shapes
16px trays, 8px fields. Capsule status labels. Crop-corner marks connect the UI to the photographed item.
## Components
Buttons share hover, focus and disabled states. Native selects intentionally permit platform popups. Feedback uses a persistent live region. Tables use bounded paging and native semantics. No destructive actions. Motion only on loading; reduced motion disables animation. Text and labels accompany every status color.
## Do's and Don'ts
Use real held-out samples and measured evaluation. Never portray model scores as calibrated certainty or recyclability guarantees. Keep manual review prominent.
