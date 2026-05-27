<template>
  <div class="container-fluid py-4">
    <div class="row">
      <!-- SIDEBAR: FILTERS -->
      <div class="col-md-3">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Filters</h5>
          </div>
          <div class="card-body">
            <!-- Search by Location -->
            <div class="mb-3">
              <label class="form-label fw-bold">Location</label>
              <input
                v-model="filterForm.location"
                type="text"
                class="form-control form-control-sm"
                placeholder="e.g., Himalayas"
              />
            </div>

            <!-- Difficulty Filter -->
            <div class="mb-3">
              <label class="form-label fw-bold">Difficulty</label>
              <select v-model="filterForm.difficulty" class="form-select form-select-sm">
                <option value="">All Levels</option>
                <option value="Easy">Easy</option>
                <option value="Moderate">Moderate</option>
                <option value="Hard">Hard</option>
              </select>
            </div>

            <!-- Duration Filter -->
            <div class="mb-3">
              <label class="form-label fw-bold">Duration (Days)</label>
              <div class="row g-2">
                <div class="col-6">
                  <input
                    v-model.number="filterForm.duration_min"
                    type="number"
                    class="form-control form-control-sm"
                    placeholder="Min"
                    min="1"
                  />
                </div>
                <div class="col-6">
                  <input
                    v-model.number="filterForm.duration_max"
                    type="number"
                    class="form-control form-control-sm"
                    placeholder="Max"
                    min="1"
                  />
                </div>
              </div>
            </div>

            <!-- Sort Filter -->
            <div class="mb-3">
              <label class="form-label fw-bold">Sort By</label>
              <select v-model="filterForm.sort_by" class="form-select form-select-sm">
                <option value="start_date">Start Date</option>
                <option value="difficulty">Difficulty</option>
              </select>
            </div>

            <!-- Action Buttons -->
            <div class="d-grid gap-2">
              <button @click="handleApplyFilters" class="btn btn-primary btn-sm">
                <i class="bi bi-funnel"></i> Apply Filters
              </button>
              <button @click="handleResetFilters" class="btn btn-outline-secondary btn-sm">
                <i class="bi bi-arrow-clockwise"></i> Reset
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- MAIN: TREK LIST -->
      <div class="col-md-9">
        <!-- HEADER -->
        <div class="mb-4">
          <h2>Available Treks</h2>
          <p class="text-muted">
            {{ trekStore.treks.length }} trek(s) found
            <span v-if="activeFilters">• Filters applied</span>
          </p>
        </div>

        <!-- LOADING STATE -->
        <div v-if="trekStore.isLoading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="mt-2 text-muted">Fetching treks...</p>
        </div>

        <!-- ERROR STATE -->
        <div v-else-if="trekStore.error" class="alert alert-danger alert-dismissible fade show" role="alert">
          <i class="bi bi-exclamation-triangle"></i>
          {{ trekStore.error }}
          <button type="button" class="btn-close" @click="trekStore.error = null"></button>
        </div>

        <!-- EMPTY STATE -->
        <div v-else-if="trekStore.emptyState" class="alert alert-info">
          <i class="bi bi-info-circle"></i>
          No treks available. Try adjusting your filters!
        </div>

        <!-- TREK CARDS -->
        <div v-else class="row row-cols-1 row-cols-md-2 g-4">
          <div
            v-for="trek in trekStore.treks"
            :key="trek.id"
            class="col"
          >
            <TrekCard
              :trek="trek"
              @view-details="handleViewDetails"
              @book="handleBookClick"
            />
          </div>
        </div>

        <!-- PAGINATION -->
        <nav v-if="trekStore.totalPages > 1" class="mt-5 d-flex justify-content-center">
          <ul class="pagination">
            <li class="page-item" :class="{ disabled: trekStore.currentPage === 1 }">
              <button
                @click="handlePageChange(trekStore.currentPage - 1)"
                class="page-link"
                :disabled="trekStore.currentPage === 1"
              >
                Previous
              </button>
            </li>

            <li
              v-for="page in pageNumbers"
              :key="page"
              class="page-item"
              :class="{ active: page === trekStore.currentPage }"
            >
              <button @click="handlePageChange(page)" class="page-link">
                {{ page }}
              </button>
            </li>

            <li class="page-item" :class="{ disabled: !trekStore.hasMorePages }">
              <button
                @click="handlePageChange(trekStore.currentPage + 1)"
                class="page-link"
                :disabled="!trekStore.hasMorePages"
              >
                Next
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <!-- DETAIL MODAL -->
    <TrekDetailModal
      v-if="selectedTrekId"
      :trek-id="selectedTrekId"
      @close="selectedTrekId = null"
      @book="handleBookFromModal"
    />

    <!-- BOOKING CONFIRMATION MODAL -->
    <BookingConfirmationModal
      v-if="showBookingModal"
      :trek="bookingTrek"
      @confirm="handleConfirmBooking"
      @cancel="showBookingModal = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTrekStore } from '../../store/treks'
import TrekCard from '../../components/TrekCard.vue'
import TrekDetailModal from '../../components/TrekDetailModal.vue'
import BookingConfirmationModal from '../../components/BookingConfirmationModal.vue'
import { useToast } from '../../composables/useToast'

const trekStore = useTrekStore()
const toast = useToast()

// LOCAL STATE
const filterForm = ref({
  location: null,
  difficulty: null,
  duration_min: null,
  duration_max: null,
  sort_by: 'start_date'
})

const selectedTrekId = ref(null)
const showBookingModal = ref(false)
const bookingTrek = ref(null)

// COMPUTED
const activeFilters = computed(() => {
  return filterForm.value.location ||
         filterForm.value.difficulty ||
         filterForm.value.duration_min ||
         filterForm.value.duration_max
})

const pageNumbers = computed(() => {
  const total = trekStore.totalPages
  const current = trekStore.currentPage
  const pages = []
  
  const start = Math.max(1, current - 2)
  const end = Math.min(total, current + 2)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

// HANDLERS
const handleApplyFilters = async () => {
  try {
    await trekStore.applyFilters(filterForm.value)
    toast.success('Filters applied')
  } catch (err) {
    // Error already in store
  }
}

const handleResetFilters = async () => {
  filterForm.value = {
    location: null,
    difficulty: null,
    duration_min: null,
    duration_max: null,
    sort_by: 'start_date'
  }
  try {
    await trekStore.fetchAvailableTreks(1)
    toast.success('Filters reset')
  } catch (err) {
    // Error already in store
  }
}

const handlePageChange = async (page) => {
  try {
    await trekStore.fetchAvailableTreks(page)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } catch (err) {
    // Error already in store
  }
}

const handleViewDetails = (trekId) => {
  selectedTrekId.value = trekId
}

const handleBookClick = (trek) => {
  bookingTrek.value = trek
  showBookingModal.value = true
}

const handleBookFromModal = (trek) => {
  bookingTrek.value = trek
  showBookingModal.value = true
}

const handleConfirmBooking = async () => {
  try {
    await trekStore.bookTrek(bookingTrek.value.id)
    showBookingModal.value = false
    const trekName = bookingTrek.value?.trek_name
    bookingTrek.value = null
    toast.success(`Successfully booked: ${trekName}`)
    
    await trekStore.fetchAvailableTreks(trekStore.currentPage)
  } catch (err) {
    toast.error(err)
  }
}

// LIFECYCLE
onMounted(async () => {
  try {
    await trekStore.fetchAvailableTreks(1)
  } catch (err) {
    // Error handled in store
  }
})
</script>

<style scoped>
.pagination {
  margin: 0;
}

.card {
  border: 1px solid #dee2e6;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}
</style>
