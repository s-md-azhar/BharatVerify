# Design Decisions

## Inspiration Principles
Used internet research and general enterprise patterns to define the UI aesthetic. The visual language communicates:
- **Trust & Compliance**: Restrained neutral base with strong, purposeful accent colors. No flashy gradients or "AI sparkles".
- **Information Density**: Compliance operators need simultaneous visibility into evidence, flags, and audit history. We use dense but clear layouts, side panels, and tabular data.
- **Clear Hierarchy**: The overall decision (VERIFIED, REVIEW, MISMATCH) is immediately visible, followed by field-level evidence and a detailed audit trail.

## Implementation Choices
- **Tailwind CSS**: For rapid, consistent, utility-first styling.
- **Lucide Icons**: Restrained and professional iconography.
- **Server-Sent Events**: To provide live pipeline visualization without faking loading bars.
- **Color Palette**: Slate/Zinc for neutrals, Emerald for success, Amber for review, Rose for mismatch.
