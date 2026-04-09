import type { Task, TaskCreatePayload } from "../types/task"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"

export class ApiError extends Error {
  readonly status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const message = await response.text().catch(() => "Unknown error")
    throw new ApiError(message, response.status)
  }
  return response.json() as Promise<T>
}

export async function fetchTasks(): Promise<readonly Task[]> {
  const response = await fetch(`${API_BASE_URL}/tasks`)
  return handleResponse<readonly Task[]>(response)
}

export async function createTask(payload: TaskCreatePayload): Promise<Task> {
  const response = await fetch(`${API_BASE_URL}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  return handleResponse<Task>(response)
}

export async function markTaskDone(id: number): Promise<Task> {
  const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
    method: "PATCH",
  })
  return handleResponse<Task>(response)
}

export async function deleteTask(id: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
    method: "DELETE",
  })
  if (!response.ok) {
    const message = await response.text().catch(() => "Unknown error")
    throw new ApiError(message, response.status)
  }
}
