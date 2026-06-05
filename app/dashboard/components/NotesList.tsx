import type { Note, Profile } from '@/lib/types'
import NoteCard from './NoteCard'

interface Props {
  notes: Note[]
  onEdit: (note: Note) => void
  onDelete: (id: string) => void
  onToggleComplete: (id: string, completed: boolean) => void
  currentUserId?: string
  profiles: Profile[]
  onView: (noteId: string) => void
}

export default function NotesList({ notes, onEdit, onDelete, onToggleComplete, currentUserId, profiles, onView }: Props) {
  if (notes.length === 0) {
    return <p className="text-gray-500">No hay notas en esta seccion.</p>
  }
  return (
    <div className="grid gap-4">
      {notes.map(note => (
        <NoteCard
          key={note.id}
          note={note}
          onEdit={() => onEdit(note)}
          onDelete={() => onDelete(note.id)}
          onToggleComplete={() => onToggleComplete(note.id, !note.is_completed)}
          currentUserId={currentUserId}
          profiles={profiles}
          onView={() => onView(note.id)}
        />
      ))}
    </div>
  )
}
