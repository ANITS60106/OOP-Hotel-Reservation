import { Link } from 'react-router-dom'

export default function RoomCard({ room }) {
  return (
    <article className="room-card">
      <div className="room-card-top">
        <span className={`status-pill ${room.is_booked ? 'danger' : 'success'}`}>{room.status_label}</span>
        <span className="category-pill">{room.category.name}</span>
      </div>
      <h3>{room.title}</h3>
      <p>{room.summary}</p>
      <div className="room-meta">
        <span>{room.capacity} guests</span>
        <span>{room.room_size} m²</span>
        <span>{room.beds} bed</span>
      </div>
      <div className="room-card-bottom">
        <strong>${room.price_per_night}/night</strong>
        <Link to={`/rooms/${room.slug}`} className="button-link">Open</Link>
      </div>
    </article>
  )
}
