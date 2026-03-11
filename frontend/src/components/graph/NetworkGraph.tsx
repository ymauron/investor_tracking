import { useCallback, useRef, useEffect } from 'react'
import ForceGraph2D from 'react-force-graph-2d'
import { useNavigate } from 'react-router-dom'
import { NODE_COLORS } from '@/lib/constants'
import type { GraphData, GraphNode } from '@/types'

interface Props {
  data: GraphData
  width: number
  height: number
}

export function NetworkGraph({ data, width, height }: Props) {
  const navigate = useNavigate()
  const fgRef = useRef<any>(null)

  useEffect(() => {
    if (fgRef.current) {
      fgRef.current.d3Force('charge').strength(-120)
      fgRef.current.d3Force('link').distance(60)
    }
  }, [data])

  const getNodeColor = useCallback((node: any) => {
    const n = node as GraphNode
    if (n.type === 'firm') {
      if (n.has_lp_commitment) return NODE_COLORS.lp_committed
      return NODE_COLORS[n.firm_type || 'other'] || NODE_COLORS.other
    }
    return NODE_COLORS.person
  }, [])

  const handleNodeClick = useCallback(
    (node: any) => {
      const n = node as GraphNode
      if (n.type === 'person') {
        navigate(`/individuals/${n.id.replace('person-', '')}`)
      } else if (n.type === 'firm') {
        navigate(`/firms/${n.id.replace('firm-', '')}`)
      }
    },
    [navigate]
  )

  const paintNode = useCallback(
    (node: any, ctx: CanvasRenderingContext2D) => {
      const n = node as GraphNode & { x: number; y: number }
      const size = n.type === 'firm' ? Math.max(4, Math.sqrt(n.val) * 3) : 3
      const color = getNodeColor(n)

      ctx.beginPath()
      if (n.type === 'firm') {
        // Square for firms
        ctx.rect(n.x - size, n.y - size, size * 2, size * 2)
      } else {
        // Circle for people
        ctx.arc(n.x, n.y, size, 0, 2 * Math.PI)
      }
      ctx.fillStyle = color
      ctx.fill()

      // Label
      if (n.type === 'firm' || n.val > 2) {
        ctx.font = `${n.type === 'firm' ? '3px' : '2.5px'} sans-serif`
        ctx.fillStyle = '#666'
        ctx.textAlign = 'center'
        ctx.fillText(n.name, n.x, n.y + size + 4)
      }
    },
    [getNodeColor]
  )

  return (
    <ForceGraph2D
      ref={fgRef}
      graphData={data}
      width={width}
      height={height}
      nodeCanvasObject={paintNode}
      nodePointerAreaPaint={(node: any, color, ctx) => {
        const n = node as GraphNode & { x: number; y: number }
        const size = n.type === 'firm' ? Math.max(6, Math.sqrt(n.val) * 4) : 5
        ctx.beginPath()
        ctx.arc(n.x, n.y, size, 0, 2 * Math.PI)
        ctx.fillStyle = color
        ctx.fill()
      }}
      linkColor={() => 'rgba(156, 163, 175, 0.3)'}
      linkWidth={(link: any) => (link.is_current ? 1.5 : 0.5)}
      linkDirectionalParticles={0}
      onNodeClick={handleNodeClick}
      cooldownTicks={100}
      enableNodeDrag={true}
      enableZoomInteraction={true}
      enablePanInteraction={true}
    />
  )
}
