import { useEffect, useState } from 'react'
import api from '../lib/api'
import RoomCard from '../components/RoomCard'
import StatsGrid from '../components/StatsGrid'

export default function HomePage() {
  const [rooms, setRooms] = useState([])

  useEffect(() => {
    api.get('rooms/?featured=true').then((response) => setRooms(response.data)).catch(() => setRooms([]))
  }, [])

  return (
    <div className="page">
      <section className="hero">
        <div>
          <span className="eyebrow">Hotel booking system on Django</span>
          <h1>Fresh look, modern stack and no ancient chaos in the codebase</h1>
          <p>Full-stack project with JWT auth, booking flow, admin dashboard, reports and responsive interface.</p>
          <div className="hero-actions">
            <a className="button-link" href="/rooms">Browse rooms</a>
            <a className="ghost-link" href="/dashboard">Open dashboard</a>
          </div>
        </div>
        <div className="hero-panel">
          <div className="glass-card">
            <h3>What changed</h3>
            <ul>
              <li>React 19 + Vite frontend</li>
              <li>Django 5.2 backend</li>
              <li>DAO classes and reports</li>
              <li>Cleaner booking logic</li>
            </ul>
          </div>
        </div>
      </section>
      <StatsGrid />
      <section className="section-block">
        <div className="section-head">
          <div>
            <span className="eyebrow">Featured rooms</span>
            <h2>Rooms that look like they belong in a 2026 project</h2>
          </div>
        </div>
        <div className="room-grid">
          {rooms.length ? rooms.map((room) => <RoomCard key={room.id} room={room} />) : <div className="empty-state">No featured rooms yet. Add them in Django admin.</div>}
        </div>
      </section>
    </div>
  )
}
