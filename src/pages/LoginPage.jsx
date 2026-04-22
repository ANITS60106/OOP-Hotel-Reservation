import { useState } from 'react'
import { authApi } from '../lib/api'

export default function LoginPage() {
  const [form, setForm] = useState({ username: '', password: '' })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const handleChange = (event) => setForm((previous) => ({ ...previous, [event.target.name]: event.target.value }))

  const handleSubmit = async (event) => {
    event.preventDefault()
    setMessage('')
    setError('')
    try {
      const response = await authApi.post('login/', form)
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
      localStorage.setItem('username', response.data.username)
      localStorage.setItem('is_admin', String(response.data.is_admin))
      setMessage('Logged in successfully.')
    } catch {
      setError('Wrong username or password.')
    }
  }

  return (
    <div className="page narrow-page">
      <section className="form-card">
        <span className="eyebrow">Auth</span>
        <h1>Login</h1>
        <form className="booking-form" onSubmit={handleSubmit}>
          <input name="username" placeholder="Username" value={form.username} onChange={handleChange} required />
          <input name="password" type="password" placeholder="Password" value={form.password} onChange={handleChange} required />
          <button type="submit">Login</button>
        </form>
        {message ? <div className="notice success">{message}</div> : null}
        {error ? <div className="notice error">{error}</div> : null}
      </section>
    </div>
  )
}
