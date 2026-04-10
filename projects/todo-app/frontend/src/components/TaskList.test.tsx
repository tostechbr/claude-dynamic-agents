import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"
import { TaskList } from "./TaskList"
import type { Task } from "../types/task"

const MOCK_TASKS: readonly Task[] = [
  { id: 1, title: "Buy groceries", description: "Milk, eggs, bread", done: false, priority: "medium" },
  { id: 2, title: "Walk the dog", description: null, done: true, priority: "high" },
  { id: 3, title: "Read a book", description: "Chapter 5", done: false, priority: "low" },
]

describe("TaskList", () => {
  it("renders loading state", () => {
    render(<TaskList tasks={[]} loading={true} error={null} />)
    expect(screen.getByText("Loading tasks...")).toBeInTheDocument()
  })

  it("renders error state", () => {
    render(<TaskList tasks={[]} loading={false} error="Network error" />)
    const alert = screen.getByRole("alert")
    expect(alert).toHaveTextContent("Error: Network error")
  })

  it("renders empty state when no tasks", () => {
    render(<TaskList tasks={[]} loading={false} error={null} />)
    expect(screen.getByText("No tasks yet. Create one above!")).toBeInTheDocument()
  })

  it("renders all tasks", () => {
    render(<TaskList tasks={MOCK_TASKS} loading={false} error={null} />)
    expect(screen.getByText("Buy groceries")).toBeInTheDocument()
    expect(screen.getByText("Walk the dog")).toBeInTheDocument()
    expect(screen.getByText("Read a book")).toBeInTheDocument()
  })

  it("renders task descriptions when present", () => {
    render(<TaskList tasks={MOCK_TASKS} loading={false} error={null} />)
    expect(screen.getByText("Milk, eggs, bread")).toBeInTheDocument()
    expect(screen.getByText("Chapter 5")).toBeInTheDocument()
  })

  it("does not render description for tasks without one", () => {
    const tasksWithoutDesc: readonly Task[] = [
      { id: 1, title: "No desc task", description: null, done: false, priority: "medium" },
    ]
    render(<TaskList tasks={tasksWithoutDesc} loading={false} error={null} />)
    expect(screen.getByText("No desc task")).toBeInTheDocument()
    const listItem = screen.getByText("No desc task").closest("li")
    expect(listItem?.querySelectorAll(".task-description")).toHaveLength(0)
  })

  it("applies done styling class to completed tasks", () => {
    render(<TaskList tasks={MOCK_TASKS} loading={false} error={null} />)
    const doneTask = screen.getByText("Walk the dog").closest("li")
    expect(doneTask).toHaveClass("task-done")

    const pendingTask = screen.getByText("Buy groceries").closest("li")
    expect(pendingTask).not.toHaveClass("task-done")
  })

  it("prioritizes loading over empty state", () => {
    render(<TaskList tasks={[]} loading={true} error={null} />)
    expect(screen.getByText("Loading tasks...")).toBeInTheDocument()
    expect(screen.queryByText("No tasks yet. Create one above!")).not.toBeInTheDocument()
  })

  it("prioritizes error over empty state", () => {
    render(<TaskList tasks={[]} loading={false} error="Server down" />)
    expect(screen.getByRole("alert")).toBeInTheDocument()
    expect(screen.queryByText("No tasks yet. Create one above!")).not.toBeInTheDocument()
  })
})
