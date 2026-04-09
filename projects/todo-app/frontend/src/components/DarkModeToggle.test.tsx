import { render, screen, fireEvent } from "@testing-library/react"
import { describe, it, expect, vi } from "vitest"
import { DarkModeToggle } from "./DarkModeToggle"

describe("DarkModeToggle", () => {
  it("renders with moon icon when in light mode", () => {
    render(<DarkModeToggle isDark={false} onToggle={vi.fn()} />)
    const button = screen.getByRole("button", { name: /switch to dark mode/i })
    expect(button).toBeDefined()
  })

  it("renders with sun icon when in dark mode", () => {
    render(<DarkModeToggle isDark={true} onToggle={vi.fn()} />)
    const button = screen.getByRole("button", { name: /switch to light mode/i })
    expect(button).toBeDefined()
  })

  it("calls onToggle when clicked", () => {
    const onToggle = vi.fn()
    render(<DarkModeToggle isDark={false} onToggle={onToggle} />)
    const button = screen.getByRole("button")
    fireEvent.click(button)
    expect(onToggle).toHaveBeenCalledTimes(1)
  })
})
