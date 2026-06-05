# VisualVerse Notes

Plataforma colaborativa de apuntes y propuestas, con autenticación segura, tiempo real y gestión de contenido multimedia. Pensada para equipos que necesitan una sala de ideas organizada por secciones, donde cada miembro puede ver quién editó, qué se propuso y quién lo ha revisado.

## Características principales

- **Autenticación obligatoria** – registro/inicio de sesión con email y contraseña mediante Supabase Auth.
- **Espacio de trabajo compartido** – todos los usuarios autenticados ven y editan las mismas notas.
- **Secciones** – agrupa las notas por temas o categorías.
- **Notas enriquecidas**:
  - Título y contenido Markdown (soporta imágenes, enlaces y videos de YouTube incrustados automáticamente).
  - Checkbox para marcar como completada.
  - Modo propuesta: cada nota puede ser una propuesta con estado (abierta, aceptada, rechazada).
  - Etiquetado de usuarios (multiselección).
  - Registro de última edición (usuario y fecha).
  - Visualización de quiénes han visto la nota.
- **Actualizaciones en tiempo real** – cualquier cambio en secciones, notas, etiquetas o vistas se sincroniza al instante con Supabase Realtime.
- **Interfaz limpia e intuitiva** – construida con Tailwind CSS, sin emojis ni distracciones.
- **Despliegue sencillo en Vercel** – configuración lista para producción.

## Tecnologías

- [Next.js 14](https://nextjs.org/) (App Router)
- [React 18](https://react.dev/)
- [TypeScript](https://www.typescriptlang.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Supabase](https://supabase.com/) – base de datos PostgreSQL, autenticación y Realtime.
- [React Markdown](https://github.com/remarkjs/react-markdown) para renderizar contenido.
- [Supabase SSR](https://supabase.com/docs/guides/auth/server-side/nextjs) para manejo de sesiones.

## Requisitos previos

- Node.js 18 o superior.
- Cuenta en [Supabase](https://supabase.com) con un proyecto creado.
- Cuenta en [Vercel](https://vercel.com) (para el despliegue).

## Configuración local

1. Clona el repositorio y entra en el proyecto:

  ```bash
  git clone https://github.com/bearzarre-sudo/visualverse-notes.git
  cd visualverse-notes
  ```

2. Instala dependencias:

  ```bash
  npm install
  ```

3. Crea tu archivo de entorno local `.env.local` con estas variables:

  ```bash
  NEXT_PUBLIC_SUPABASE_URL=https://TU-PROYECTO.supabase.co
  NEXT_PUBLIC_SUPABASE_ANON_KEY=TU_SUPABASE_ANON_KEY
  ```

4. Crea la base de datos en Supabase:

  - Abre el editor SQL de Supabase.
  - Ejecuta el script [Gnerador en python/Supa.sql](Gnerador%20en%20python/Supa.sql).

5. Inicia el servidor de desarrollo:

  ```bash
  npm run dev
  ```

6. Abre la app en `http://localhost:3000`.

## Scripts disponibles

- `npm run dev`: inicia Next.js en desarrollo.
- `npm run build`: compila para producción.
- `npm run start`: ejecuta el build de producción.

## Despliegue en Vercel

1. Importa el repositorio `bearzarre-sudo/visualverse-notes` en Vercel.
2. Agrega estas variables de entorno en el proyecto de Vercel:

  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

3. Ejecuta el despliegue.
4. Verifica que las URLs de autenticación en Supabase incluyan:

  - `https://TU-DOMINIO-VERCEL`
  - `https://TU-DOMINIO-VERCEL/auth/login`
  - `https://TU-DOMINIO-VERCEL/auth/signup`

## Protección de rama

La rama principal `main` está protegida para evitar cambios accidentales:

- Requiere Pull Request con al menos 1 aprobación.
- Bloquea `force push`.
- Bloquea eliminación de la rama.
- Requiere resolver conversaciones antes de merge.

## Estructura principal

- [app](app): rutas y layouts de la aplicación (App Router).
- [app/dashboard/components](app/dashboard/components): componentes del panel de notas.
- [lib/supabase](lib/supabase): clientes Supabase para browser, server y middleware.
- [Gnerador en python](Gnerador%20en%20python): script y SQL auxiliar para generación/configuración.

## Notas

- Si trabajas en Windows y detectas errores de memoria con `next dev`, puedes usar temporalmente:

  ```bash
  npm run dev -- --webpack
  ```

- Mantén `next-env.d.ts` versionado en el repositorio (comportamiento recomendado por Next.js).