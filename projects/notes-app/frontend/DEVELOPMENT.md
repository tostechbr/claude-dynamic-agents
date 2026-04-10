# Development Guide

## Getting Started

### Prerequisites
- Node.js 16+
- A running backend API at `http://localhost:8000/api`

### Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app runs at `http://localhost:5173` with automatic hot reload.

## Development Workflow

### Component Development

All components are in `src/components/`. Follow these patterns:

1. **Functional Components**: Use React function components with TypeScript
2. **Props**: Define clear prop interfaces
3. **Hooks**: Keep component logic focused and testable

Example:
```typescript
interface MyComponentProps {
  data: string
  onEvent: (value: string) => void
}

export function MyComponent({ data, onEvent }: MyComponentProps) {
  // Component code
}
```

### Custom Hooks

Hooks go in `src/hooks/`. They should handle:
- Data fetching and state management
- Business logic
- Side effects

The app uses `useNotes` and `useTagFilter` hooks - add more as needed.

### API Integration

All backend calls go through `src/api/notesApi.ts`. Pattern:

```typescript
async function operationName(): Promise<ReturnType> {
  try {
    const response = await fetch(endpoint, options)
    if (!response.ok) throw new Error(...)
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}
```

## Testing

### Manual Testing Checklist

Before marking features complete:

1. **Create Note**
   - [ ] Form opens/closes correctly
   - [ ] All fields validate
   - [ ] Success shows in list
   - [ ] Tags parse correctly

2. **View Notes**
   - [ ] Initial load fetches notes
   - [ ] Grid displays all notes
   - [ ] Empty state shows when no notes
   - [ ] Note cards show all data

3. **Edit Note**
   - [ ] Form prefills with existing data
   - [ ] Changes save correctly
   - [ ] Form closes after save
   - [ ] List updates immediately

4. **Delete Note**
   - [ ] Confirmation modal appears
   - [ ] Cancel doesn't delete
   - [ ] Confirm removes from list
   - [ ] Deleted note is gone

5. **Tag Filtering**
   - [ ] Filter buttons appear when tags exist
   - [ ] Selecting tag filters correctly
   - [ ] "All Notes" clears filter
   - [ ] Multiple notes per tag works

6. **Error Handling**
   - [ ] Network errors show message
   - [ ] Retry button works
   - [ ] Form errors prevent submission
   - [ ] API errors are user-friendly

## Building

```bash
# Type check
npm run type-check

# Build for production
npm run build

# Preview production build
npm run preview
```

Output goes to `dist/` directory.

## Code Quality

```bash
# Lint code
npm run lint
```

The project uses:
- TypeScript for type safety
- ESLint for code quality
- Tailwind CSS for styling

## Architecture Notes

### State Management

The app uses React Hooks for state:
- `useNotes`: Global note data and operations
- `useTagFilter`: Tag filtering logic
- Component local state: Form inputs, modals

No Redux/Zustand needed for this MVP.

### Data Flow

```
App (root)
├── useNotes() → notes, loading, error
├── useTagFilter(notes) → filtered notes, selected tag
├── Header: handles new note clicks
├── Modal: form dialog
└── NoteList: displays filtered notes
    └── NoteCard: individual note
```

### Error Handling Strategy

1. **API Errors**: Caught and displayed in UI
2. **Form Errors**: Validation prevents submission
3. **Delete Errors**: User can retry
4. **Loading States**: Spinner during fetch

## Performance

- Components use memoization (`useMemo`) for tag extraction
- No unnecessary re-renders via proper hook dependencies
- CSS grid for responsive layout
- Lazy loading with modal for forms

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- No IE11 support

## Troubleshooting

### API not connecting?
- Ensure backend runs on `http://localhost:8000`
- Check CORS headers in backend
- Vite proxy should handle `/api` calls

### Styles not working?
- Run `npm install` to ensure Tailwind is installed
- Check `tailwind.config.js` includes correct paths
- Rebuild CSS: delete `dist/` and run `npm run build`

### Type errors?
- Run `npm run type-check` to see all issues
- Check that all imports have proper types
- Update TypeScript if needed

## Adding Features

### New Component

1. Create file in `src/components/ComponentName.tsx`
2. Define props interface
3. Implement component
4. Export from App.tsx
5. Add to JSX

### New Hook

1. Create file in `src/hooks/useFeature.ts`
2. Export hook function
3. Use in components
4. Add tests if complex

### New API Endpoint

1. Add function to `src/api/notesApi.ts`
2. Define types in `src/types.ts`
3. Handle errors properly
4. Use in hooks or components
