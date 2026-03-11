import { useState, useEffect, useRef, useCallback } from 'react'
import { getNetworkGraph, getTimeline } from '@/api/graph'
import { listIndividuals } from '@/api/individuals'
import { NetworkGraph } from '@/components/graph/NetworkGraph'
import { GraphControls } from '@/components/graph/GraphControls'
import { MovementTimeline } from '@/components/timeline/MovementTimeline'
import { DirectoryTable } from '@/components/directory/DirectoryTable'
import { NODE_COLORS } from '@/lib/constants'
import type { GraphData, TimelineEvent, IndividualListItem } from '@/types'

type Tab = 'graph' | 'timeline' | 'directory'

export function DashboardPage() {
  const [tab, setTab] = useState<Tab>('graph')
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] })
  const [timelineEvents, setTimelineEvents] = useState<TimelineEvent[]>([])
  const [individuals, setIndividuals] = useState<IndividualListItem[]>([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    firmType: '',
    therapeuticArea: '',
    lpCommittedOnly: false,
  })
  const containerRef = useRef<HTMLDivElement>(null)
  const [dimensions, setDimensions] = useState({ width: 800, height: 500 })

  const loadData = useCallback(async () => {
    setLoading(true)
    try {
      const [graph, timeline, people] = await Promise.all([
        getNetworkGraph({
          firm_type: filters.firmType || undefined,
          therapeutic_area: filters.therapeuticArea || undefined,
          lp_committed_only: filters.lpCommittedOnly || undefined,
        }),
        getTimeline(),
        listIndividuals({ per_page: 100 }),
      ])
      setGraphData(graph)
      setTimelineEvents(timeline.events)
      setIndividuals(people)
    } finally {
      setLoading(false)
    }
  }, [filters])

  useEffect(() => {
    loadData()
  }, [loadData])

  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.clientWidth,
          height: Math.max(500, window.innerHeight - 280),
        })
      }
    }
    updateDimensions()
    window.addEventListener('resize', updateDimensions)
    return () => window.removeEventListener('resize', updateDimensions)
  }, [])

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold">Dashboard</h2>
        <div className="flex rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
          {(['graph', 'timeline', 'directory'] as Tab[]).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-1.5 text-sm font-medium transition-colors ${
                tab === t
                  ? 'bg-brand-600 text-white'
                  : 'bg-white dark:bg-gray-900 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800'
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {tab === 'graph' && (
        <>
          <div className="mb-3 flex items-center justify-between">
            <GraphControls filters={filters} onChange={setFilters} />
            <div className="flex items-center gap-3 text-xs text-gray-400">
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: NODE_COLORS.vc }} /> VC
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: NODE_COLORS.growth_equity }} /> Growth
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: NODE_COLORS.buyout }} /> Buyout
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: NODE_COLORS.lp_committed }} /> LP Committed
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: NODE_COLORS.person }} /> Person
              </span>
            </div>
          </div>
          <div
            ref={containerRef}
            className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden"
          >
            {loading ? (
              <div className="flex items-center justify-center h-[500px] text-gray-400">Loading graph...</div>
            ) : (
              <NetworkGraph data={graphData} width={dimensions.width} height={dimensions.height} />
            )}
          </div>
        </>
      )}

      {tab === 'timeline' && (
        <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-4">
          {loading ? (
            <div className="flex items-center justify-center h-64 text-gray-400">Loading...</div>
          ) : (
            <MovementTimeline events={timelineEvents} />
          )}
        </div>
      )}

      {tab === 'directory' && (
        <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
          <DirectoryTable individuals={individuals} loading={loading} />
        </div>
      )}
    </div>
  )
}
