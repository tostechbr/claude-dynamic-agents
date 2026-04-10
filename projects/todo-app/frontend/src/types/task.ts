export type Priority = 'low' | 'medium' | 'high'

export interface Task {
  readonly id: number
  readonly title: string
  readonly description: string | null
  readonly done: boolean
  readonly priority: Priority
}

export interface TaskCreatePayload {
  readonly title: string
  readonly description?: string
  readonly priority: Priority
}
