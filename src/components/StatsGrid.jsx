export default function StatsGrid() {
  const items = [
    { value: '24/7', label: 'Fast booking flow' },
    { value: '5', label: 'Database reports' },
    { value: 'JWT', label: 'Secure auth' },
    { value: 'MVC', label: 'Clean architecture' }
  ]

  return (
    <section className="stats-grid">
      {items.map((item) => (
        <div key={item.label} className="stat-card">
          <h3>{item.value}</h3>
          <p>{item.label}</p>
        </div>
      ))}
    </section>
  )
}
