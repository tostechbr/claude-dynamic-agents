import { useState, useMemo } from 'react'
import { Note } from '../types'

interface UseTagFilterReturn {
  selectedTag: string | null
  setSelectedTag: (tag: string | null) => void
  allTags: string[]
  filteredNotes: Note[]
}

export function useTagFilter(notes: Note[]): UseTagFilterReturn {
  const [selectedTag, setSelectedTag] = useState<string | null>(null)

  const allTags = useMemo(() => {
    const tags = new Set<string>()
    notes.forEach((note) => {
      note.tags.forEach((tag) => tags.add(tag))
    })
    return Array.from(tags).sort()
  }, [notes])

  const filteredNotes = useMemo(() => {
    if (!selectedTag) return notes
    return notes.filter((note) => note.tags.includes(selectedTag))
  }, [notes, selectedTag])

  return { selectedTag, setSelectedTag, allTags, filteredNotes }
}
