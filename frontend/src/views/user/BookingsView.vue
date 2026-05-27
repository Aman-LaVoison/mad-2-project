<template>
  <div class="container py-4">
    <!-- HEADER -->
    <div class="mb-4">
      <h2>My Bookings</h2>
      <p class="text-muted">View and manage all your trek bookings</p>
    </div>

    <!-- LOADING STATE -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2 text-muted">Fetching your bookings...</p>
    </div>

    <!-- ERROR STATE -->
    <div v-else-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
      <i class="bi bi-exclamation-triangle"></i>
      {{ error }}
      <button type="button" class="btn-close" @click="error = null"></button>
    </div>

    <!-- EMPTY STATE -->
    <div v-else-if="bookings.length === 0" class="alert alert-info">
      <i class="bi bi-info-circle"></i>
      You haven't booked any treks yet. <router-link to="/user/treks">Browse available treks</router-link>
    </div>

    <!-- BOOKINGS TABLE -->
    <div v-else class="table-responsive">
      <table class="table table-hover">
        <thead class="table-light">
          <tr>
            <th>Trek Name</th>
            <th>Location</th>
            <th>Booking Date</th>
            <th>Trek Dates</th>
            <th>Status</th>
            <th>Amount</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in bookings" :key="booking.id">
            <td class="fw-bold">{{ booking.trek_name }}</td>
            <td>{{ booking.location }}</td>
            <td>{{ formatDate(booking.booking_date) }}</td>
            <td class="small">
              {{ formatDate(booking.start_date) }} to {{ formatDate(booking.end_date) }}
            </td>
            <td>
              <span :class="getStatusBadge(booking.booking_status)" class="badge">
                {{ booking.booking_status }}
              </span>
            </td>
            <td class="text-success fw-bold">₹{{ formatPrice(booking.amount_paid) }}</td>
            <td>
              <div class="btn-group btn-group-sm">
                <button @click="viewBookingDetails(booking)" class="btn btn-info">
                  <i class="bi bi-eye"></i>
                </button>
                <button
                  v-if="booking.booking_status === 'Booked'"
                  @click="cancelBooking(booking)"
                  class="btn btn-danger"
                >
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- PAGINATION -->
    <nav v-if="totalPages > 1" class="d-flex justify-content-center mt-4">
      <ul class="pagination">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <button @click="loadBookings(currentPage - 1)" class="page-link">Previous</button>
        </li>
        <li
          v-for="page in pageNumbers"
          :key="page"
          class="page-item"
          :class="{ active: page === currentPage }"
        >
          <button @click="loadBookings(page)" class="page-link">{{ page }}</button>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <button @click="loadBookings(currentPage + 1)" class="page-link">Next</button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../services/api'
import { useToast } from '../../composables/useToast'

const router = useRouter()
const toast = useToast()

const bookings = ref([])
const isLoading = ref(false)
const error = ref(null)
const currentPage = ref(1)
const totalPages = ref(1)

const pageNumbers = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const pages = []
  
  const start = Math.max(1, current - 2)
  const end = Math.min(total, current + 2)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

const formatDate = (isoString) => {
  if (!isoString) return 'N/A'
  return new Date(isoString).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatPrice = (price) => {
  return price ? price.toLocaleString('en-IN') : '0'
}

const getStatusBadge = (status) => {
  const statusMap = {
    'Booked': 'bg-success',
    'Cancelled': 'bg-danger',
    'Completed': 'bg-info'
  }
  return statusMap[status] || 'bg-secondary'
}

const loadBookings = async (page = 1) => {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await api.get('/user/bookings', {
      params: { page, per_page: 10 }
    })
    
    bookings.value = response.data.bookings
    totalPages.value = response.data.pages
    currentPage.value = page
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to load bookings'
  } finally {
    isLoading.value = false
  }
}

const viewBookingDetails = (booking) => {
  toast.info(`Booking ID: ${booking.id} - Status: ${booking.booking_status}`)
}

const cancelBooking = async (booking) => {
  if (!confirm(`Are you sure you want to cancel this booking for ${booking.trek_name}?`)) {
    return
  }
  
  try {
    await api.post(`/user/bookings/${booking.id}/cancel`, {
      cancellation_reason: 'User initiated cancellation'
    })
    
    toast.success('Booking cancelled successfully')
    await loadBookings(currentPage.value)
  } catch (err) {
    toast.error(err.response?.data?.error || 'Failed to cancel booking')
  }
}

onMounted(() => {
  loadBookings(1)
})
</script>

<style scoped>
.table {
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.btn-group-sm .btn {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>
