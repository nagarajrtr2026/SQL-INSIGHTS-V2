# Frontend Developer Skills & Architecture Guide

This document outlines the core skills, technologies, and patterns required to build and maintain the frontend of the **SQL Insights** application.

---

## 🚀 Core Technology Stack

### 1. Next.js & React (v15 / v18)
- **Framework Model:** Custom React UI with pages/routes configuration.
- **Routing:** Standard Next.js client-side page-based routing.
- **TypeScript integration:** Strictly-typed components, hooks, and API interfaces for type safety.

### 2. Styling & Layout (TailwindCSS)
- **Utility-First CSS:** Rapid styling using Tailwind utility classes.
- **Responsive Design:** Consistent layouts across mobile, tablet, and desktop viewports.
- **Modern UI Features:** Custom animations, gradient backgrounds, and transition effects.

### 3. State Management (Zustand)
- **Global Store:** Lightweight store management for active database connections, user sessions, and global UI states.
- **Asynchronous Actions:** Clean separation between business logic and UI presentation layer.

### 4. Data Fetching & Caching (TanStack React Query v4)
- **Server State Sync:** Keeps queries, API test statuses, and response analytics in sync with the backend.
- **Declarative Fetching:** Streamlined loading, error, and retry states for API requests.

### 5. Interactive Visualizations (Plotly.js)
- **Dynamic Charts:** Client-side rendering of query outcomes into interactive charts (line charts, bar charts, heatmaps).
- **Data Parsing:** Transforming raw SQL results from the API into structured Plotly formats.

---

## 🎨 Design & Interaction Guidelines

### Visual Polish
- **Color Harmony:** Ensure the interface adheres to a curated color scheme rather than generic/raw colors.
- **Transitions:** Use smooth, elegant micro-animations via `framer-motion` to make elements feel responsive and premium.
- **No Placeholders:** All UI components must display realistic data states. Avoid empty blocks or boilerplate content.

### File Structure
- **`/components`:** Reusable UI components (e.g., Sidebar, Chat window, Chart wrapper).
- **`/pages`:** Application views mapped directly to routes.
- **`/context` / `/store`:** State providers and Zustand stores.
- **`/styles`:** Global style declarations, Tailwind configs, and fonts.
