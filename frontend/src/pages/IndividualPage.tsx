import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { ArrowLeft, ExternalLink, Mail, Phone } from 'lucide-react'
import { getIndividual, getIndividualRoles, getIndividualMovements, getIndividualNotes } from '@/api/individuals'
import { formatArea, formatDate } from '@/lib/utils'
import type { Individual, Role, MovementEvent, Note } from '@/types'

export function IndividualPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [individual, setIndividual] = useState<Individual | null>(null)
  const [roles, setRoles] = useState<Role[]>([])
  const [movements, setMovements] = useState<MovementEvent[]>([])
  const [notes, setNotes] = useState<Note[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    Promise.all([
      getIndividual(id),
      getIndividualRoles(id),
      getIndividualMovements(id),
      getIndividualNotes(id),
    ]).then(([ind, r, m, n]) => {
      setIndividual(ind)
      setRoles(r)
      setMovements(m)
      setNotes(n)
    }).finally(() => setLoading(false))
  }, [id])

  if (loading || !individual) {
    return <div className="flex items-center justify-center h-64 text-gray-400">Loading...</div>
  }

  return (
    <div className="max-w-4xl">
      <button onClick={() => navigate(-1)} className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-700 mb-4">
        <ArrowLeft size={14} /> Back
      </button>

      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 mb-4">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-xl font-bold">{individual.first_name} {individual.last_name}</h2>
            {individual.primary_therapeutic_area && (
              <span className="inline-flex mt-1 px-2.5 py-0.5 rounded-full text-xs bg-brand-50 dark:bg-brand-900/20 text-brand-700 dark:text-brand-300">
                {formatArea(individual.primary_therapeutic_area)}
              </span>
            )}
            {individual.relationship_status && (
              <span className="inline-flex mt-1 ml-2 px-2.5 py-0.5 rounded-full text-xs bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400">
                {individual.relationship_status}
              </span>
            )}
          </div>
          <div className="flex items-center gap-3 text-sm text-gray-500">
            {individual.email && (
              <a href={`mailto:${individual.email}`} className="hover:text-gray-700 flex items-center gap-1">
                <Mail size={14} /> {individual.email}
              </a>
            )}
            {individual.linkedin_url && (
              <a href={individual.linkedin_url} target="_blank" rel="noopener" className="hover:text-gray-700 flex items-center gap-1">
                <ExternalLink size={14} /> LinkedIn
              </a>
            )}
            {individual.phone && (
              <span className="flex items-center gap-1"><Phone size={14} /> {individual.phone}</span>
            )}
          </div>
        </div>

        {individual.personal_notes && (
          <p className="mt-3 text-sm text-gray-600 dark:text-gray-400">{individual.personal_notes}</p>
        )}
      </div>

      {/* Education */}
      {individual.education.length > 0 && (
        <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 mb-4">
          <h3 className="text-sm font-semibold mb-3">Education</h3>
          <div className="space-y-2">
            {individual.education.map((edu) => (
              <div key={edu.id} className="text-sm">
                <span className="font-medium">{edu.institution}</span>
                <span className="text-gray-500"> — {edu.degree_type.toUpperCase()}</span>
                {edu.field_of_study && <span className="text-gray-500">, {edu.field_of_study}</span>}
                {edu.graduation_year && <span className="text-gray-400"> ({edu.graduation_year})</span>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Roles */}
      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 mb-4">
        <h3 className="text-sm font-semibold mb-3">Career History</h3>
        {roles.length === 0 ? (
          <p className="text-sm text-gray-400">No roles recorded</p>
        ) : (
          <div className="space-y-3">
            {roles.map((role) => (
              <div key={role.id} className="flex items-start justify-between text-sm">
                <div>
                  <span className="font-medium">{role.title}</span>
                  {role.management_company_id && (
                    <Link to={`/firms/${role.management_company_id}`} className="text-brand-600 hover:underline ml-1">
                      (View Firm)
                    </Link>
                  )}
                  {role.is_current && (
                    <span className="ml-2 px-1.5 py-0.5 rounded text-xs bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400">
                      Current
                    </span>
                  )}
                </div>
                <span className="text-gray-400 text-xs">
                  {role.start_date ? formatDate(role.start_date) : '?'}
                  {' — '}
                  {role.is_current ? 'Present' : role.end_date ? formatDate(role.end_date) : '?'}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Movement Events */}
      {movements.length > 0 && (
        <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 mb-4">
          <h3 className="text-sm font-semibold mb-3">Movement Events</h3>
          <div className="space-y-3">
            {movements.map((m) => (
              <div key={m.id} className="text-sm border-l-2 border-brand-300 pl-3">
                <div className="flex items-center gap-2">
                  <span className="font-medium">
                    {m.move_type === 'external' ? 'External Move' : 'Internal Move'}
                  </span>
                  {m.is_spinout && (
                    <span className="px-1.5 py-0.5 rounded text-xs bg-purple-100 dark:bg-purple-900/20 text-purple-700">Spinout</span>
                  )}
                  <span className="px-1.5 py-0.5 rounded text-xs bg-gray-100 dark:bg-gray-800 text-gray-500">
                    {m.confidence}
                  </span>
                </div>
                {m.reason && <p className="text-gray-500 mt-0.5">{m.reason}</p>}
                <div className="flex items-center gap-3 text-xs text-gray-400 mt-1">
                  {m.departure_date && <span>Left: {formatDate(m.departure_date)}</span>}
                  {m.joining_date && <span>Joined: {formatDate(m.joining_date)}</span>}
                  {m.source_of_intel && <span>Source: {m.source_of_intel}</span>}
                </div>
                {m.tags.length > 0 && (
                  <div className="flex gap-1 mt-1">
                    {m.tags.map((t) => (
                      <span key={t} className="px-1.5 py-0.5 rounded text-xs bg-amber-100 dark:bg-amber-900/20 text-amber-700">
                        {t}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Notes */}
      {notes.length > 0 && (
        <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6">
          <h3 className="text-sm font-semibold mb-3">Notes</h3>
          <div className="space-y-2">
            {notes.map((n) => (
              <div key={n.id} className="text-sm p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <p>{n.content}</p>
                <p className="text-xs text-gray-400 mt-1">{formatDate(n.created_at)}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
