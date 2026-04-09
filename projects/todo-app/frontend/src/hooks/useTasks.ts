import { useCallback, useEffect, useState } from "react"
import type { Task } from "../types/task"
import type { TaskCreatePayload } from "../types/task"
import * as api from "../services/api"

interface UseTasksResult {
  readonly tasks: readonly Task[]
  readonly loading: boolean
  readonly error: string | null
  readonly addTask: (payload: TaskCreatePayload) => Promise<void>
  readonly markDone: (id: number) => Promise<void>
  readonly removeTask: (id: number) => Promise<void>
  readonly refresh: () => Promise<void>
}

export function useTasks(): UseTasksResult {
  const [tasks, setTasks] = useState<readonly Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const fetched = await api.fetchTasks()
      setTasks(fetched)
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to load tasks"
      setError(message)
    } finally {
      setLoading(false)
    }
  }, [])

  const addTask = useCallback(
    async (payload: TaskCreatePayload) => {
      const created = await api.createTask(payload)
      setTasks((prev) => [...prev, created])
    },
    [],
  )

  const markDone = useCallback(
    async (id: number) => {
      const updated = await api.markTaskDone(id)
      setTasks((prev) => prev.map((t) => (t.id === id ? updated : t)))
    },
    [],
  )

  const removeTask = useCallback(
    async (id: number) => {
      await api.deleteTask(id)
      setTasks((prev) => prev.filter((t) => t.id !== id))
    },
    [],
  )

  useEffect(() => {
    refresh()
  }, [refresh])

  return { tasks, loading, error, addTask, markDone, removeTask, refresh }
}
