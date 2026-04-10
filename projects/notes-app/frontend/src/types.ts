export interface Note {
  id: string
  title: string
  content: string
  tags: string[]
  created_at: string
  updated_at: string
}

export interface CreateNoteRequest {
  title: string
  content: string
  tags: string[]
}

export interface UpdateNoteRequest {
  title: string
  content: string
  tags: string[]
}

export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}

export interface NotesListResponse {
  success: boolean
  data: Note[]
  error?: string
}
