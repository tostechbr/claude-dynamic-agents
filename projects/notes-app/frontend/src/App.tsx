import { useState } from 'react'
import './index.css'
import { Note, CreateNoteRequest } from './types'
import { notesApi } from './api/notesApi'
import { useNotes } from './hooks/useNotes'
import { useTagFilter } from './hooks/useTagFilter'
import { Header } from './components/Header'
import { Modal } from './components/Modal'
import { NoteForm } from './components/NoteForm'
import { NoteList } from './components/NoteList'
import { TagFilter } from './components/TagFilter'

function App() {
  const { notes, loading, error, refreshNotes, deleteNote } = useNotes()
  const { selectedTag, setSelectedTag, allTags, filteredNotes } = useTagFilter(notes)
  const [isFormOpen, setIsFormOpen] = useState(false)
  const [editingNote, setEditingNote] = useState<Note | null>(null)
  const [formError, setFormError] = useState<string | null>(null)

  const handleOpenForm = () => {
    setEditingNote(null)
    setFormError(null)
    setIsFormOpen(true)
  }

  const handleEditNote = (note: Note) => {
    setEditingNote(note)
    setFormError(null)
    setIsFormOpen(true)
  }

  const handleCloseForm = () => {
    setIsFormOpen(false)
    setEditingNote(null)
    setFormError(null)
  }

  const handleSubmitForm = async (noteData: CreateNoteRequest) => {
    try {
      setFormError(null)
      if (editingNote) {
        await notesApi.updateNote(editingNote.id, noteData)
      } else {
        await notesApi.createNote(noteData)
      }
      await refreshNotes()
      handleCloseForm()
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to save note'
      setFormError(message)
      throw err
    }
  }

  const handleDeleteNote = async (id: string) => {
    try {
      await deleteNote(id)
    } catch (err) {
      console.error('Failed to delete note:', err)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header onNewNote={handleOpenForm} isLoading={loading} />

      <main className="max-w-7xl mx-auto px-4 py-8">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            <p className="font-semibold">Error loading notes</p>
            <p className="text-sm">{error.message}</p>
            <button
              onClick={() => refreshNotes()}
              className="mt-2 text-red-600 hover:text-red-700 font-medium text-sm underline"
            >
              Try again
            </button>
          </div>
        )}

        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
              <p className="text-gray-600">Loading notes...</p>
            </div>
          </div>
        )}

        {!loading && (
          <>
            <TagFilter
              tags={allTags}
              selectedTag={selectedTag}
              onTagSelect={setSelectedTag}
            />

            <NoteList
              notes={filteredNotes}
              onEdit={handleEditNote}
              onDelete={handleDeleteNote}
              isEmpty={notes.length === 0}
            />
          </>
        )}
      </main>

      <Modal isOpen={isFormOpen} onClose={handleCloseForm}>
        <NoteForm
          note={editingNote ?? undefined}
          onSubmit={handleSubmitForm}
          onCancel={handleCloseForm}
        />
        {formError && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
            {formError}
          </div>
        )}
      </Modal>
    </div>
  )
}

export default App
