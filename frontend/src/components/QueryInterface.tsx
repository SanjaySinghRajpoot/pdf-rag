import { useState } from 'react';
import { Search, Send, Loader2, MessageSquare, Bot } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { useToast } from '@/hooks/use-toast';

interface QueryResult {
  chunk_text: string;
  // Add any additional fields from your API response
  score?: number;
  source?: string;
}

interface QueryResponse {
  query: string;
  results: QueryResult[];
  status?: 'success' | 'error';
  message?: string;
  sources?: string[];
  answer?: string; // Include if your API returns an answer field
}

export function QueryInterface() {
  const [query, setQuery] = useState('');
  const [isQuerying, setIsQuerying] = useState(false);
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) {
      toast({
        title: "Empty query",
        description: "Please enter a question to search.",
        variant: "destructive",
      });
      return;
    }

    setIsQuerying(true);
    setResponse(null);

    try {
      const startTime = performance.now();
      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const response = await fetch(`${apiBaseUrl}/api/v1/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query: query.trim(),
          // Add any additional parameters your API expects
          limit: 5 // Example: limit number of results
        }),
      });

      const result: QueryResponse = await response.json();
      const elapsedTime = (performance.now() - startTime).toFixed(0);

      if (response.ok) {
        setResponse({
          ...result,
          status: 'success'
        });
        toast({
          title: "Query successful",
          description: `Found ${result.results?.length || 0} results in ${elapsedTime}ms`,
        });
      } else {
        setResponse({
          query: query.trim(),
          results: [],
          status: 'error',
          message: result.message || 'Failed to process query'
        });
        toast({
          title: "Query failed",
          description: result.message || "Failed to process your query.",
          variant: "destructive",
        });
      }
    } catch (error) {
      console.error('Query error:', error);
      setResponse({
        query: query.trim(),
        results: [],
        status: 'error',
        message: 'Network error. Please check your connection and backend server.'
      });
      toast({
        title: "Query error",
        description: "Network error. Please check your connection and backend server.",
        variant: "destructive",
      });
    } finally {
      setIsQuerying(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gradient-card border-border shadow-elegant">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Search className="h-5 w-5 text-primary" />
            Query Documents
          </CardTitle>
          <CardDescription>
            Ask questions about your uploaded PDF documents
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Textarea
                placeholder="Ask a question about your documents... (e.g., What is the main topic discussed in the document?)"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="min-h-[100px] bg-background border-border focus:ring-primary"
                disabled={isQuerying}
              />
            </div>
            <Button
              type="submit"
              disabled={!query.trim() || isQuerying}
              className="w-full bg-gradient-primary hover:opacity-90 transition-opacity"
            >
              {isQuerying ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Searching...
                </>
              ) : (
                <>
                  <Send className="mr-2 h-4 w-4" />
                  Submit Query
                </>
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
  
      {response && (
        <Card className="bg-gradient-card border-border shadow-elegant">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              {response.status === 'success' ? (
                <>
                  <Bot className="h-5 w-5 text-success" />
                  Response
                </>
              ) : (
                <>
                  <MessageSquare className="h-5 w-5 text-destructive" />
                  Error
                </>
              )}
            </CardTitle>
            <CardDescription>
              {response.query && `Query: "${response.query}"`}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {response.status === 'success' ? (
              <>
                {response.answer && (
                  <div className="p-4 bg-muted rounded-lg">
                    <h4 className="font-medium text-foreground mb-2">Answer:</h4>
                    <p className="text-foreground leading-relaxed whitespace-pre-wrap">
                      {response.answer}
                    </p>
                  </div>
                )}
  
                {response.results?.length > 0 && (
                  <div className="space-y-4">
                    <h4 className="font-medium text-foreground">
                      Relevant Chunks ({response.results.length}):
                    </h4>
                    <div className="space-y-3">
                      {response.results.map((result, index) => (
                        <div 
                          key={index}
                          className="p-4 bg-muted/50 rounded-lg border border-border/50"
                        >
                          <div className="flex justify-between items-start mb-2">
                            <span className="text-xs font-mono px-2 py-1 bg-muted-foreground/10 rounded">
                              Chunk #{index + 1}
                            </span>
                            {result.score && (
                              <span className="text-xs font-mono px-2 py-1 bg-muted-foreground/10 rounded">
                                Score: {result.score.toFixed(2)}
                              </span>
                            )}
                          </div>
                          <p className="text-foreground whitespace-pre-wrap">
                            {result.chunk_text}
                          </p>
                          {result.source && (
                            <p className="text-xs text-muted-foreground mt-2">
                              Source: {result.source}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
  
                {response.sources && response.sources.length > 0 && (
                  <div className="p-4 bg-muted/50 rounded-lg">
                    <h4 className="font-medium text-foreground mb-2">Sources:</h4>
                    <ul className="list-disc list-inside space-y-1">
                      {response.sources.map((source, index) => (
                        <li key={index} className="text-muted-foreground text-sm">
                          {source}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </>
            ) : (
              <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
                <p className="text-destructive">
                  {response.message || 'An error occurred while processing your query.'}
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
