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
