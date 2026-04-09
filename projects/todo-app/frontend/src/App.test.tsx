import { render, screen } from "@testing-library/react"
import { describe, expect, it, vi } from "vitest"
import { App } from "./App"

vi.mock("./services/api", () => ({
  fetchTasks: vi.fn().mockResolvedValue([
    { id: 1, title: "Test task", description: null, done: false },
  ]),
  createTask: vi.fn().mockResolvedValue({
    id: 2,
    title: "New task",
    description: null,
    done: false,
  }),
}))

describe("App", () => {
  it("renders the app heading", () => {
    render(<App />)
    expect(screen.getByRole("heading", { name: "Todo App" })).toBeInTheDocument()
  })

  it("renders the task form", () => {
    render(<App />)
    expect(screen.getByLabelText("Title")).toBeInTheDocument()
    expect(screen.getByRole("button", { name: "Add Task" })).toBeInTheDocument()
  })

  it("shows loading state initially", () => {
    render(<App />)
    expect(screen.getByText("Loading tasks...")).toBeInTheDocument()
  })

  it("renders tasks after loading", async () => {
    render(<App />)
    expect(await screen.findByText("Test task")).toBeInTheDocument()
  })
})
