import { useNavigate } from 'react-router-dom'
import { formatDate } from '@/lib/utils'
import type { TimelineEvent } from '@/types'

interface Props {
  events: TimelineEvent[]
}

export function MovementTimeline({ events }: Props) {
  const navigate = useNavigate()

  if (events.length === 0) {
    return <div className="flex items-center justify-center h-64 text-gray-400">No movement events</div>
  }

  return (
    <div className="space-y-2 max-h-[600px] overflow-y-auto">
      {events.map((e) => (
        <div
          key={e.id}
          onClick={() => navigate(`/individuals/${e.individual_id}`)}
          className="p-3 rounded-lg bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer transition-colors"
        >
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">{e.individual_name}</span>
            <span className="text-xs text-gray-400">{formatDate(e.date)}</span>
          </div>
          <div className="text-xs text-gray-500 mt-1">
            {e.origin_firm && <span>{e.origin_title} at {e.origin_firm}</span>}
            {e.origin_firm && e.destination_firm && <span> → </span>}
            {e.destination_firm && <span>{e.destination_title} at {e.destination_firm}</span>}
          </div>
          {e.tags.length > 0 && (
            <div className="flex gap-1 mt-1">
              {e.tags.map((t) => (
                <span key={t} className="px-1.5 py-0.5 rounded text-xs bg-amber-100 dark:bg-amber-900/20 text-amber-700">
                  {t}
                </span>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
