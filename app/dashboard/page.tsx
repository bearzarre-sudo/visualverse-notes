'use client'
import { useEffect, useState, useCallback } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'
import Sidebar from './components/Sidebar'
import NotesList from './components/NotesList'
import NoteEditor from './components/NoteEditor'
import type { Section, Note, Profile } from '@/lib/types'

export default function DashboardPage() {
  const supabase = createClient()
  const router = useRouter()
  const [sections, setSections] = useState<Section[]>([])
  const [notes, setNotes] = useState<Note[]>([])
  const [profiles, setProfiles] = useState<Profile[]>([])
  const [selectedSectionId, setSelectedSectionId] = useState<string | null>(null)
  const [editingNote, setEditingNote] = useState<Note | null>(null)
  const [currentUser, setCurrentUser] = useState<Profile | null>(null)

  const fetchInitialData = useCallback(async () => {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) { router.push('/auth/login'); return }
    const { data: profile } = await supabase.from('profiles').select('*').eq('id', user.id).single()
    setCurrentUser(profile as Profile)

    const { data: sec } = await supabase.from('sections').select('*').order('order')
    setSections(sec || [])

    const { data: noteData } = await supabase.from('notes').select(`
      *,
      author:created_by(id, email, display_name),
      last_editor:last_edited_by(id, email, display_name)
    `).order('created_at', { ascending: false })
    setNotes(noteData || [])

    const { data: profs } = await supabase.from('profiles').select('*')
    setProfiles(profs || [])
  }, [supabase, router])

  useEffect(() => {
    fetchInitialData()
  }, [fetchInitialData])

  useEffect(() => {
    const sectionsChannel = supabase
      .channel('sections-changes')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'sections' }, (payload) => {
        fetchInitialData()
      })
      .subscribe()

    const notesChannel = supabase
      .channel('notes-changes')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'notes' }, (payload) => {
        fetchInitialData()
      })
      .subscribe()

    return () => {
      supabase.removeChannel(sectionsChannel)
      supabase.removeChannel(notesChannel)
    }
  }, [supabase, fetchInitialData])

  const handleLogout = async () => {
    await supabase.auth.signOut()
    router.push('/auth/login')
  }

  const handleCreateNote = () => {
    setEditingNote({
      id: '',
      section_id: selectedSectionId,
      title: '',
      content: '',
      is_completed: false,
      is_proposal: false,
      proposal_status: null,
      created_by: currentUser?.id || '',
      created_at: '',
      last_edited_by: null,
      last_edited_at: null,
    } as Note)
  }

  const handleSaveNote = async (note: Note, taggedUserIds: string[]) => {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    const noteData = {
      section_id: note.section_id,
      title: note.title,
      content: note.content,
      is_completed: note.is_completed,
      is_proposal: note.is_proposal,
      proposal_status: note.proposal_status,
      last_edited_by: user.id,
      last_edited_at: new Date().toISOString(),
      ...(note.id ? {} : { created_by: user.id }),
    }
    if (note.id) {
      await supabase.from('notes').update(noteData).eq('id', note.id)
    } else {
      const { data: newNote } = await supabase.from('notes').insert(noteData).select('id').single()
      note.id = newNote?.id
    }
    await supabase.from('note_tagged_users').delete().eq('note_id', note.id)
    const tagInserts = taggedUserIds.map(uid => ({ note_id: note.id, user_id: uid }))
    if (tagInserts.length > 0) {
      await supabase.from('note_tagged_users').insert(tagInserts)
    }
    setEditingNote(null)
  }

  const handleDeleteNote = async (noteId: string) => {
    await supabase.from('notes').delete().eq('id', noteId)
  }

  const handleViewNote = async (noteId: string) => {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    await supabase.from('note_views').upsert({ note_id: noteId, user_id: user.id, viewed_at: new Date().toISOString() }, { onConflict: 'note_id, user_id' })
  }

  return (
    <div className="flex h-screen">
      <Sidebar
        sections={sections}
        selectedSectionId={selectedSectionId}
        onSelectSection={setSelectedSectionId}
        onAddSection={async (title) => {
          await supabase.from('sections').insert({ title, order: sections.length })
        }}
        onDeleteSection={async (id) => {
          await supabase.from('sections').delete().eq('id', id)
        }}
        onLogout={handleLogout}
        currentUser={currentUser}
      />
      <main className="flex-1 overflow-auto p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">
            {selectedSectionId ? sections.find(s => s.id === selectedSectionId)?.title : 'Todas las notas'}
          </h2>
          <button
            onClick={handleCreateNote}
            className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          >
            Nueva nota
          </button>
        </div>
        <NotesList
          notes={notes.filter(n => !selectedSectionId || n.section_id === selectedSectionId)}
          onEdit={(note) => {
            handleViewNote(note.id)
            setEditingNote(note)
          }}
          onDelete={handleDeleteNote}
          onToggleComplete={async (id, completed) => {
            await supabase.from('notes').update({ is_completed: completed }).eq('id', id)
          }}
          currentUserId={currentUser?.id}
          profiles={profiles}
          onView={handleViewNote}
        />
      </main>
      {editingNote && (
        <NoteEditor
          note={editingNote}
          sections={sections}
          profiles={profiles}
          onSave={handleSaveNote}
          onClose={() => setEditingNote(null)}
          currentUserId={currentUser?.id!}
        />
      )}
    </div>
  )
}
