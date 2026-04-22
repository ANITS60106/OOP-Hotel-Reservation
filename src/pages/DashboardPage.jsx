import { useEffect, useState } from 'react'
import api from '../lib/api'

export default function DashboardPage() {
  const [reports, setReports] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('dashboard/reports/').then((response) => setReports(response.data)).catch(() => setError('This page needs an admin account.'))
  }, [])

  if (error) {
    return <div className="page"><div className="notice error">{error}</div></div>
  }

  if (!reports) {
    return <div className="page"><div className="empty-state">Loading dashboard...</div></div>
  }

  return (
    <div className="page">
      <section className="section-block compact">
        <span className="eyebrow">Dashboard</span>
        <h1>Database reports</h1>
        <div className="stats-grid">
          {Object.entries(reports.summary).map(([key, value]) => (
            <div className="stat-card" key={key}>
              <h3>{String(value)}</h3>
              <p>{key}</p>
            </div>
          ))}
        </div>
        <div className="report-grid">
          {Object.entries(reports.reports).map(([key, value]) => (
            <article className="report-card" key={key}>
              <h2>{key}</h2>
              <pre>{JSON.stringify(value, null, 2)}</pre>
            </article>
          ))}
        </div>
      </section>
    </div>
  )
}
