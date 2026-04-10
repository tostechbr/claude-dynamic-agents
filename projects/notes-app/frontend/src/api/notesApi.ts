import { Note, CreateNoteRequest, UpdateNoteRequest, NotesListResponse, ApiResponse } from '../types'

const API_BASE = '/api'

export const notesApi = {
  async getAllNotes(): Promise<Note[]> {
    try {
      const response = await fetch(`${API_BASE}/notes`)
      if (!response.ok) {
        throw new Error(`Failed to fetch notes: ${response.statusText}`)
      }
      const data: NotesListResponse = await response.json()
      if (!data.success) {
        throw new Error(data.error || 'Failed to fetch notes')
      }
      return data.data || []
    } catch (error) {
      console.error('Error fetching notes:', error)
      throw error
    }
  },

  async createNote(note: CreateNoteRequest): Promise<Note> {
    try {
      const response = await fetch(`${API_BASE}/notes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(note),
      })
      if (!response.ok) {
        throw new Error(`Failed to create note: ${response.statusText}`)
      }
      const data: ApiResponse<Note> = await response.json()
      if (!data.success || !data.data) {
        throw new Error(data.error || 'Failed to create note')
      }
      return data.data
    } catch (error) {
      console.error('Error creating note:', error)
      throw error
    }
  },

  async updateNote(id: string, note: UpdateNoteRequest): Promise<Note> {
    try {
      const response = await fetch(`${API_BASE}/notes/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(note),
      })
      if (!response.ok) {
        throw new Error(`Failed to update note: ${response.statusText}`)
      }
      const data: ApiResponse<Note> = await response.json()
      if (!data.success || !data.data) {
        throw new Error(data.error || 'Failed to update note')
      }
      return data.data
    } catch (error) {
      console.error('Error updating note:', error)
      throw error
    }
  },

  async deleteNote(id: string): Promise<void> {
    try {
      const response = await fetch(`${API_BASE}/notes/${id}`, {
        method: 'DELETE',
      })
      if (!response.ok) {
        throw new Error(`Failed to delete note: ${response.statusText}`)
      }
    } catch (error) {
      console.error('Error deleting note:', error)
      throw error
    }
  },
}
