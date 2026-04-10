interface HeaderProps {
  onNewNote: () => void
  isLoading: boolean
}

export function Header({ onNewNote, isLoading }: HeaderProps) {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 py-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Notes App</h1>
          <p className="text-blue-100 text-sm mt-1">Organize your thoughts</p>
        </div>
        <button
          onClick={onNewNote}
          disabled={isLoading}
          className="bg-white text-blue-600 hover:bg-blue-50 disabled:opacity-50 font-semibold py-2 px-6 rounded-lg transition-colors"
        >
          + New Note
        </button>
      </div>
    </header>
  )
}
