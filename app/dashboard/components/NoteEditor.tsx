import { useState, useEffect } from 'react'
import type { Note, Section, Profile } from '@/lib/types'
import { createClient } from '@/lib/supabase/client'

interface Props {
  note: Note
  sections: Section[]
  profiles: Profile[]
  onSave: (note: Note, taggedUserIds: string[]) => void
  onClose: () => void
  currentUserId: string
}

export default function NoteEditor({ note, sections, profiles, onSave, onClose, currentUserId }: Props) {
  const [title, setTitle] = useState(note.title)
  const [content, setContent] = useState(note.content)
  const [sectionId, setSectionId] = useState(note.section_id || '')
  const [isCompleted, setIsCompleted] = useState(note.is_completed)
  const [isProposal, setIsProposal] = useState(note.is_proposal)
  const [proposalStatus, setProposalStatus] = useState(note.proposal_status || 'open')
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const supabase = createClient()

  useEffect(() => {
    const fetchTags = async () => {
      if (note.id) {
        const { data } = await supabase.from('note_tagged_users').select('user_id').eq('note_id', note.id)
        setSelectedTags(data?.map(t => t.user_id) || [])
      }
    }
    fetchTags()
  }, [note.id, supabase])

  const handleSave = () => {
    onSave(
      {
        ...note,
        title,
        content,
        section_id: sectionId || null,
        is_completed: isCompleted,
        is_proposal: isProposal,
        proposal_status: isProposal ? proposalStatus : null,
      },
      selectedTags.filter(id => id !== currentUserId) // evitar auto-etiquetarse
    )
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-lg w-full max-w-2xl p-6 max-h-[90vh] overflow-y-auto">
        <h2 className="text-xl font-bold mb-4">{note.id ? 'Editar nota' : 'Nueva nota'}</h2>
        <input
          type="text"
          placeholder="Titulo"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full border rounded p-2 mb-3"
        />
        <textarea
          placeholder="Contenido (Markdown, enlaces, imagenes, videos de YouTube)"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="w-full border rounded p-2 mb-3 h-40"
        />
        <div className="grid grid-cols-2 gap-4 mb-3">
          <div>
            <label className="block text-sm font-medium">Seccion</label>
            <select value={sectionId} onChange={(e) => setSectionId(e.target.value)} className="w-full border rounded p-2">
              <option value="">Sin seccion</option>
              {sections.map(s => <option key={s.id} value={s.id}>{s.title}</option>)}
            </select>
          </div>
          <div className="flex items-center gap-4">
            <label className="flex items-center gap-1 text-sm">
              <input type="checkbox" checked={isCompleted} onChange={(e) => setIsCompleted(e.target.checked)} />
              Completada
            </label>
            <label className="flex items-center gap-1 text-sm">
              <input type="checkbox" checked={isProposal} onChange={(e) => setIsProposal(e.target.checked)} />
              Propuesta
            </label>
          </div>
        </div>
        {isProposal && (
          <div className="mb-3">
            <label className="block text-sm font-medium">Estado de la propuesta</label>
            <select value={proposalStatus} onChange={(e) => setProposalStatus(e.target.value)} className="w-full border rounded p-2">
              <option value="open">Abierta</option>
              <option value="accepted">Aceptada</option>
              <option value="rejected">Rechazada</option>
            </select>
          </div>
        )}
        <div className="mb-4">
          <label className="block text-sm font-medium">Etiquetar usuarios</label>
          <div className="flex flex-wrap gap-2 mt-1">
            {profiles.filter(p => p.id !== currentUserId).map(profile => (
              <label key={profile.id} className="flex items-center gap-1 text-sm">
                <input
                  type="checkbox"
                  checked={selectedTags.includes(profile.id)}
                  onChange={(e) => {
                    if (e.target.checked) setSelectedTags([...selectedTags, profile.id])
                    else setSelectedTags(selectedTags.filter(id => id !== profile.id))
                  }}
                />
                {profile.display_name || profile.email}
              </label>
            ))}
          </div>
        </div>
        <div className="flex justify-end gap-3">
          <button onClick={onClose} className="px-4 py-2 border rounded">Cancelar</button>
          <button onClick={handleSave} className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Guardar</button>
        </div>
      </div>
    </div>
  )
}
