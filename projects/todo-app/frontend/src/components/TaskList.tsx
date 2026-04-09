import type { Task } from "../types/task"

interface TaskListProps {
  readonly tasks: readonly Task[]
  readonly loading: boolean
  readonly error: string | null
  readonly onMarkDone: (id: number) => Promise<void>
  readonly onDelete: (id: number) => Promise<void>
}

export function TaskList({ tasks, loading, error, onMarkDone, onDelete }: TaskListProps) {
  if (loading) {
    return <p className="task-list-loading">Loading tasks...</p>
  }

  if (error) {
    return <p className="task-list-error" role="alert">Error: {error}</p>
  }

  if (tasks.length === 0) {
    return <p className="task-list-empty">No tasks yet. Create one above!</p>
  }

  return (
    <ul className="task-list">
      {tasks.map((task) => (
        <li key={task.id} className={`task-item ${task.done ? "task-done" : ""}`}>
          <div className="task-content">
            <span className="task-title">{task.title}</span>
            {task.description && (
              <span className="task-description">{task.description}</span>
            )}
          </div>
          <div className="task-actions">
            {!task.done && (
              <button
                className="btn-done"
                onClick={() => onMarkDone(task.id)}
                aria-label={`Mark "${task.title}" as done`}
              >
                ✓ Done
              </button>
            )}
            <button
              className="btn-delete"
              onClick={() => onDelete(task.id)}
              aria-label={`Delete "${task.title}"`}
            >
              ✕ Delete
            </button>
          </div>
        </li>
      ))}
    </ul>
  )
}
