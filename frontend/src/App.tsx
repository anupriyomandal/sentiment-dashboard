import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import SentimentPieChart from '@/charts/SentimentPieChart'
import MentionsLineChart from '@/charts/MentionsLineChart'
import TopPosts from '@/components/TopPosts'
import TopInfluencers from '@/components/TopInfluencers'
import ResponseAgent from '@/components/ResponseAgent'
import { SentimentSummary, SentimentTrend, Post, Influencer } from '@/types'
import { Activity, Users, MessageCircle, BarChart3, Moon, Sun } from 'lucide-react'
import { Button } from '@/components/ui/button'

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

export default function App() {
  const [summary, setSummary] = useState<SentimentSummary | null>(null)
  const [trends, setTrends] = useState<SentimentTrend[]>([])
  const [topPosts, setTopPosts] = useState<Post[]>([])
  const [influencers, setInfluencers] = useState<Influencer[]>([])
  const [darkMode, setDarkMode] = useState(false)

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
    document.documentElement.classList.toggle('dark')
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [sumRes, trendRes, postRes, infRes] = await Promise.all([
          fetch(`${API_URL}/api/sentiment-summary`),
          fetch(`${API_URL}/api/sentiment-over-time`),
          fetch(`${API_URL}/api/top-posts`),
          fetch(`${API_URL}/api/top-influencers`)
        ])
        if(sumRes.ok) setSummary(await sumRes.json())
        if(trendRes.ok) setTrends(await trendRes.json())
        if(postRes.ok) setTopPosts(await postRes.json())
        if(infRes.ok) setInfluencers(await infRes.json())
      } catch (e) {
        console.error("Error fetching dashboard data", e)
      }
    }
    fetchData()
  }, [])

  return (
    <div className="min-h-screen pb-12 transition-colors duration-300">
      <header className="sticky top-0 z-10 glass border-b shadow-sm mb-8 px-6 py-4 flex justify-between items-center bg-white/70 dark:bg-black/70 backdrop-blur-xl">
        <div className="flex items-center space-x-3">
          <div className="bg-ceat-green text-white p-2 rounded-lg shadow-lg">
            <Activity className="w-6 h-6" />
          </div>
          <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-ceat-green to-ceat-grey bg-clip-text text-transparent">Anupriyo Mandal's Sentiments Intelligence</h1>
        </div>
        <Button variant="ghost" size="icon" onClick={toggleDarkMode} className="rounded-full">
          {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
        </Button>
      </header>

      <main className="container mx-auto px-4 lg:px-8 space-y-8 max-w-7xl animate-in fade-in slide-in-from-bottom-8 duration-500">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Section 1: Sentiment Overview */}
          <Card className="lg:col-span-1 border-t-4 border-t-ceat-green hover:shadow-lg transition-shadow">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center text-lg">
                <BarChart3 className="w-5 h-5 mr-2 text-muted-foreground" />
                Sentiment Overview
              </CardTitle>
            </CardHeader>
            <CardContent>
              <SentimentPieChart data={summary} />
            </CardContent>
          </Card>

          {/* Section 2: Mentions Over Time */}
          <Card className="lg:col-span-2 border-t-4 border-t-ceat-grey hover:shadow-lg transition-shadow">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center text-lg">
                <Activity className="w-5 h-5 mr-2 text-muted-foreground" />
                Mentions Over Time
              </CardTitle>
            </CardHeader>
            <CardContent>
              <MentionsLineChart data={trends} />
            </CardContent>
          </Card>
        </div>

        {/* Section 7: Response Suggestion Agent */}
        <div>
          <ResponseAgent apiUrl={API_URL} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Section 3: Top Posts */}
          <Card className="border-t-4 border-t-ceat-red h-[600px] flex flex-col hover:shadow-lg transition-shadow">
            <CardHeader className="pb-2 border-b mb-4 shrink-0">
              <CardTitle className="flex items-center text-lg">
                <MessageCircle className="w-5 h-5 mr-2 text-muted-foreground" />
                Top Posts Mentioning CEAT
              </CardTitle>
            </CardHeader>
            <CardContent className="overflow-y-auto flex-1 pr-2">
              <TopPosts posts={topPosts} />
            </CardContent>
          </Card>

          {/* Section 4: Top Influencers */}
          <Card className="border-t-4 border-t-ceat-green h-[600px] flex flex-col hover:shadow-lg transition-shadow">
            <CardHeader className="pb-2 border-b mb-4 shrink-0">
              <CardTitle className="flex items-center text-lg">
                <Users className="w-5 h-5 mr-2 text-muted-foreground" />
                Top Influencers
              </CardTitle>
            </CardHeader>
            <CardContent className="overflow-y-auto flex-1 px-0 mx-6">
              <TopInfluencers influencers={influencers} />
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
