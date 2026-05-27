<template>
  <div class="modal show d-block" style="background-color: rgba(0, 0, 0, 0.5);">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <!-- HEADER -->
        <div class="modal-header">
          <h5 class="modal-title">Trek Details</h5>
          <button @click="$emit('close')" type="button" class="btn-close"></button>
        </div>

        <!-- LOADING -->
        <div v-if="isLoading" class="modal-body text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <!-- CONTENT -->
        <div v-else-if="trek">
          <div class="modal-body">
            <!-- TITLE & BADGES -->
            <h4 class="mb-3">{{ trek.trek_name }}</h4>
            <div class="mb-3">
              <span class="badge bg-success me-2">
                <i class="bi bi-geo-alt"></i> {{ trek.location }}
              </span>
              <span :class="difficultyClass" class="badge me-2">
                {{ trek.difficulty }}
              </span>
              <span class="badge bg-info">
                <i class="bi bi-calendar"></i> {{ trek.duration_days }} days
              </span>
            </div>

            <!-- TWO COLUMN INFO -->
            <div class="row mb-3">
              <div class="col-md-6">
                <p class="small text-muted mb-1">Start Date</p>
                <p class="fw-bold">{{ formatDate(trek.start_date) }}</p>
              </div>
              <div class="col-md-6">
                <p class="small text-muted mb-1">End Date</p>
                <p class="fw-bold">{{ formatDate(trek.end_date) }}</p>
              </div>
              <div class="col-md-6">
                <p class="small text-muted mb-1">Altitude</p>
                <p class="fw-bold">{{ trek.altitude || 'N/A' }} m</p>
              </div>
              <div class="col-md-6">
                <p class="small text-muted mb-1">Best Season</p>
                <p class="fw-bold">{{ trek.best_season || 'N/A' }}</p>
              </div>
            </div>

            <!-- DESCRIPTION -->
            <div class="mb-3">
              <h6>About This Trek</h6>
              <p>{{ trek.description }}</p>
            </div>

            <!-- ACCOMMODATION -->
            <div class="mb-3">
              <h6>Accommodation</h6>
              <p>{{ trek.accommodation || 'Not specified' }}</p>
            </div>

            <!-- ITINERARY -->
            <div class="mb-3">
              <h6>Itinerary</h6>
              <p class="small">{{ trek.itinerary || 'Detailed itinerary available upon request' }}</p>
            </div>

            <!-- SLOTS & PRICE -->
            <div class="alert alert-light border">
              <div class="row">
                <div class="col-6">
                  <p class="small text-muted mb-1">Available Slots</p>
                  <p class="h5" :class="trek.available_slots < 3 ? 'text-danger' : 'text-success'">
                    {{ trek.available_slots }} / {{ trek.total_slots }}
                  </p>
                </div>
                <div class="col-6">
                  <p class="small text-muted mb-1">Price</p>
                  <p class="h5 text-success">₹{{ formatPrice(trek.price) }}</p>
                </div>
              </div>
            </div>

            <!-- BOOKING STATUS -->
            <div v-if="trek.is_booked_by_user" class="alert alert-success">
              <i class="bi bi-check-circle-fill"></i>
              You have already booked this trek (Status: {{ trek.booking_status }})
            </div>
          </div>

          <!-- FOOTER -->
          <div class="modal-footer">
            <button @click="$emit('close')" type="button" class="btn btn-secondary">
              Close
            </button>
            <button
              v-if="!trek.is_booked_by_user && trek.available_slots > 0"
              @click="$emit('book', trek)"
              type="button"
              class="btn btn-primary"
            >
              <i class="bi bi-check-circle"></i> Book This Trek
            </button>
          </div>
        </div>

        <!-- ERROR -->
        <div v-else class="modal-body">
          <div class="alert alert-danger">Failed to load trek details</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useTrekStore } from '../store/treks'

const props = defineProps({
  trekId: {
    type: Number,
    required: true
  }
})

defineEmits(['close', 'book'])

const trekStore = useTrekStore()
const trek = computed(() => trekStore.currentTrek)
const isLoading = computed(() => trekStore.isLoading)

const difficultyClass = computed(() => {
  if (!trek.value) return 'bg-secondary'
  const difficulty = trek.value.difficulty
  if (difficulty === 'Easy') return 'bg-success'
  if (difficulty === 'Moderate') return 'bg-warning text-dark'
  if (difficulty === 'Hard') return 'bg-danger'
  return 'bg-secondary'
})

const formatDate = (isoString) => {
  return new Date(isoString).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatPrice = (price) => {
  return price.toLocaleString('en-IN')
}

onMounted(async () => {
  try {
    await trekStore.fetchTrekDetails(props.trekId)
  } catch (err) {
    // Error handled in store
  }
})
</script>

<style scoped>
.modal.show {
  display: block;
}
</style>
