export interface Task {
  readonly id: number
  readonly title: string
  readonly description: string | null
  readonly done: boolean
}

export interface TaskCreatePayload {
  readonly title: string
  readonly description?: string
}
