# Notes App Frontend

A modern React + TypeScript frontend for a notes application with tag filtering and full CRUD operations.

## Features

- View all notes in a responsive grid layout
- Create new notes with title, content, and tags
- Edit existing notes
- Delete notes with confirmation
- Filter notes by tags
- Empty state handling
- Loading and error states
- Form validation
- Responsive design with Tailwind CSS

## Tech Stack

- React 18
- TypeScript
- Vite
- Tailwind CSS
- React Hooks for state management

## Setup

### Prerequisites

- Node.js 16+
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173` with API proxy to `http://localhost:8000/api`

### Build

```bash
npm run build
```

### Type Check

```bash
npm run type-check
```

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── notesApi.ts          # API client for backend calls
│   ├── components/
│   │   ├── Header.tsx           # App header with new note button
│   │   ├── Modal.tsx            # Reusable modal component
│   │   ├── NoteCard.tsx         # Single note card display
│   │   ├── NoteForm.tsx         # Create/edit form
│   │   ├── NoteList.tsx         # Grid of note cards
│   │   └── TagFilter.tsx        # Tag filtering component
│   ├── hooks/
│   │   ├── useNotes.ts          # Notes data management
│   │   └── useTagFilter.ts      # Tag filtering logic
│   ├── types.ts                 # TypeScript types
│   ├── App.tsx                  # Main app component
│   ├── main.tsx                 # Entry point
│   └── index.css                # Tailwind styles
├── public/
│   └── vite.svg                 # Vite logo
├── index.html                   # HTML template
├── vite.config.ts               # Vite configuration
├── tsconfig.json                # TypeScript config
└── package.json                 # Dependencies

```

## API Integration

The frontend expects a backend API at `http://localhost:8000/api` with the following endpoints:

### GET /api/notes
Fetch all notes. Returns `{ success: bool, data: Note[] }`

### POST /api/notes
Create a new note. Expects `{ title, content, tags }`. Returns `{ success: bool, data: Note }`

### PUT /api/notes/:id
Update a note. Expects `{ title, content, tags }`. Returns `{ success: bool, data: Note }`

### DELETE /api/notes/:id
Delete a note. Returns success status.

## Component Details

### NoteCard
Displays a single note with:
- Title (truncated if too long)
- Content preview (100 chars)
- Tag badges
- Last updated date
- Edit and Delete buttons

### NoteForm
Create/edit form with:
- Title input (required)
- Content textarea (required)
- Comma-separated tags input
- Form validation
- Error display

### TagFilter
Tag filtering UI with:
- "All Notes" button to clear filter
- Individual tag buttons
- Active state highlighting

### Modal
Simple modal wrapper for forms with:
- Overlay background
- Close button
- Scrollable content

## Hooks

### useNotes()
Manages note data fetching and operations:
- Initial load on mount
- Refresh functionality
- Delete operation with optimistic update

### useTagFilter(notes)
Manages tag filtering logic:
- Extract all unique tags
- Filter notes by selected tag
- Memoized for performance

## Error Handling

- API errors are caught and displayed to users
- Form validation prevents submission of empty fields
- Delete operations require confirmation
- Network errors show retry option
- Comprehensive try-catch blocks in API calls

## Styling

Uses Tailwind CSS for utility-first styling with:
- Responsive grid layout
- Hover effects
- Loading spinner animation
- Focus states for accessibility
- Color-coded UI (blue for primary, red for destructive)

## Future Enhancements

- Search functionality
- Note sorting (date, title, etc.)
- Favorites/pinned notes
- Dark mode
- Note categories/folders
- Rich text editor
- Local storage caching
- Offline support
