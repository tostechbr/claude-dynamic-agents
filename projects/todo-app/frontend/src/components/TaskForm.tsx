import { type FormEvent, useState } from "react"
import type { TaskCreatePayload } from "../types/task"

interface TaskFormProps {
  readonly onSubmit: (payload: TaskCreatePayload) => Promise<void>
}

export function TaskForm({ onSubmit }: TaskFormProps) {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()

    const trimmedTitle = title.trim()
    if (!trimmedTitle) {
      return
    }

    setSubmitting(true)
    setError(null)

    try {
      const payload: TaskCreatePayload = {
        title: trimmedTitle,
        ...(description.trim() ? { description: description.trim() } : {}),
      }
      await onSubmit(payload)
      setTitle("")
      setDescription("")
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to create task"
      setError(message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <div className="form-field">
        <label htmlFor="task-title">Title</label>
        <input
          id="task-title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          required
          disabled={submitting}
        />
      </div>
      <div className="form-field">
        <label htmlFor="task-description">Description (optional)</label>
        <input
          id="task-description"
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add details..."
          disabled={submitting}
        />
      </div>
      {error && <p className="form-error" role="alert">{error}</p>}
      <button type="submit" disabled={submitting || !title.trim()}>
        {submitting ? "Adding..." : "Add Task"}
      </button>
    </form>
  )
}
