import { useState } from 'react'
import Head from 'next/head'
import Sidebar from '../components/Sidebar'
import ChatPanel from '../components/ChatPanel'
import DBModal from '../components/DBModal'
import UploadSection from '../components/UploadSection'
import { ConnectionProvider } from '../context/connection-context'

export default function Home() {
  const [activeTab, setActiveTab] = useState('console')

  return (
    <ConnectionProvider>
      <div className="min-h-screen bg-gradient-to-br from-zinc-950 via-black to-zinc-900 text-white flex select-none overflow-x-hidden relative">
        {/* Neon Glow Highlights in Backdrop */}
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-violet-600/10 rounded-full blur-[150px] pointer-events-none" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[55%] h-[55%] bg-cyan-500/10 rounded-full blur-[160px] pointer-events-none" />

        <Head>
          <title>GENORA AI - Autonomous SQL Analytics SaaS</title>
          <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>✧</text></svg>" />
        </Head>

        {/* Brand Sidebar with Active Tab Callbacks */}
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

        {/* Main Dashboard Space */}
        <main className="flex-1 p-8 overflow-y-auto h-screen relative z-10 space-y-6 scrollbar-thin">
          {/* Header Area */}
          <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/5 pb-5">
            <div>
              <h1 className="text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-zinc-200 to-zinc-400">
                {activeTab === 'console' && 'Autonomous Database Console'}
                {activeTab === 'warehouses' && 'Data Warehouses'}
                {activeTab === 'reports' && 'BI Reports Center'}
              </h1>
              <p className="text-xs text-zinc-400 font-medium mt-1">
                {activeTab === 'console' && 'Translate English business prompts into executable SQL queries, insights, charts, and reports dynamically.'}
                {activeTab === 'warehouses' && 'Browse your connected databases, configure connection credentials, and inspect database schemas.'}
                {activeTab === 'reports' && 'Schedule, generate, and view business intelligence PDF reports created from database insights.'}
              </p>
            </div>
            <div className="flex items-center gap-2 bg-white/5 border border-white/10 px-4 py-2.5 rounded-2xl text-xs backdrop-blur-md">
              <span className="w-2 h-2 rounded-full bg-cyan-400 shadow-[0_0_8px_#22d3ee] animate-pulse"></span>
              <span className="text-zinc-300 font-mono">Agent Engine: Local Ollama Client</span>
            </div>
          </header>

          {/* Tab Views */}
          {activeTab === 'console' && (
            <div className="grid grid-cols-1 xl:grid-cols-[380px_minmax(0,1fr)] gap-6 items-start animate-fadeIn">
              {/* Left Control Workspace */}
              <div className="space-y-6">
                <DBModal />
                <UploadSection />
              </div>

              {/* Right Chat and Output Terminal */}
              <div className="space-y-6">
                <ChatPanel />
              </div>
            </div>
          )}

          {activeTab === 'warehouses' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start animate-fadeIn">
              <div className="lg:col-span-1 space-y-6">
                <DBModal />
                <UploadSection />
              </div>
              <div className="lg:col-span-2 bg-zinc-900/60 border border-white/10 rounded-3xl p-6 shadow-2xl backdrop-blur-xl space-y-6">
                <div>
                  <p className="text-sm uppercase tracking-[0.24em] text-violet-300">Schema Explorer</p>
                  <h2 className="text-2xl font-bold">Connected Relational Stores</h2>
                </div>
                <p className="text-sm text-zinc-400">
                  Manage database adapters and explore active schemas dynamically registered from tables and columns.
                </p>
                <div className="p-5 rounded-2xl bg-black/40 border border-white/5 space-y-4">
                  <div className="flex items-center justify-between text-xs text-zinc-400 uppercase tracking-widest font-bold">
                    <span>Detected Tables</span>
                    <span className="text-cyan-400">Sync Online</span>
                  </div>
                  <div className="divide-y divide-white/5 text-sm">
                    <div className="py-3 flex items-center justify-between">
                      <div>
                        <span className="font-mono text-white font-semibold">sales</span>
                        <p className="text-[10px] text-zinc-500 mt-0.5">Columns: id, product_name, region, sales, sale_date</p>
                      </div>
                      <span className="text-xs px-2.5 py-1 rounded-full bg-white/5 border border-white/10 text-zinc-300">
                        Default Table
                      </span>
                    </div>
                    <div className="py-3 flex items-center justify-between">
                      <div>
                        <span className="font-mono text-white font-semibold">t_test</span>
                        <p className="text-[10px] text-zinc-500 mt-0.5">Columns: col1, col2</p>
                      </div>
                      <span className="text-xs px-2.5 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
                        Uploaded CSV
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'reports' && (
            <div className="bg-zinc-900/60 border border-white/10 rounded-3xl p-6 shadow-2xl backdrop-blur-xl space-y-6 animate-fadeIn">
              <div>
                <p className="text-sm uppercase tracking-[0.24em] text-fuchsia-300">Reporting Engine</p>
                <h2 className="text-2xl font-bold">Scheduled & Exported Reports</h2>
              </div>
              <p className="text-sm text-zinc-400">
                Generate compiled PDF business intelligence reports from recent SQL executions. Customize templates, schedules, and delivery targets.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-5 rounded-2xl bg-black/40 border border-white/5 space-y-3">
                  <h3 className="font-semibold text-lg">BI PDF Template</h3>
                  <p className="text-xs text-zinc-400 leading-relaxed">
                    Standard corporate report layout including dynamic database summaries, reflected schemas, AI business insights, and Plotly Express trend figures.
                  </p>
                  <div className="flex gap-2">
                    <span className="text-xs px-2.5 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 font-mono">Portrait</span>
                    <span className="text-xs px-2.5 py-1 rounded-full bg-violet-500/10 border border-violet-500/20 text-violet-400 font-mono">Letter Size</span>
                  </div>
                </div>
                <div className="p-5 rounded-2xl bg-black/40 border border-white/5 space-y-3">
                  <h3 className="font-semibold text-lg">Delivery Target</h3>
                  <p className="text-xs text-zinc-400 leading-relaxed">
                    Configure email, Slack webhooks, or cloud bucket targets to automatically dispatch generated insights reports on a Cron schedule.
                  </p>
                  <button className="px-4 py-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-semibold text-white transition">
                    Configure Dispatcher
                  </button>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </ConnectionProvider>
  )
}


