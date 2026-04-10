import { Note } from '../types'

interface NoteCardProps {
  note: Note
  onEdit: (note: Note) => void
  onDelete: (id: string) => void
}

export function NoteCard({ note, onEdit, onDelete }: NoteCardProps) {
  const contentPreview = note.content.substring(0, 100)
  const showEllipsis = note.content.length > 100

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this note?')) {
      onDelete(note.id)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
      <h3 className="text-lg font-semibold text-gray-800 mb-2 line-clamp-2">
        {note.title}
      </h3>
      <p className="text-gray-600 text-sm mb-3 line-clamp-3">
        {contentPreview}
        {showEllipsis && '...'}
      </p>
      {note.tags.length > 0 && (
        <div className="mb-3 flex flex-wrap gap-1">
          {note.tags.map((tag) => (
            <span
              key={tag}
              className="inline-block bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
      <div className="text-xs text-gray-400 mb-3">
        {new Date(note.updated_at).toLocaleDateString()}
      </div>
      <div className="flex gap-2">
        <button
          onClick={() => onEdit(note)}
          className="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded text-sm transition-colors"
        >
          Edit
        </button>
        <button
          onClick={handleDelete}
          className="flex-1 bg-red-500 hover:bg-red-600 text-white py-1 px-3 rounded text-sm transition-colors"
        >
          Delete
        </button>
      </div>
    </div>
  )
}
