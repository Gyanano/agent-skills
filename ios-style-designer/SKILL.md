---
name: ios-style-designer
description: >
  Architect web interfaces that adhere to Apple's Human Interface Guidelines (HIG),
  translating native iOS/iPadOS design patterns into high-performance web environments.
  Use when: (1) building web UIs with iOS-native look and feel, (2) implementing glassmorphism,
  translucency, or vibrancy effects, (3) designing mobile-first interfaces with Apple-style
  components (bottom sheets, navigation bars, inset grouped lists), (4) applying SF Pro typography,
  8pt grid systems, or squircle corner radii, (5) creating Light/Dark mode adaptive designs
  following Apple's system color palette, (6) the user mentions "iOS style", "Apple HIG",
  "iOS design", or wants a native-feeling mobile web app.
---

# iOS Frontend Design

## Core Principles

1. **Clarity**: Legible text at every size, precise icons, subtle adornments that enhance understanding.
2. **Deference**: Fluid motion and beautiful interface that supports content without competing with it.
3. **Depth**: Visual layers, translucency (glassmorphism), and realistic shadows to convey hierarchy.

## Layout & Composition

- **Safe Areas**: Respect device-specific safe areas. Use `env(safe-area-inset-*)` for CSS positioning.
- **8pt Grid**: Align all elements to an 8pt grid. Spacing: 8, 16, 24, or 32pt increments.
- **Margins**: Standard horizontal gutter of 16pt or 20pt for content alignment.

## Visual Language

### Typography
- System font stack: `-apple-system`, `BlinkMacSystemFont`, `"SF Pro Text"`, `"SF Pro Display"`.
- Dynamic Type scale: Large Title 34pt, Title 1 28pt, Title 2 22pt, Title 3 20pt, Headline 17pt bold, Body 17pt, Callout 16pt, Subhead 15pt, Footnote 13pt, Caption 12pt.

### Corner Radius (Squircles)
- Use continuous corner curves (Squircle), not standard geometric circles.
- Containers: 10pt to 20pt. Nested radius: `Inner Radius = Outer Radius - Padding`.

### Color & Adaptivity
- iOS System Palette: `systemBlue (#007AFF)`, `systemGreen (#34C759)`, `systemRed (#FF3B30)`, `systemOrange (#FF9500)`, `systemYellow (#FFCC00)`, `systemGray (#8E8E93)`.
- Support seamless Light/Dark mode transitions.
- Translucency: `backdrop-filter: blur(20px)` + semi-transparent backgrounds for the iOS glass effect.

## Component Standards

- **Navigation Bar**: "Large Title to Inline Title" collapse transition on scroll.
- **Bottom Sheets**: Prioritize for mobile modals. Include visible grabber handle at top.
- **Buttons**:
  - Filled: High emphasis, subtle drop shadow, rounded corners.
  - Plain: System blue text, no background.
- **Inset Grouped Lists**: Rounded-corner cards with distinct section headers.
- **Minimum tap target**: 44x44pt.

## Animation & Interaction

- **Easing**: `cubic-bezier(0.25, 0.1, 0.25, 1.0)` or spring physics. Never linear.
- **Haptic Simulation**: Subtle `scale(0.96)` on press for interactive elements.
- **Transitions**: 200-300ms duration for most UI transitions.

## Tailwind CSS Example

```html
<div class="bg-white/80 dark:bg-black/80 backdrop-blur-xl rounded-[20px] p-5 shadow-sm border border-black/[0.05] dark:border-white/[0.1] active:scale-[0.98] transition-all duration-200">
  <h1 class="text-[34px] font-bold tracking-tight text-black dark:text-white">
    Activity
  </h1>
  <p class="text-[17px] text-gray-500 dark:text-gray-400 mt-1">
    Daily Summary
  </p>
  <button class="mt-6 w-full bg-[#007AFF] hover:bg-[#0071E3] text-white font-semibold py-3 rounded-xl transition-colors">
    View Details
  </button>
</div>
```

## Checklist

- [ ] Safe area insets handled (Home Indicator, Status Bar)?
- [ ] Minimum tap target 44x44pt?
- [ ] `backdrop-blur` and vibrancy on overlays?
- [ ] Color contrast meets WCAG in both Light and Dark modes?
- [ ] Animations use spring physics or Apple-standard bezier curves?

## Evaluation Criteria

- **Native Fidelity**: Does the UI feel like a native App Store app?
- **Consistency**: Uniform corner radii, spacing, and typography weights throughout?
- **Elegance**: Sufficient whitespace to prevent clutter?
