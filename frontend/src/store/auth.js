import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const storedUser = localStorage.getItem('user')
  const user = ref(storedUser ? JSON.parse(storedUser) : null)
  const userType = ref(localStorage.getItem('user_type') || (user.value?.user_type || null))
  const isLoggedIn = ref(!!user.value)

  const register = async (username, email, password, fullName) => {
    try {
      const response = await api.post('/auth/register', {
        username,
        email,
        password,
        full_name: fullName
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  }

  const login = async (username, password) => {
    try {
      const response = await api.post('/auth/login', {
        username,
        password
      })
      
      
      user.value = response.data.user
      userType.value = response.data.user.user_type
      isLoggedIn.value = true
      
      localStorage.setItem('user_type', userType.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  }

  const logout = async () => {
    try {
      await api.post('/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      user.value = null
      isLoggedIn.value = false
      userType.value = null
      
      localStorage.removeItem('user_type')
      localStorage.removeItem('user')
    }
  }

  const getProfile = async () => {
    try {
      const response = await api.get('/auth/profile')
      user.value = response.data.user
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  }

  const updateProfile = async (profileData) => {
    try {
      const response = await api.put('/auth/profile', profileData)
      user.value = response.data.user
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  }

  return {
    user,
    isLoggedIn,
    userType,
    register,
    login,
    logout,
    getProfile,
    updateProfile
  }
})
