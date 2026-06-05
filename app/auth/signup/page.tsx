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
