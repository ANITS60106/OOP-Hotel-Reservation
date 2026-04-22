import { useState } from 'react'
import { authApi } from '../lib/api'

export default function RegisterPage() {
  const [form, setForm] = useState({ username: '', email: '', password: '', password2: '' })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const handleChange = (event) => setForm((previous) => ({ ...previous, [event.target.name]: event.target.value }))

  const handleSubmit = async (event) => {
    event.preventDefault()
    setMessage('')
    setError('')
    try {
      await authApi.post('register/', form)
      setMessage('Account created successfully.')
      setForm({ username: '', email: '', password: '', password2: '' })
    } catch (submissionError) {
      const data = submissionError.response?.data
      setError(typeof data === 'string' ? data : JSON.stringify(data))
    }
  }

  return (
    <div className="page narrow-page">
      <section className="form-card">
        <span className="eyebrow">Auth</span>
        <h1>Register</h1>
        <form className="booking-form" onSubmit={handleSubmit}>
          <input name="username" placeholder="Username" value={form.username} onChange={handleChange} required />
          <input name="email" type="email" placeholder="Email" value={form.email} onChange={handleChange} required />
          <input name="password" type="password" placeholder="Password" value={form.password} onChange={handleChange} required />
          <input name="password2" type="password" placeholder="Repeat password" value={form.password2} onChange={handleChange} required />
          <button type="submit">Create account</button>
        </form>
        {message ? <div className="notice success">{message}</div> : null}
        {error ? <div className="notice error">{error}</div> : null}
      </section>
    </div>
  )
}
