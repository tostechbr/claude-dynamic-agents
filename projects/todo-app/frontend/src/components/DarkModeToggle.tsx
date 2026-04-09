interface DarkModeToggleProps {
  readonly isDark: boolean
  readonly onToggle: () => void
}

export function DarkModeToggle({ isDark, onToggle }: DarkModeToggleProps) {
  return (
    <button
      className="dark-mode-toggle"
      onClick={onToggle}
      aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
      type="button"
    >
      <span className="dark-mode-icon" aria-hidden="true">
        {isDark ? "\u2600\uFE0F" : "\uD83C\uDF19"}
      </span>
    </button>
  )
}
