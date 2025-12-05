import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access') || null,
    refreshToken: localStorage.getItem('refresh') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null')
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken
  },

  actions: {
    setAuth({ access, refresh, user }) {
      this.accessToken = access
      this.refreshToken = refresh
      this.user = user || null

      localStorage.setItem('access', access)
      localStorage.setItem('refresh', refresh)
      if (user) {
        localStorage.setItem('user', JSON.stringify(user))
      }
    },

    logout() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null

      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      localStorage.removeItem('user')
    }
  }
})
