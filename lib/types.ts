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
