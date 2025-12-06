import { boot } from 'quasar/wrappers'
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Django backend
})

export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})


export { axios, api }
