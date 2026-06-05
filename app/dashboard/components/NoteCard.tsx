import { useEffect, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import type { Note, Profile } from '@/lib/types'
import { createClient } from '@/lib/supabase/client'

interface Props {
  note: Note
  onEdit: () => void
  onDelete: () => void
  onToggleComplete: () => void
  currentUserId?: string
  profiles: Profile[]
  onView: () => void
}

export default function NoteCard({ note, onEdit, onDelete, onToggleComplete, currentUserId, profiles, onView }: Props) {
  const [taggedUsers, setTaggedUsers] = useState<Profile[]>([])
  const [viewers, setViewers] = useState<Profile[]>([])
  const supabase = createClient()

  useEffect(() => {
    const fetchMeta = async () => {
      const { data: tags } = await supabase.from('note_tagged_users').select('user_id').eq('note_id', note.id)
      const { data: views } = await supabase.from('note_views').select('user_id').eq('note_id', note.id)
      const tagIds = tags?.map(t => t.user_id) || []
      const viewIds = views?.map(v => v.user_id) || []
      setTaggedUsers(profiles.filter(p => tagIds.includes(p.id)))
      setViewers(profiles.filter(p => viewIds.includes(p.id)))
    }
    fetchMeta()
  }, [note.id, profiles, supabase])

  // Auto-embed de YouTube
  const contentWithEmbeds = note.content.replace(
    /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]+)/g,
    (match, id) => `<iframe width="100%" height="315" src="https://www.youtube.com/embed/${id}" frameborder="0" allowfullscreen></iframe>`
  )

  return (
    <div className="bg-white rounded shadow p-4 hover:shadow-md transition" onClick={onView}>
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={note.is_completed}
            onChange={onToggleComplete}
            className="h-5 w-5"
          />
          <h3 className={`font-semibold ${note.is_completed ? 'line-through text-gray-400' : ''}`}>
            {note.title || 'Sin titulo'}
          </h3>
          {note.is_proposal && (
            <span className={`text-xs px-2 py-0.5 rounded ${
              note.proposal_status === 'open' ? 'bg-yellow-200 text-yellow-800' :
              note.proposal_status === 'accepted' ? 'bg-green-200 text-green-800' :
              'bg-red-200 text-red-800'
            }`}>
              {note.proposal_status || 'abierta'}
            </span>
          )}
        </div>
        <div className="flex gap-2">
          <button onClick={onEdit} className="text-sm text-blue-600 hover:underline">Editar</button>
          <button onClick={onDelete} className="text-sm text-red-600 hover:underline">Eliminar</button>
        </div>
      </div>
      <div className="mt-2 prose prose-sm max-w-none" dangerouslySetInnerHTML={{ __html: contentWithEmbeds }} />
      <div className="mt-3 flex flex-wrap gap-2 text-xs text-gray-500">
        {note.last_editor && (
          <span>Ultima edicion: {note.last_editor.display_name || note.last_editor.email} - {new Date(note.last_edited_at!).toLocaleString()}</span>
        )}
        {taggedUsers.length > 0 && (
          <span>Etiquetados: {taggedUsers.map(u => u.display_name || u.email).join(', ')}</span>
        )}
        {viewers.length > 0 && (
          <span>Visto por: {viewers.map(u => u.display_name || u.email).join(', ')}</span>
        )}
      </div>
    </div>
  )
}
