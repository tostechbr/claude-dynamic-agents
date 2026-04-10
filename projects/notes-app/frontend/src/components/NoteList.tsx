import { Note } from '../types'
import { NoteCard } from './NoteCard'

interface NoteListProps {
  notes: Note[]
  onEdit: (note: Note) => void
  onDelete: (id: string) => void
  isEmpty: boolean
}

export function NoteList({ notes, onEdit, onDelete, isEmpty }: NoteListProps) {
  if (isEmpty) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No notes found</p>
        <p className="text-gray-400 text-sm">Create your first note to get started</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {notes.map((note) => (
        <NoteCard
          key={note.id}
          note={note}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}
