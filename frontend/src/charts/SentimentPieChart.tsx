import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts'
import { SentimentSummary } from '@/types'

const COLORS = {
  Positive: '#009F6B', // CEAT Green
  Neutral: '#8C92AC',  // CEAT Grey
  Negative: '#DA291C'  // CEAT Red
}

export default function SentimentPieChart({ data }: { data: SentimentSummary | null }) {
  if (!data) return <div className="h-[300px] flex items-center justify-center">Loading...</div>

  const chartData = [
    { name: 'Positive', value: data.positive_count },
    { name: 'Neutral', value: data.neutral_count },
    { name: 'Negative', value: data.negative_count },
  ].filter(item => item.value > 0);

  if (chartData.length === 0) return <div className="h-[300px] flex items-center justify-center">No data available</div>

  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={90}
            paddingAngle={5}
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[entry.name as keyof typeof COLORS]} />
            ))}
          </Pie>
          <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
          <Legend verticalAlign="bottom" height={36} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
