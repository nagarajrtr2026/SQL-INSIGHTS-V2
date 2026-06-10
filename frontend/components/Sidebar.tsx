import React from 'react'

interface SidebarProps {
  activeTab: string
  setActiveTab: (tab: string) => void
}

export default function Sidebar({ activeTab, setActiveTab }: SidebarProps) {
  return (
    <aside className="w-72 bg-black/50 border-r border-white/10 backdrop-blur-xl h-screen sticky top-0 flex flex-col p-6 shadow-2xl justify-between">
      <div>
        {/* Brand Header */}
        <div className="mb-8 flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-cyan-400 via-fuchsia-500 to-violet-600 flex items-center justify-center font-bold text-lg text-white shadow-[0_0_20px_rgba(167,139,250,0.3)] animate-pulse">
            Ω
          </div>
          <div>
            <div className="text-base font-bold tracking-tight text-white">GENORA AI</div>
            <div className="text-[10px] uppercase font-bold tracking-[0.2em] text-cyan-400">Insight SaaS</div>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="space-y-2.5">
          <button
            onClick={() => setActiveTab('console')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition duration-200 ${
              activeTab === 'console'
                ? 'bg-white/5 border border-white/10 text-white font-semibold text-xs shadow-inner'
                : 'hover:bg-white/5 border border-transparent hover:border-white/5 text-zinc-400 hover:text-white font-medium text-xs'
            }`}
          >
            <span className="text-cyan-400 text-sm">✦</span>
            Interactive Console
          </button>
          <button
            onClick={() => setActiveTab('warehouses')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition duration-200 ${
              activeTab === 'warehouses'
                ? 'bg-white/5 border border-white/10 text-white font-semibold text-xs shadow-inner'
                : 'hover:bg-white/5 border border-transparent hover:border-white/5 text-zinc-400 hover:text-white font-medium text-xs'
            }`}
          >
            <span className="text-violet-400 text-sm">⎔</span>
            Data Warehouses
          </button>
          <button
            onClick={() => setActiveTab('reports')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition duration-200 ${
              activeTab === 'reports'
                ? 'bg-white/5 border border-white/10 text-white font-semibold text-xs shadow-inner'
                : 'hover:bg-white/5 border border-transparent hover:border-white/5 text-zinc-400 hover:text-white font-medium text-xs'
            }`}
          >
            <span className="text-fuchsia-400 text-sm">⌹</span>
            Scheduled Reports
          </button>
        </nav>
      </div>

      {/* Footer Info */}
      <div className="space-y-2.5">
        <div className="p-3.5 rounded-2xl bg-gradient-to-br from-violet-950/40 to-black/30 border border-violet-500/10 text-[10px] leading-relaxed text-zinc-400">
          <div className="font-bold text-violet-300 uppercase tracking-widest mb-1">Active Core</div>
          FastAPI orchestration with Ollama local models.
        </div>
        <div className="text-center text-[10px] text-zinc-600">
          • Genora pair-programming
        </div>
      </div>
    </aside>
  )
}


