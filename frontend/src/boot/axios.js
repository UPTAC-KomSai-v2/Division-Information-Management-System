import { boot } from 'quasar/wrappers'
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://192.168.1.76:8000', // Django backend host (update if backend IP changes)
})

// Silence noisy ResizeObserver loop errors that bubble to the dev-server overlay
if (typeof window !== 'undefined' && !window.__roErrorSilencer__) {
  const handler = (event) => {
    const message = event?.message || ''
    if (
      typeof message === 'string' &&
      (message.includes('ResizeObserver loop completed') ||
        message.includes('ResizeObserver loop limit exceeded'))
    ) {
      event.preventDefault()
      event.stopImmediatePropagation()
    }
  }
  const onError = window.onerror
  window.onerror = (message, source, lineno, colno, error) => {
    if (
      typeof message === 'string' &&
      (message.includes('ResizeObserver loop completed') ||
        message.includes('ResizeObserver loop limit exceeded'))
    ) {
      return true
    }
    if (typeof onError === 'function') {
      return onError(message, source, lineno, colno, error)
    }
    return false
  }
  window.__roErrorSilencer__ = handler
  window.addEventListener('error', handler, { capture: true })
}

export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})


export { axios, api }
