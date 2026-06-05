-- Habilitar extensión para gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Tabla de perfiles (se llena automáticamente al registrarse)
CREATE TABLE public.profiles (
  id uuid REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  email text UNIQUE NOT NULL,
  display_name text,
  avatar_url text,
  created_at timestamptz DEFAULT now()
);

-- Trigger para crear perfil al registrarse
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id, email, display_name)
  VALUES (new.id, new.email, new.raw_user_meta_data->>'display_name');
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Secciones
CREATE TABLE public.sections (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  title text NOT NULL,
  "order" integer DEFAULT 0,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Notas
CREATE TABLE public.notes (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  section_id uuid REFERENCES public.sections ON DELETE SET NULL,
  title text NOT NULL DEFAULT '',
  content text DEFAULT '',
  is_completed boolean DEFAULT false,
  is_proposal boolean DEFAULT false,
  proposal_status text CHECK (proposal_status IN ('open', 'accepted', 'rejected')),
  created_by uuid REFERENCES public.profiles NOT NULL,
  created_at timestamptz DEFAULT now(),
  last_edited_by uuid REFERENCES public.profiles,
  last_edited_at timestamptz DEFAULT now()
);

-- Etiquetado de usuarios en notas
CREATE TABLE public.note_tagged_users (
  note_id uuid REFERENCES public.notes ON DELETE CASCADE,
  user_id uuid REFERENCES public.profiles ON DELETE CASCADE,
  PRIMARY KEY (note_id, user_id)
);

-- Vistas de notas (quién ha visto qué)
CREATE TABLE public.note_views (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  note_id uuid REFERENCES public.notes ON DELETE CASCADE,
  user_id uuid REFERENCES public.profiles ON DELETE CASCADE,
  viewed_at timestamptz DEFAULT now(),
  UNIQUE (note_id, user_id)
);

-- Políticas de seguridad (solo usuarios autenticados)
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sections ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.note_tagged_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.note_views ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Usuarios autenticados pueden leer perfiles" ON public.profiles FOR SELECT TO authenticated USING (true);
CREATE POLICY "Usuarios autenticados pueden actualizar su perfil" ON public.profiles FOR UPDATE TO authenticated USING (id = auth.uid());

CREATE POLICY "Autenticados pueden leer secciones" ON public.sections FOR SELECT TO authenticated USING (true);
CREATE POLICY "Autenticados pueden insertar secciones" ON public.sections FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Autenticados pueden eliminar secciones" ON public.sections FOR DELETE TO authenticated USING (true);

CREATE POLICY "Autenticados pueden leer notas" ON public.notes FOR SELECT TO authenticated USING (true);
CREATE POLICY "Autenticados pueden insertar notas" ON public.notes FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Autenticados pueden actualizar notas" ON public.notes FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Autenticados pueden eliminar notas" ON public.notes FOR DELETE TO authenticated USING (true);

CREATE POLICY "Autenticados pueden leer etiquetados" ON public.note_tagged_users FOR SELECT TO authenticated USING (true);
CREATE POLICY "Autenticados pueden insertar etiquetados" ON public.note_tagged_users FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Autenticados pueden eliminar etiquetados" ON public.note_tagged_users FOR DELETE TO authenticated USING (true);

CREATE POLICY "Autenticados pueden leer vistas" ON public.note_views FOR SELECT TO authenticated USING (true);
CREATE POLICY "Autenticados pueden insertar vistas" ON public.note_views FOR INSERT TO authenticated WITH CHECK (true);

-- Habilitar realtime para las tablas necesarias
BEGIN;
  ALTER PUBLICATION supabase_realtime ADD TABLE public.sections;
  ALTER PUBLICATION supabase_realtime ADD TABLE public.notes;
  ALTER PUBLICATION supabase_realtime ADD TABLE public.note_tagged_users;
  ALTER PUBLICATION supabase_realtime ADD TABLE public.note_views;
COMMIT;