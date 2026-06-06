<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h3>Trek Vouchers</h3>
        <p class="text-muted">Your valid vouchers and discounts available for booking.</p>
      </div>
    </div>

    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-if="vouchers.length === 0 && !isLoading" class="alert alert-info">
      No vouchers found. Complete bookings or stay tuned for upcoming offers.
    </div>

    <div class="row">
      <div class="col-md-6 mb-4" v-for="voucher in vouchers" :key="voucher.id">
        <div class="card h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">{{ voucher.code }}</h5>
            <p class="text-muted mb-2">{{ voucher.description || 'Voucher available for your next booking' }}</p>
            <p class="mb-2"><strong>Discount:</strong> {{ voucher.discount }}%</p>
            <p class="small text-muted mb-0">
              Valid from {{ formatDate(voucher.valid_from) }}
              <span v-if="voucher.valid_until">to {{ formatDate(voucher.valid_until) }}</span>
            </p>
            <p class="mt-2"><span class="badge" :class="voucher.status === 'active' ? 'bg-success' : 'bg-secondary'">{{ voucher.status }}</span></p>
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
  name: 'TrekVouchersView',

  setup() {
    const vouchers = ref([])
    const isLoading = ref(false)
    const error = ref(null)

    const fetchVouchers = async () => {
      isLoading.value = true
      error.value = null
      try {
        const response = await api.get('/user/dashboard/vouchers')
        vouchers.value = response.data.vouchers
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to load vouchers.'
      } finally {
        isLoading.value = false
      }
    }

    const formatDate = (value) => {
      if (!value) return 'N/A'
      return new Date(value).toLocaleDateString('en-IN', { day: 'short', month: 'short', year: 'numeric' })
    }

    onMounted(fetchVouchers)

    return { vouchers, isLoading, error, formatDate }
  }
}
</script>
