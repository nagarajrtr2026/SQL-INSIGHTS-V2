import React, { useState } from 'react'
import { useConnection } from '../context/connection-context'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8100'

interface UploadResult {
  table_name: string
  rows: number
  columns: string[]
}

export default function UploadSection({ onUploadSuccess }: { onUploadSuccess?: (tableName: string) => void }) {
  const { connection } = useConnection()
  const [file, setFile] = useState<File | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [status, setStatus] = useState<string | null>(null)
  const [result, setResult] = useState<UploadResult | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setResult(null)
      setStatus(null)
    }
  }

  const handleUpload = async () => {
    if (!file) return
    setIsLoading(true)
    setStatus('Parsing file and creating table in database...')
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('connection', JSON.stringify(connection))

    try {
      const response = await fetch(`${API_BASE}/api/upload`, {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()
      if (response.ok) {
        setStatus('Dataset uploaded successfully!')
        setResult({
          table_name: data.table_name,
          rows: data.rows,
          columns: data.columns,
        })
        setFile(null)
        if (onUploadSuccess) {
          onUploadSuccess(data.table_name)
        }
      } else {
        setStatus(`Upload failed: ${data.detail || 'Error processing spreadsheet'}`)
      }
    } catch (error) {
      setStatus('Network or connection error')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="bg-zinc-900/60 rounded-3xl border border-white/10 p-5 shadow-2xl shadow-cyan-500/10 backdrop-blur-xl transition duration-300">
      <div className="mb-4">
        <p className="text-sm uppercase tracking-[0.24em] text-cyan-300">Fast Ingestion</p>
        <h2 className="text-xl font-semibold">Upload Dataset</h2>
      </div>

      <div className="space-y-4">
        <label className="flex flex-col items-center justify-center border border-dashed border-white/20 rounded-2xl p-6 cursor-pointer bg-black/30 hover:bg-black/50 transition">
          <svg className="w-8 h-8 text-cyan-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
          </svg>
          <span className="text-sm text-slate-300 font-medium">
            {file ? file.name : 'Drop CSV or Excel here, or click to browse'}
          </span>
          <span className="text-xs text-slate-500 mt-1">Supports .csv, .xlsx, .xls</span>
          <input type="file" accept=".csv, .xlsx, .xls" onChange={handleFileChange} className="hidden" />
        </label>

        {file && (
          <button
            onClick={handleUpload}
            disabled={isLoading}
            className="w-full py-3 rounded-2xl font-semibold bg-gradient-to-r from-cyan-400 to-blue-500 text-black shadow-lg shadow-cyan-500/20 hover:scale-[1.01] transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Processing Ingestion...' : 'Ingest to Database'}
          </button>
        )}

        {status && (
          <div className="text-sm text-center font-medium bg-black/40 rounded-xl p-3 border border-white/5 text-slate-300">
            {isLoading && (
              <span className="inline-block animate-spin mr-2 border-2 border-cyan-400 border-t-transparent rounded-full w-4 h-4 vertical-middle"></span>
            )}
            {status}
          </div>
        )}

        {result && (
          <div className="bg-black/60 border border-emerald-500/20 rounded-2xl p-4 text-sm space-y-2">
            <div className="flex items-center text-emerald-400 font-semibold mb-1">
              <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Table Created Successfully
            </div>
            <div className="grid grid-cols-2 gap-2 text-slate-400 text-xs">
              <div>Table Name: <span className="text-white font-mono">{result.table_name}</span></div>
              <div>Rows Inserted: <span className="text-white font-semibold">{result.rows}</span></div>
            </div>
            <div className="pt-2 border-t border-white/10">
              <div className="text-xs text-slate-400 mb-1">Detected Columns:</div>
              <div className="flex flex-wrap gap-1">
                {result.columns.map((col, idx) => (
                  <span key={idx} className="text-[10px] font-mono bg-white/5 border border-white/10 rounded px-1.5 py-0.5 text-slate-300">
                    {col}
                  </span>
                ))}
              </div>
            </div>
            <p className="text-xs text-cyan-400 pt-1">
              💡 Tip: Try asking "Show average values for the table {result.table_name}"
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
