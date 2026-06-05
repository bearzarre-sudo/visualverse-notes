#!/usr/bin/env python3
"""
Generador del proyecto VisualVerse Notes
Ejecutar: python VisualVerseNotes.py
"""

import os

# Contenido de cada archivo
files = {
    ".env.local.example": """\
NEXT_PUBLIC_SUPABASE_URL=https://tu-proyecto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=tu-anon-key
""",
    "package.json": r'''{
  "name": "visualverse-notes",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "@supabase/ssr": "^0.5.2",
    "@supabase/supabase-js": "^2.45.0",
    "next": "14.2.15",
    "react": "^18",
    "react-dom": "^18",
    "react-markdown": "^9.0.1",
    "react-select": "^5.8.0",
    "tailwindcss": "^3.4.13",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "typescript": "^5"
  }
}
''',
    "next.config.js": """\
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: '**' }
    ]
  }
}
module.exports = nextConfig
""",
    "tailwind.config.ts": """\
import type { Config } from 'tailwindcss'
const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: { extend: {} },
  plugins: [],
}
export default config
""",
    "postcss.config.js": """\
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""",
    "tsconfig.json": r'''{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
''',
    "middleware.ts": """\
import { updateSession } from '@/lib/supabase/middleware'
import type { NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  return await updateSession(request)
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
""",
    "app/globals.css": """\
@tailwind base;
@tailwind components;
@tailwind utilities;
""",
    "app/layout.tsx": """\
import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'VisualVerse Notes',
  description: 'Sala de ideas colaborativa',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body className="min-h-screen bg-gray-50 text-gray-900">{children}</body>
    </html>
  )
}
""",
    "app/page.tsx": """\
import { createServerClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function Home() {
  const supabase = createServerClient()
  const { data: { session } } = await supabase.auth.getSession()
  redirect(session ? '/dashboard' : '/auth/login')
}
""",
    "app/auth/login/page.tsx": """\
'use client'
import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter()
  const supabase = createClient()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    setLoading(false)
    if (error) {
      setError(error.message)
    } else {
      router.push('/dashboard')
      router.refresh()
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      <form onSubmit={handleLogin} className="w-full max-w-md space-y-4 rounded bg-white p-8 shadow">
        <h1 className="text-2xl font-bold">Iniciar sesion</h1>
        {error && <p className="text-red-500">{error}</p>}
        <input
          type="email"
          placeholder="Correo electronico"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full rounded border p-2"
          required
        />
        <input
          type="password"
          placeholder="Contrasena"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full rounded border p-2"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded bg-blue-600 p-2 text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Entrando...' : 'Entrar'}
        </button>
        <p className="text-center text-sm">
          No tienes cuenta? <Link href="/auth/signup" className="text-blue-600">Registrate</Link>
        </p>
      </form>
    </div>
  )
}
""",
    "app/auth/signup/page.tsx": """\
'use client'
import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function SignupPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [displayName, setDisplayName] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter()
  const supabase = createClient()

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: { display_name: displayName },
      },
    })
    setLoading(false)
    if (error) {
      setError(error.message)
    } else {
      router.push('/dashboard')
      router.refresh()
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      <form onSubmit={handleSignup} className="w-full max-w-md space-y-4 rounded bg-white p-8 shadow">
        <h1 className="text-2xl font-bold">Registrarse</h1>
        {error && <p className="text-red-500">{error}</p>}
        <input
          type="text"
          placeholder="Nombre visible"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          className="w-full rounded border p-2"
          required
        />
        <input
          type="email"
          placeholder="Correo electronico"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full rounded border p-2"
          required
        />
        <input
          type="password"
          placeholder="Contrasena"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full rounded border p-2"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded bg-blue-600 p-2 text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Creando cuenta...' : 'Crear cuenta'}
        </button>
        <p className="text-center text-sm">
          Ya tienes cuenta? <Link href="/auth/login" className="text-blue-600">Inicia sesion</Link>
        </p>
      </form>
    </div>
  )
}
""",
    "app/dashboard/layout.tsx": """\
import { createServerClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  const supabase = createServerClient()
  const { data: { session } } = await supabase.auth.getSession()
  if (!session) {
    redirect('/auth/login')
  }
  return <>{children}</>
}
""",
    "app/dashboard/page.tsx": """\
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
""",
    "app/dashboard/components/Sidebar.tsx": """\
'use client'
import { useState } from 'react'
import type { Section, Profile } from '@/lib/types'

interface Props {
  sections: Section[]
  selectedSectionId: string | null
  onSelectSection: (id: string | null) => void
  onAddSection: (title: string) => void
  onDeleteSection: (id: string) => void
  onLogout: () => void
  currentUser: Profile | null
}

export default function Sidebar({ sections, selectedSectionId, onSelectSection, onAddSection, onDeleteSection, onLogout, currentUser }: Props) {
  const [newTitle, setNewTitle] = useState('')

  const handleAdd = () => {
    if (newTitle.trim()) {
      onAddSection(newTitle.trim())
      setNewTitle('')
    }
  }

  return (
    <aside className="w-64 bg-gray-800 text-white flex flex-col p-4">
      <h1 className="text-lg font-bold mb-4">VisualVerse Notes</h1>
      <button onClick={() => onSelectSection(null)} className={`text-left px-2 py-1 rounded mb-2 ${!selectedSectionId ? 'bg-blue-600' : 'hover:bg-gray-700'}`}>
        Todas las notas
      </button>
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          placeholder="Nueva seccion"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          className="flex-1 rounded px-2 py-1 text-black"
        />
        <button onClick={handleAdd} className="bg-blue-600 px-2 rounded">+</button>
      </div>
      <ul className="flex-1 space-y-1 overflow-auto">
        {sections.map(section => (
          <li key={section.id} className="flex justify-between items-center group">
            <button
              onClick={() => onSelectSection(section.id)}
              className={`flex-1 text-left px-2 py-1 rounded ${selectedSectionId === section.id ? 'bg-blue-600' : 'hover:bg-gray-700'}`}
            >
              {section.title}
            </button>
            <button
              onClick={() => onDeleteSection(section.id)}
              className="text-red-400 opacity-0 group-hover:opacity-100 px-1"
            >
              X
            </button>
          </li>
        ))}
      </ul>
      <div className="mt-4 border-t border-gray-600 pt-4">
        <p className="text-sm">{currentUser?.display_name || currentUser?.email}</p>
        <button onClick={onLogout} className="text-sm text-red-400 hover:underline">Cerrar sesion</button>
      </div>
    </aside>
  )
}
""",
    "app/dashboard/components/NotesList.tsx": """\
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
""",
    "app/dashboard/components/NoteCard.tsx": """\
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
    /(?:https?:\\/\\/)?(?:www\\.)?(?:youtube\\.com\\/watch\\?v=|youtu\\.be\\/)([\\w-]+)/g,
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
""",
    "app/dashboard/components/NoteEditor.tsx": """\
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
""",
    "lib/types.ts": """\
export interface Profile {
  id: string
  email: string
  display_name: string | null
  avatar_url: string | null
}

export interface Section {
  id: string
  title: string
  order: number
  created_at: string
  updated_at: string
}

export interface Note {
  id: string
  section_id: string | null
  title: string
  content: string
  is_completed: boolean
  is_proposal: boolean
  proposal_status: 'open' | 'accepted' | 'rejected' | null
  created_by: string
  created_at: string
  last_edited_by: string | null
  last_edited_at: string | null
  tagged_users?: Profile[]
  viewers?: Profile[]
  author?: Profile
  last_editor?: Profile
}
""",
    "lib/supabase/client.ts": """\
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
""",
    "lib/supabase/server.ts": """\
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export function createServerClient() {
  const cookieStore = cookies()
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options)
          )
        },
      },
    }
  )
}
""",
    "lib/supabase/middleware.ts": """\
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request })
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            request.cookies.set(name, value)
          )
          supabaseResponse = NextResponse.next({ request })
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          )
        },
      },
    }
  )
  await supabase.auth.getUser()
  return supabaseResponse
}
""",
}

def create_project():
    base_dir = "visualverse-notes"
    print(f"Creando proyecto en '{base_dir}'...")
    os.makedirs(base_dir, exist_ok=True)
    for filepath, content in files.items():
        full_path = os.path.join(base_dir, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Creado: {filepath}")
    print("\nProyecto generado exitosamente.")
    print("Siguientes pasos:")
    print("  1. cd visualverse-notes")
    print("  2. npm install")
    print("  3. Copia .env.local.example a .env.local y completa tus credenciales de Supabase")
    print("  4. Ejecuta el SQL proporcionado en Supabase para crear las tablas y políticas")
    print("  5. npm run dev")

if __name__ == "__main__":
    create_project()