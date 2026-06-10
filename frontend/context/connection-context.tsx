import React, { createContext, useContext, useState, ReactNode } from 'react'

type DBConnection = {
  kind: string
  host: string
  port: number
  username: string
  password: string
  database: string
}

type ConnectionContextType = {
  connection: DBConnection
  setConnection: (connection: DBConnection) => void
}

const defaultConnection: DBConnection = {
  kind: 'postgresql',
  host: 'localhost',
  port: 5432,
  username: 'postgres',
  password: 'postgres',
  database: 'agentic_ai',
}

const ConnectionContext = createContext<ConnectionContextType>({
  connection: defaultConnection,
  setConnection: () => {},
})

export function ConnectionProvider({ children }: { children: ReactNode }) {
  const [connection, setConnection] = useState<DBConnection>(defaultConnection)
  return (
    <ConnectionContext.Provider value={{ connection, setConnection }}>
      {children}
    </ConnectionContext.Provider>
  )
}

export function useConnection() {
  return useContext(ConnectionContext)
}
