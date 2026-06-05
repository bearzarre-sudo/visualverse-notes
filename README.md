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

1. **Clona el repositorio** o genera la estructura con el script Python incluido:

   ```bash
   python generar_visualverse.py
   cd visualverse-notes