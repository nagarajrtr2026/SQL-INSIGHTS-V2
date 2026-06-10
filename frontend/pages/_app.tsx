import '../styles/globals.css'
import type { AppProps } from 'next/app'
import { motion } from 'framer-motion'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <Component {...pageProps} />
    </motion.div>
  )
}
