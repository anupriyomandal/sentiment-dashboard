import { Influencer } from '@/types'
import { Badge } from '@/components/ui/badge'

export default function TopInfluencers({ influencers }: { influencers: Influencer[] }) {
  if (!influencers || influencers.length === 0) return <div className="p-4 text-muted-foreground">No influencers found.</div>

  const getBadgeVariant = (sentiment: string) => {
    if (sentiment === 'Positive') return 'positive'
    if (sentiment === 'Negative') return 'negative'
    return 'neutral'
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm text-left">
        <thead className="text-xs text-muted-foreground uppercase bg-muted/50 rounded-t-lg">
          <tr>
            <th className="px-4 py-3 font-medium">Username</th>
            <th className="px-4 py-3 font-medium text-right">Score</th>
            <th className="px-4 py-3 font-medium text-center">Leaning</th>
            <th className="px-4 py-3 font-medium text-right">Mentions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border">
          {influencers.map((inf) => (
            <tr key={inf.username} className="bg-card hover:bg-muted/30 transition-colors">
              <td className="px-4 py-3 font-medium">u/{inf.username}</td>
              <td className="px-4 py-3 text-right">{inf.influence_score}</td>
              <td className="px-4 py-3 text-center">
                <Badge variant={getBadgeVariant(inf.sentiment_leaning)}>{inf.sentiment_leaning}</Badge>
              </td>
              <td className="px-4 py-3 text-right">{inf.mentions}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
