<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h3>Previous Treks</h3>
        <p class="text-muted">A history of completed and past trek bookings.</p>
      </div>
    </div>

    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-if="treks.length === 0 && !isLoading" class="alert alert-info">
      No previous treks found. Your upcoming adventures will appear once they are completed.
    </div>

    <div class="row">
      <div class="col-md-6 mb-4" v-for="trek in treks" :key="trek.id">
        <div class="card h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">{{ trek.trek_name }}</h5>
            <p class="text-muted mb-1">{{ trek.location }} • {{ trek.difficulty }}</p>
            <p class="mb-2">{{ trek.duration_days }} days • ₹{{ trek.price }}</p>
            <p class="small text-muted mb-2">{{ formatDate(trek.start_date) }} - {{ formatDate(trek.end_date) }}</p>
            <p class="card-text">{{ trek.description }}</p>
            <span class="badge bg-secondary">{{ trek.booking_status }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

export default {
  name: 'PreviousTreksView',

  setup() {
    const treks = ref([])
    const isLoading = ref(false)
    const error = ref(null)

    const fetchPreviousTreks = async () => {
      isLoading.value = true
      error.value = null
      try {
        const response = await api.get('/user/dashboard/previous-treks')
        treks.value = response.data.previous_treks
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to load previous treks.'
      } finally {
        isLoading.value = false
      }
    }

    const formatDate = (value) => {
      if (!value) return 'N/A'
      return new Date(value).toLocaleDateString('en-IN', { day: 'short', month: 'short', year: 'numeric' })
    }

    onMounted(fetchPreviousTreks)

    return { treks, isLoading, error, formatDate }
  }
}
</script>
