import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Suggestion } from '@/types'
import { Bot, RefreshCw } from 'lucide-react'

export default function ResponseAgent({ apiUrl }: { apiUrl: string }) {
  const [suggestions, setSuggestions] = useState<Suggestion[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchSuggestions = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${apiUrl}/api/generate-response-suggestions`, { method: 'POST' })
      if (!res.ok) throw new Error("Failed to generate responses")
      const data = await res.json()
      setSuggestions(data)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="glass border-ceat-green/30">
      <CardHeader className="pb-3 border-b border-border/50 bg-muted/10">
        <div className="flex justify-between items-center">
          <CardTitle className="text-lg flex items-center">
            <Bot className="w-5 h-5 mr-2 text-ceat-green" />
            Response Suggestion Agent
          </CardTitle>
          <Button onClick={fetchSuggestions} disabled={loading} size="sm" className="bg-ceat-green hover:bg-ceat-green/90 text-white">
            {loading ? <RefreshCw className="w-4 h-4 mr-2 animate-spin" /> : null}
            Generate Response Suggestions
          </Button>
        </div>
      </CardHeader>
      <CardContent className="pt-4">
        {error && <div className="text-destructive text-sm mb-4">{error}</div>}
        
        {suggestions.length === 0 && !loading && !error && (
          <p className="text-sm text-muted-foreground py-2 text-center">
            Click generate to analyze negative posts and brainstorm professional brand replies.
          </p>
        )}

        <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
          {suggestions.map((s, i) => (
            <div key={i} className="bg-muted/50 p-4 rounded-lg text-sm space-y-3">
              <p className="font-semibold text-foreground">Post Issue: <span className="font-normal text-muted-foreground">{s.post_title}</span></p>
              <div className="bg-background border p-3 pl-4 rounded-md text-ceat-green italic shadow-sm relative before:absolute before:left-0 before:top-0 before:bottom-0 before:w-1 before:bg-ceat-green before:rounded-l-md">
                "{s.suggestion}"
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
