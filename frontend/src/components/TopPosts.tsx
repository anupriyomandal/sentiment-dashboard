import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Post } from '@/types'
import { MessageSquare, ThumbsUp } from 'lucide-react'

export default function TopPosts({ posts }: { posts: Post[] }) {
  if (!posts || posts.length === 0) return <div className="text-muted-foreground p-4">No top posts found.</div>

  const getBadgeVariant = (sentiment: string) => {
    if (sentiment === 'Positive') return 'positive'
    if (sentiment === 'Negative') return 'negative'
    return 'neutral'
  }

  return (
    <div className="space-y-4">
      {posts.map((post) => (
        <Card key={post.id} className="overflow-hidden transition-all hover:shadow-lg dark:hover:shadow-white/5">
          <CardHeader className="pb-2 bg-muted/30">
            <div className="flex justify-between items-start">
              <div className="space-y-1 pr-4">
                <CardTitle className="text-base line-clamp-2">
                  <a href={post.url} target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors">
                    {post.title}
                  </a>
                </CardTitle>
                <div className="text-xs text-muted-foreground flex items-center space-x-2">
                  <span className="font-medium text-foreground">r/{post.subreddit}</span>
                  <span>•</span>
                  <div className="flex items-center">
                    <ThumbsUp className="w-3 h-3 mr-1" /> {post.upvotes}
                  </div>
                </div>
              </div>
              <Badge variant={getBadgeVariant(post.sentiment)}>{post.sentiment}</Badge>
            </div>
          </CardHeader>
          <CardContent className="pt-4 text-sm">
            {post.top_comment ? (
              <div className="bg-muted p-3 rounded-md flex items-start space-x-2">
                <MessageSquare className="w-4 h-4 text-muted-foreground mt-0.5 shrink-0" />
                <p className="line-clamp-3 italic text-muted-foreground">"{post.top_comment}"</p>
              </div>
            ) : (
              <p className="text-muted-foreground italic">No top comment available.</p>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
