import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useUserProfileStore = defineStore('userProfile', () => {
  // STATE
  const profile = ref(null)
  const isLoading = ref(false)
  const isSaving = ref(false)
  const error = ref(null)

  // ACTIONS - Fetch Profile
  const fetchProfile = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.get('/auth/profile')
      profile.value = response.data.user
      return response.data.user
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch profile'
      throw error.value
    } finally {
      isLoading.value = false
    }
  }

  // ACTIONS - Update Profile
  const updateProfile = async (data) => {
    isSaving.value = true
    error.value = null
    
    try {
      const response = await api.put('/auth/profile', data)
      profile.value = response.data.user
      return response.data.user
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to update profile'
      throw error.value
    } finally {
      isSaving.value = false
    }
  }

  // ACTIONS - Reset
  const reset = () => {
    profile.value = null
    error.value = null
  }

  return {
    // State
    profile,
    isLoading,
    isSaving,
    error,
    
    // Actions
    fetchProfile,
    updateProfile,
    reset
  }
})
