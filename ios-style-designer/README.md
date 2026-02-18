# ios-style-designer

A Claude Code skill that guides the creation of web interfaces following Apple's Human Interface Guidelines (HIG). It translates native iOS/iPadOS design patterns — glassmorphism, SF Pro typography, squircle corners, spring animations — into high-performance web code.

## What It Does

When triggered, this skill instructs Claude to apply iOS-native design principles to web development:

- **Layout**: 8pt grid system, safe area insets, standard margins
- **Typography**: SF Pro font stack with full Dynamic Type scale
- **Visual Style**: iOS system color palette, Light/Dark mode, glassmorphism (`backdrop-blur`)
- **Components**: Navigation bars with large-title collapse, bottom sheets, inset grouped lists
- **Animation**: Apple-standard bezier curves and spring physics, haptic-style press feedback
- **Accessibility**: 44x44pt minimum tap targets, WCAG color contrast

## When It Triggers

- Building web UIs with an iOS-native look and feel
- Implementing glassmorphism, translucency, or vibrancy effects
- Designing mobile-first interfaces with Apple-style components
- User mentions "iOS style", "Apple HIG", "iOS design", etc.

## File Structure

```
ios-style-designer/
├── SKILL.md    # Skill definition (loaded by Claude Code)
└── README.md   # This file
```

## Installation

```bash
claude install-skill /path/to/ios-style-designer.skill
```
