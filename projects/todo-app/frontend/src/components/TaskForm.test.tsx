import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import { TaskForm } from "./TaskForm"

describe("TaskForm", () => {
  it("renders title and description inputs", () => {
    render(<TaskForm onSubmit={vi.fn()} />)
    expect(screen.getByLabelText("Title")).toBeInTheDocument()
    expect(screen.getByLabelText("Description (optional)")).toBeInTheDocument()
  })

  it("renders submit button", () => {
    render(<TaskForm onSubmit={vi.fn()} />)
    expect(screen.getByRole("button", { name: "Add Task" })).toBeInTheDocument()
  })

  it("disables submit button when title is empty", () => {
    render(<TaskForm onSubmit={vi.fn()} />)
    expect(screen.getByRole("button", { name: "Add Task" })).toBeDisabled()
  })

  it("enables submit button when title has content", async () => {
    const user = userEvent.setup()
    render(<TaskForm onSubmit={vi.fn()} />)

    await user.type(screen.getByLabelText("Title"), "New task")
    expect(screen.getByRole("button", { name: "Add Task" })).toBeEnabled()
  })

  it("calls onSubmit with title only when no description", async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn().mockResolvedValue(undefined)
    render(<TaskForm onSubmit={onSubmit} />)

    await user.type(screen.getByLabelText("Title"), "Buy milk")
    await user.click(screen.getByRole("button", { name: "Add Task" }))

    expect(onSubmit).toHaveBeenCalledOnce()
    expect(onSubmit).toHaveBeenCalledWith({ title: "Buy milk" })
  })

  it("calls onSubmit with title and description when provided", async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn().mockResolvedValue(undefined)
    render(<TaskForm onSubmit={onSubmit} />)

    await user.type(screen.getByLabelText("Title"), "Buy milk")
    await user.type(screen.getByLabelText("Description (optional)"), "From the store")
    await user.click(screen.getByRole("button", { name: "Add Task" }))

    expect(onSubmit).toHaveBeenCalledOnce()
    expect(onSubmit).toHaveBeenCalledWith({
      title: "Buy milk",
      description: "From the store",
    })
  })

  it("resets form after successful submission", async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn().mockResolvedValue(undefined)
    render(<TaskForm onSubmit={onSubmit} />)

    await user.type(screen.getByLabelText("Title"), "Buy milk")
    await user.type(screen.getByLabelText("Description (optional)"), "2% milk")
    await user.click(screen.getByRole("button", { name: "Add Task" }))

    expect(screen.getByLabelText("Title")).toHaveValue("")
    expect(screen.getByLabelText("Description (optional)")).toHaveValue("")
  })

  it("shows error message when submission fails", async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn().mockRejectedValue(new Error("Server error"))
    render(<TaskForm onSubmit={onSubmit} />)

    await user.type(screen.getByLabelText("Title"), "Buy milk")
    await user.click(screen.getByRole("button", { name: "Add Task" }))

    expect(screen.getByRole("alert")).toHaveTextContent("Server error")
  })

  it("does not reset form after failed submission", async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn().mockRejectedValue(new Error("Server error"))
    render(<TaskForm onSubmit={onSubmit} />)

    await user.type(screen.getByLabelText("Title"), "Buy milk")
    await user.click(screen.getByRole("button", { name: "Add Task" }))

    expect(screen.getByLabelText("Title")).toHaveValue("Buy milk")
  })

  it("trims whitespace from title before submitting", async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn().mockResolvedValue(undefined)
    render(<TaskForm onSubmit={onSubmit} />)

    await user.type(screen.getByLabelText("Title"), "  Buy milk  ")
    await user.click(screen.getByRole("button", { name: "Add Task" }))

    expect(onSubmit).toHaveBeenCalledWith({ title: "Buy milk" })
  })

  it("shows Adding... text while submitting", async () => {
    const user = userEvent.setup()
    let resolveSubmit: () => void
    const onSubmit = vi.fn().mockImplementation(
      () => new Promise<void>((resolve) => { resolveSubmit = resolve }),
    )
    render(<TaskForm onSubmit={onSubmit} />)

    await user.type(screen.getByLabelText("Title"), "Buy milk")
    await user.click(screen.getByRole("button", { name: "Add Task" }))

    expect(screen.getByRole("button", { name: "Adding..." })).toBeDisabled()

    resolveSubmit!()
  })
})
