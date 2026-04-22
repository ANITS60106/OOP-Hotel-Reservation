import { Link, NavLink } from 'react-router-dom'

export default function Layout({ children }) {
  return (
    <div className="app-shell">
      <header className="topbar">
        <Link className="brand" to="/">HotelFlow</Link>
        <nav className="navlinks">
          <NavLink to="/">Home</NavLink>
          <NavLink to="/rooms">Rooms</NavLink>
          <NavLink to="/login">Login</NavLink>
          <NavLink to="/register">Register</NavLink>
          <NavLink to="/dashboard">Dashboard</NavLink>
        </nav>
      </header>
      <main>{children}</main>
      <footer className="footer">
        <div>Modern Django Hotel Booking System</div>
        <div>Responsive UI, reports, dashboard and clean API</div>
      </footer>
    </div>
  )
}
