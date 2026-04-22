import { useEffect, useMemo, useState } from 'react'
import api from '../lib/api'
import RoomCard from '../components/RoomCard'

export default function RoomsPage() {
  const [rooms, setRooms] = useState([])
  const [search, setSearch] = useState('')
  const [price, setPrice] = useState(500)
  const [capacity, setCapacity] = useState(1)

  useEffect(() => {
    api.get('rooms/').then((response) => setRooms(response.data)).catch(() => setRooms([]))
  }, [])

  const filteredRooms = useMemo(() => rooms.filter((room) => room.title.toLowerCase().includes(search.toLowerCase()) && Number(room.price_per_night) <= price && room.capacity >= capacity), [rooms, search, price, capacity])

  return (
    <div className="page">
      <section className="section-block compact">
        <div className="section-head">
          <div>
            <span className="eyebrow">Catalog</span>
            <h1>Find a room without suffering</h1>
          </div>
        </div>
        <div className="filters">
          <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search by room name" />
          <input type="range" min="50" max="500" value={price} onChange={(event) => setPrice(Number(event.target.value))} />
          <select value={capacity} onChange={(event) => setCapacity(Number(event.target.value))}>
            <option value="1">1+ guest</option>
            <option value="2">2+ guests</option>
            <option value="3">3+ guests</option>
            <option value="4">4+ guests</option>
          </select>
        </div>
        <div className="helper-line">Max price: ${price} | Capacity: {capacity}+</div>
        <div className="room-grid">
          {filteredRooms.length ? filteredRooms.map((room) => <RoomCard key={room.id} room={room} />) : <div className="empty-state">Nothing found. Try another filter.</div>}
        </div>
      </section>
    </div>
  )
}
