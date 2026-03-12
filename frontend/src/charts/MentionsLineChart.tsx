import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { SentimentTrend } from '@/types'

export default function MentionsLineChart({ data }: { data: SentimentTrend[] }) {
  if (!data || data.length === 0) return <div className="h-[300px] flex items-center justify-center">Loading trends...</div>

  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" opacity={0.2} vertical={false} />
          <XAxis dataKey="date" tick={{fontSize: 12}} tickMargin={10} axisLine={false} />
          <YAxis tick={{fontSize: 12}} axisLine={false} tickLine={false} />
          <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
          <Legend verticalAlign="top" height={36} />
          <Line type="monotone" dataKey="Positive" stroke="#009F6B" strokeWidth={3} dot={{r: 4}} activeDot={{r: 6}} />
          <Line type="monotone" dataKey="Neutral" stroke="#8C92AC" strokeWidth={3} dot={{r: 4}} activeDot={{r: 6}} />
          <Line type="monotone" dataKey="Negative" stroke="#DA291C" strokeWidth={3} dot={{r: 4}} activeDot={{r: 6}} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
