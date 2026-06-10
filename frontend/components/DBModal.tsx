import React, { useState } from 'react'
import { useConnection } from '../context/connection-context'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8100'

export default function DBModal() {
  const { connection, setConnection } = useConnection()
  const [open, setOpen] = useState(false)
  const [status, setStatus] = useState<'idle' | 'testing' | 'success' | 'failed'>('idle')
  const [statusMsg, setStatusMsg] = useState<string | null>(null)

  const testConn = async () => {
    setStatus('testing')
    setStatusMsg('Testing connection to database...')
    try {
      const resp = await fetch(`${API_BASE}/api/database/test`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(connection),
      })
      if (resp.ok) {
        setStatus('success')
        setStatusMsg('Active Connection Established Successfully!')
      } else {
        const data = await resp.json()
        setStatus('failed')
        setStatusMsg(`Failed to connect: ${data.detail || 'Access denied'}`)
      }
    } catch (err) {
      setStatus('failed')
      setStatusMsg('Network timeout. Verify backend routes.')
    }
  }

  return (
    <div className="bg-zinc-900/60 rounded-3xl border border-white/10 p-5 shadow-2xl shadow-violet-500/10 backdrop-blur-xl transition duration-300">
      <div className="flex items-center justify-between mb-4">
        <div>
          <p className="text-sm uppercase tracking-[0.24em] text-violet-300">Database Engine</p>
          <h2 className="text-xl font-semibold flex items-center gap-2">
            PostgreSQL Connection
            <span className={`w-2.5 h-2.5 rounded-full ${
              status === 'success' ? 'bg-emerald-500 animate-pulse shadow-[0_0_8px_#10b981]' : 'bg-zinc-600 shadow-[0_0_8px_#4b5563]'
            }`} />
          </h2>
        </div>
        <button
          onClick={() => setOpen(!open)}
          className="px-4 py-1.5 rounded-full text-xs font-semibold bg-white/5 border border-white/10 hover:bg-white/10 active:scale-95 transition"
        >
          {open ? 'Collapse' : 'Configure'}
        </button>
      </div>

      {open && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4 animate-fadeIn">
          <div className="flex flex-col gap-1">
            <span className="text-[10px] uppercase font-bold text-zinc-400 tracking-wider pl-1">Engine Kind</span>
            <select
              value={connection.kind}
              onChange={(e) => setConnection({ ...connection, kind: e.target.value })}
              className="rounded-2xl p-3 bg-black/60 border border-white/10 text-white text-xs focus:outline-none focus:border-cyan-400"
            >
              <option value="postgresql">PostgreSQL</option>
              <option value="mysql">MySQL</option>
            </select>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-[10px] uppercase font-bold text-zinc-400 tracking-wider pl-1">Server Host</span>
            <input
              value={connection.host}
              onChange={(e) => setConnection({ ...connection, host: e.target.value })}
              placeholder="127.0.0.1"
              className="rounded-2xl p-3 bg-black/60 border border-white/10 text-white text-xs focus:outline-none focus:border-cyan-400"
            />
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-[10px] uppercase font-bold text-zinc-400 tracking-wider pl-1">Server Port</span>
            <input
              value={connection.port}
              type="number"
              onChange={(e) => setConnection({ ...connection, port: Number(e.target.value) })}
              placeholder="5432"
              className="rounded-2xl p-3 bg-black/60 border border-white/10 text-white text-xs focus:outline-none focus:border-cyan-400"
            />
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-[10px] uppercase font-bold text-zinc-400 tracking-wider pl-1">DB Name</span>
            <input
              value={connection.database}
              onChange={(e) => setConnection({ ...connection, database: e.target.value })}
              placeholder="agentic_ai"
              className="rounded-2xl p-3 bg-black/60 border border-white/10 text-white text-xs focus:outline-none focus:border-cyan-400"
            />
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-[10px] uppercase font-bold text-zinc-400 tracking-wider pl-1">Username</span>
            <input
              value={connection.username}
              onChange={(e) => setConnection({ ...connection, username: e.target.value })}
              placeholder="postgres"
              className="rounded-2xl p-3 bg-black/60 border border-white/10 text-white text-xs focus:outline-none focus:border-cyan-400"
            />
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-[10px] uppercase font-bold text-zinc-400 tracking-wider pl-1">Password</span>
            <input
              value={connection.password}
              type="password"
              onChange={(e) => setConnection({ ...connection, password: e.target.value })}
              placeholder="••••••••"
              className="rounded-2xl p-3 bg-black/60 border border-white/10 text-white text-xs focus:outline-none focus:border-cyan-400"
            />
          </div>
        </div>
      )}

      <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center">
        <button
          onClick={testConn}
          disabled={status === 'testing'}
          className="px-5 py-3 rounded-2xl bg-gradient-to-r from-violet-500 to-indigo-600 text-white font-semibold text-xs hover:scale-[1.01] active:scale-[0.99] transition disabled:opacity-60 shadow-lg shadow-violet-500/20"
        >
          {status === 'testing' ? 'Testing Link...' : 'Sync Connection'}
        </button>
        <span className={`text-xs font-medium ${
          status === 'success' ? 'text-emerald-400' : status === 'failed' ? 'text-fuchsia-400' : 'text-slate-400'
        }`}>
          {statusMsg ?? 'Click test to validate active database workspace'}
        </span>
      </div>
    </div>
  )
}

