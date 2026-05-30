const BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json()
}

export const getProfile = () => request('/profile')

export const putProfile = (profile) =>
  request('/profile', { method: 'PUT', body: JSON.stringify(profile) })

export const getFeed = () => request('/feed')
