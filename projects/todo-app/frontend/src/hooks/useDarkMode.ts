import { useCallback, useEffect, useState } from "react"

const STORAGE_KEY = "todo-app-dark-mode"

function getInitialDarkMode(): boolean {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored !== null) {
    return stored === "true"
  }
  return window.matchMedia("(prefers-color-scheme: dark)").matches
}

interface UseDarkModeResult {
  readonly isDark: boolean
  readonly toggle: () => void
}

export function useDarkMode(): UseDarkModeResult {
  const [isDark, setIsDark] = useState<boolean>(getInitialDarkMode)

  useEffect(() => {
    const root = document.documentElement
    if (isDark) {
      root.classList.add("dark")
    } else {
      root.classList.remove("dark")
    }
    localStorage.setItem(STORAGE_KEY, String(isDark))
  }, [isDark])

  const toggle = useCallback(() => {
    setIsDark((prev) => !prev)
  }, [])

  return { isDark, toggle }
}
