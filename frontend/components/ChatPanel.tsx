import React, { useState, useEffect, useRef, ReactNode } from 'react'
import { useConnection } from '../context/connection-context'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8100'

interface Message {
  sender: 'user' | 'ai'
  text: string
  sql?: string
  rows?: any[]
  insights?: string[]
  chart?: {
    title: string
    value: ReactNode
    type: string
    figure?: string
  }
}

// Sub-component to safely render Plotly Express figures dynamically on the client
const ChartRenderer = ({ figureJson }: { figureJson: string }) => {
  const chartRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!chartRef.current || !figureJson) return

    import('plotly.js-basic-dist').then((Plotly) => {
      try {
        const fig = JSON.parse(figureJson)
        fig.layout = {
          ...fig.layout,
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(0,0,0,0)',
          font: { color: '#f4f4f5', family: 'Inter, sans-serif' },
          autosize: true,
          margin: { l: 50, r: 20, t: 40, b: 50 }
        }
        if (fig.data && fig.data.length > 0) {
          fig.data.forEach((trace: any) => {
            if (trace.type === 'bar') {
              trace.marker = { ...trace.marker, color: '#22d3ee' } // Neon Cyan
            } else {
              trace.line = { ...trace.line, color: '#a78bfa', width: 3 } // Violet Line
            }
          })
        }
        Plotly.newPlot(chartRef.current!, fig.data, fig.layout, { responsive: true, displayModeBar: false })
      } catch (err) {
        console.error('Error drawing Plotly chart:', err)
      }
    })
  }, [figureJson])

  return <div ref={chartRef} className="w-full h-80 bg-zinc-950/50 border border-white/5 rounded-2xl overflow-hidden p-2" />
}

