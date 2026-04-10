import { useState, useEffect, useCallback } from 'react'
import { Note } from '../types'
import { notesApi } from '../api/notesApi'

interface UseNotesReturn {
  notes: Note[]
  loading: boolean
  error: Error | null
  refreshNotes: () => Promise<void>
  deleteNote: (id: string) => Promise<void>
}

export function useNotes(): UseNotesReturn {
  const [notes, setNotes] = useState<Note[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  const refreshNotes = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await notesApi.getAllNotes()
      setNotes(data)
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch notes'))
    } finally {
      setLoading(false)
    }
  }, [])

  const deleteNote = useCallback(async (id: string) => {
    try {
      await notesApi.deleteNote(id)
      setNotes((prev) => prev.filter((note) => note.id !== id))
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to delete note')
      setError(error)
      throw error
    }
  }, [])

  useEffect(() => {
    refreshNotes()
  }, [refreshNotes])

  return { notes, loading, error, refreshNotes, deleteNote }
}
