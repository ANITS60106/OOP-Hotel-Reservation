import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../lib/api'

export default function RoomDetailsPage() {
  const { slug } = useParams()
  const [room, setRoom] = useState(null)
  const [form, setForm] = useState({ guest_name: '', email: '', phone_number: '', check_in: '', check_out: '', guests: 1, special_request: '' })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    api.get(`rooms/${slug}/`).then((response) => setRoom(response.data)).catch(() => setRoom(null))
  }, [slug])

  const handleChange = (event) => setForm((previous) => ({ ...previous, [event.target.name]: event.target.value }))

  const handleSubmit = async (event) => {
    event.preventDefault()
    setMessage('')
    setError('')
    try {
      await api.post('bookings/', { ...form, room: room.id, guests: Number(form.guests) })
      setMessage('Booking created. Nice.')
    } catch (submissionError) {
      const data = submissionError.response?.data
      setError(typeof data === 'string' ? data : JSON.stringify(data))
    }
  }

  if (!room) {
    return <div className="page"><div className="empty-state">Room not found.</div></div>
  }

  return (
    <div className="page">
      <section className="details-layout">
        <article className="details-card">
          <span className="eyebrow">{room.category.name}</span>
          <h1>{room.title}</h1>
          <p>{room.description}</p>
          <div className="room-meta large">
            <span>{room.capacity} guests</span>
            <span>{room.room_size} m²</span>
            <span>{room.beds} bed</span>
            <span>{room.bathrooms} bathroom</span>
          </div>
          <div className="amenity-wrap">
            {room.amenities.length ? room.amenities.map((item) => <span key={item.id} className="category-pill">{item.name}</span>) : <span className="category-pill">Amenities can be added in admin</span>}
          </div>
          <strong className="price-big">${room.price_per_night}/night</strong>
        </article>
        <article className="booking-card">
          <h2>Book this room</h2>
          <form className="booking-form" onSubmit={handleSubmit}>
            <input name="guest_name" placeholder="Guest name" value={form.guest_name} onChange={handleChange} required />
            <input name="email" type="email" placeholder="Email" value={form.email} onChange={handleChange} required />
            <input name="phone_number" placeholder="Phone number" value={form.phone_number} onChange={handleChange} required />
            <input name="check_in" type="date" value={form.check_in} onChange={handleChange} required />
            <input name="check_out" type="date" value={form.check_out} onChange={handleChange} required />
            <input name="guests" type="number" min="1" max={room.capacity} value={form.guests} onChange={handleChange} required />
            <textarea name="special_request" placeholder="Special request" value={form.special_request} onChange={handleChange} />
            <button type="submit">Create booking</button>
          </form>
          {message ? <div className="notice success">{message}</div> : null}
          {error ? <div className="notice error">{error}</div> : null}
          {!localStorage.getItem('access_token') ? <div className="notice error">You need to login first, otherwise the API will reject the booking.</div> : null}
        </article>
      </section>
    </div>
  )
}