export default function ChatPanel() {
  const { connection } = useConnection()
  const [input, setInput] = useState('Show average sales by product_name')
  const [isLoading, setIsLoading] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [history, setHistory] = useState<string[]>([
    'Show all North region sales',
    'Show highest sales product_name',
    'Show average sales by region',
  ])
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom of chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSubmit = async (queryText?: string) => {
    const promptText = queryText || input
    if (!promptText.trim()) return

    setIsLoading(true)
    // Add user query to messaging state
    setMessages((current) => [...current, { sender: 'user', text: promptText }])
    
    // Add to history list if not duplicate
    if (!history.includes(promptText)) {
      setHistory((curr) => [promptText, ...curr.slice(0, 7)])
    }

    try {
      const response = await fetch(`${API_BASE}/api/chat/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ connection, prompt: promptText }),
      })
      const data = await response.json()
      if (response.ok) {
        setMessages((current) => [
          ...current,
          {
            sender: 'ai',
            text: data.response || 'I have analyzed the database using AI SQL generation and summarized insights below.',
            sql: data.sql,
            rows: data.rows,
            insights: data.insights,
            chart: data.chart,
          },
        ])
      } else {
        setMessages((current) => [
          ...current,
          {
            sender: 'ai',
            text: `Error parsing request: ${data.detail || 'Unable to query database table.'}`,
          },
        ])
      }
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          sender: 'ai',
          text: 'Network error connecting to AI agent backend. Make sure FastAPI server is running.',
        },
      ])
    } finally {
      setIsLoading(false)
      if (!queryText) setInput('')
    }
  }

  const handleDownloadPDF = async (title: string, rows: any[], insights: string[]) => {
    try {
      const response = await fetch(`${API_BASE}/api/reports/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, rows, insights }),
      })
      if (!response.ok) throw new Error('Failed to generate PDF')
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `agentic_ai_${title.toLowerCase().replace(/[^a-z0-9]/g, '_')}_report.pdf`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    } catch (err) {
      alert('Error exporting PDF: ' + err)
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Left Chat Window & History */}
      <div className="lg:col-span-2 flex flex-col h-[750px] bg-zinc-900/60 border border-white/10 rounded-3xl p-5 shadow-2xl backdrop-blur-xl">
        <div className="mb-4">
          <p className="text-sm uppercase tracking-[0.24em] text-fuchsia-300">AI Assistant</p>
          <h2 className="text-xl font-semibold">Insight Dialog</h2>
        </div>

        {/* Chat Feed */}
        <div className="flex-1 overflow-y-auto space-y-4 rounded-2xl border border-white/5 bg-black/40 p-4 mb-4 scrollbar-thin">
          {messages.length > 0 ? (
            messages.map((msg, index) => (
              <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-[85%] rounded-2xl p-4 leading-relaxed ${
                    msg.sender === 'user'
                      ? 'bg-gradient-to-r from-violet-600 to-indigo-600 text-white shadow-lg shadow-violet-500/10'
                      : 'bg-zinc-800/80 border border-white/5 text-zinc-100'
                  }`}
                >
                  <p className="text-xs text-white/50 uppercase tracking-widest font-bold mb-1">
                    {msg.sender === 'user' ? 'You' : 'AI SQL Agent'}
                  </p>
                  <div className="text-sm">{msg.text}</div>

                  {/* Render SQL Block */}
                  {msg.sql && (
                    <div className="mt-4 space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] uppercase font-bold text-cyan-300 tracking-widest">Generated SQL Code</span>
                        <button
                          onClick={() => {
                            navigator.clipboard.writeText(msg.sql || '')
                            alert('SQL query copied to clipboard!')
                          }}
                          className="text-xs hover:text-white text-zinc-400 bg-white/5 px-2.5 py-0.5 rounded-full border border-white/10"
                        >
                          Copy
                        </button>
                      </div>
                      <pre className="text-xs font-mono bg-black/50 border border-white/5 rounded-xl p-3 text-emerald-400 overflow-x-auto whitespace-pre-wrap">
                        {msg.sql}
                      </pre>
                    </div>
                  )}

                  {/* Render KPI Card */}
                  {msg.chart && msg.chart.type === 'kpi' && (
                    <div className="mt-4 bg-gradient-to-br from-violet-600/10 to-cyan-500/10 border border-cyan-500/20 rounded-2xl p-6 text-center shadow-lg backdrop-blur-md animate-fadeIn">
                      <span className="text-xs uppercase font-bold text-cyan-300 tracking-widest block mb-1">
                        {msg.chart.title || 'Key Metric Indicator'}
                      </span>
                      <span className="text-4xl font-extrabold text-white tracking-tight font-mono">
                        {msg.chart.value}
                      </span>
                    </div>
                  )}

                  {/* Render Charts */}
                  {msg.chart && msg.chart.figure && (
                    <div className="mt-4 space-y-1">
                      <span className="text-[10px] uppercase font-bold text-fuchsia-300 tracking-widest block mb-1">Interactive Data Chart</span>
                      <ChartRenderer figureJson={msg.chart.figure} />
                    </div>
                  )}

                  {/* Render Dynamic Insights Cards */}
                  {msg.insights && msg.insights.length > 0 && (
                    <div className="mt-4 space-y-2">
                      <span className="text-[10px] uppercase font-bold text-cyan-300 tracking-widest block">AI Business Insights</span>
                      <div className="grid grid-cols-1 gap-2">
                        {msg.insights.map((insight, idx) => (
                          <div key={idx} className="bg-black/30 border border-white/5 rounded-xl p-3 flex items-start gap-2.5">
                            <span className="mt-1 flex-shrink-0 w-2.5 h-2.5 rounded-full bg-cyan-400 shadow-[0_0_8px_#22d3ee]"></span>
                            <span className="text-xs text-slate-200">{insight}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Render Result Grid */}
                  {msg.rows && msg.rows.length > 0 && (
                    <div className="mt-4 space-y-1">
                      <span className="text-[10px] uppercase font-bold text-indigo-300 tracking-widest block mb-1">
                        Query Output ({msg.rows.length} rows)
                      </span>
                      <div className="max-h-60 overflow-auto border border-white/5 rounded-xl bg-black/40">
                        <table className="min-w-full divide-y divide-white/5 text-left text-xs">
                          <thead className="bg-white/5 text-zinc-300 uppercase tracking-wider text-[10px] sticky top-0">
                            <tr>
                              {Object.keys(msg.rows[0]).map((key) => (
                                <th key={key} className="px-3 py-2 font-semibold">
                                  {key}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-white/5 text-zinc-400 font-mono">
                            {msg.rows.map((row, rIdx) => (
                              <tr key={rIdx} className="hover:bg-white/5 transition">
                                {Object.values(row).map((val: any, cIdx) => (
                                  <td key={cIdx} className="px-3 py-1.5 truncate max-w-[150px]">
                                    {val === null ? 'NULL' : String(val)}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}

                  {/* Render Report Downloader */}
                  {msg.rows && msg.rows.length > 0 && msg.insights && (
                    <div className="mt-4 flex justify-end">
                      <button
                        onClick={() => handleDownloadPDF('Database Insights Report', msg.rows || [], msg.insights || [])}
                        className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold bg-emerald-500 hover:bg-emerald-600 text-black shadow-lg shadow-emerald-500/20 hover:scale-[1.01] transition"
                      >
                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Download PDF Report
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ))
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-center text-slate-400 p-8 space-y-3">
              <div className="w-12 h-12 rounded-full border border-white/10 bg-white/5 flex items-center justify-center text-cyan-300 text-xl font-bold animate-pulse">
                ✧
              </div>
              <div className="font-semibold text-white">No query initiated yet</div>
              <p className="text-xs max-w-xs text-slate-500">
                Connect your database, upload spreadsheets, or choose a prompt from the sidebar to generate instant AI SQL results.
              </p>
            </div>
          )}
          {isLoading && (
            <div className="flex justify-start">
              <div className="rounded-2xl p-4 bg-zinc-800/40 border border-white/5 text-zinc-100 space-y-3 max-w-[85%] w-72">
                <p className="text-[10px] text-cyan-300 font-bold uppercase tracking-widest animate-pulse">AI Agent processing...</p>
                <div className="space-y-2 animate-pulse">
                  <div className="h-3 bg-white/10 rounded w-5/6"></div>
                  <div className="h-3 bg-white/10 rounded w-full"></div>
                  <div className="h-3 bg-white/10 rounded w-2/3"></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <div className="grid gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSubmit()
              }
            }}
            rows={2}
            placeholder="Ask about sales trends, high performing products, or specific metrics..."
            className="w-full rounded-2xl bg-black/60 border border-white/10 p-3 text-white text-sm focus:outline-none focus:border-cyan-400/50 resize-none transition"
          />
          <button
            onClick={() => handleSubmit()}
            disabled={isLoading || !input.trim()}
            className="w-full py-3 rounded-2xl bg-gradient-to-r from-violet-500 via-fuchsia-500 to-cyan-500 text-white text-sm font-semibold transition hover:scale-[1.01] active:scale-[0.99] disabled:opacity-40 disabled:cursor-not-allowed shadow-xl shadow-fuchsia-500/10"
          >
            {isLoading ? 'Agent Generating Insights...' : 'Execute AI Analytics'}
          </button>
        </div>
      </div>

      {/* Right Prompt History */}
      <div className="bg-zinc-900/60 border border-white/10 rounded-3xl p-5 shadow-2xl backdrop-blur-xl h-[750px] flex flex-col">
        <div className="mb-4">
          <p className="text-sm uppercase tracking-[0.24em] text-violet-300">Prompt Library</p>
          <h2 className="text-xl font-semibold">Quick Query</h2>
        </div>
        <p className="text-xs text-slate-400 mb-4">
          Select or trigger one of the recommended and previous business query prompts instantly:
        </p>
        <div className="flex-1 overflow-y-auto space-y-2 pr-1">
          {history.map((promptText, index) => (
            <button
              key={index}
              onClick={() => {
                setInput(promptText)
                handleSubmit(promptText)
              }}
              disabled={isLoading}
              className="w-full text-left p-3.5 rounded-2xl bg-black/30 border border-white/5 text-xs text-zinc-300 hover:text-white hover:bg-white/5 hover:border-white/10 active:scale-[0.99] transition flex items-start gap-2.5"
            >
              <span className="text-violet-400 mt-0.5">⚡</span>
              <span className="line-clamp-2">{promptText}</span>
            </button>
          ))}
        </div>
        <div className="pt-4 border-t border-white/5 mt-4 text-[11px] text-slate-500 text-center leading-relaxed">
          The SQL generation dynamically adapts based on the active table structures currently loaded in the connection workspace.
        </div>
      </div>
    </div>
  )
}

