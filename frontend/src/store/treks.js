import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useTrekStore = defineStore('treks', () => {
  // STATE
  const treks = ref([])
  const currentTrek = ref(null)
  const totalPages = ref(1)
  const currentPage = ref(1)
  const isLoading = ref(false)
  const error = ref(null)

  // FILTERS & PAGINATION
  const filters = ref({
    page: 1,
    per_page: 10,
    difficulty: null,
    location: null,
    duration_min: null,
    duration_max: null,
    sort_by: 'start_date'
  })

  // COMPUTED
  const hasMorePages = computed(() => currentPage.value < totalPages.value)
  const emptyState = computed(() => treks.value.length === 0 && !isLoading.value)

  // ACTIONS - Fetch Treks
  const fetchAvailableTreks = async (pageNum = 1) => {
    isLoading.value = true
    error.value = null
    
    try {
      const params = {
        page: pageNum,
        per_page: filters.value.per_page,
        ...(filters.value.difficulty && { difficulty: filters.value.difficulty }),
        ...(filters.value.location && { location: filters.value.location }),
        ...(filters.value.duration_min && { duration_min: filters.value.duration_min }),
        ...(filters.value.duration_max && { duration_max: filters.value.duration_max }),
        sort_by: filters.value.sort_by
      }

      const response = await api.get('/user/available-treks', { params })
      
      treks.value = response.data.treks
      totalPages.value = response.data.pages
      currentPage.value = pageNum
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch treks'
      throw error.value
    } finally {
      isLoading.value = false
    }
  }

  // ACTIONS - Get Trek Details
  const fetchTrekDetails = async (trekId) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.get(`/user/treks/${trekId}`)
      currentTrek.value = response.data.trek
      return response.data.trek
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch trek details'
      throw error.value
    } finally {
      isLoading.value = false
    }
  }

  // ACTIONS - Apply Filters & Reset to Page 1
  const applyFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters, page: 1 }
    return fetchAvailableTreks(1)
  }

  // ACTIONS - Book Trek
  const bookTrek = async (trekId) => {
    error.value = null
    
    try {
      const response = await api.post('/user/book-trek', { trek_id: trekId })
      
      // Update local trek to reflect booking
      if (currentTrek.value && currentTrek.value.id === trekId) {
        currentTrek.value.is_booked_by_user = true
        currentTrek.value.available_slots -= 1
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to book trek'
      throw error.value
    }
  }

  // ACTIONS - Reset State
  const reset = () => {
    treks.value = []
    currentTrek.value = null
    error.value = null
  }

  return {
    // State
    treks,
    currentTrek,
    totalPages,
    currentPage,
    isLoading,
    error,
    filters,
    
    // Computed
    hasMorePages,
    emptyState,
    
    // Actions
    fetchAvailableTreks,
    fetchTrekDetails,
    applyFilters,
    bookTrek,
    reset
  }
})
