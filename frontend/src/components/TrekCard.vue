<template>
  <div class="card trek-card h-100 shadow-sm">
    <!-- CARD IMAGE PLACEHOLDER -->
    <div class="card-img-top bg-light d-flex align-items-center justify-content-center" style="height: 200px">
      <i class="bi bi-mountains text-muted" style="font-size: 3rem;"></i>
    </div>

    <div class="card-body d-flex flex-column">
      <!-- TREK NAME -->
      <h5 class="card-title">{{ trek.trek_name }}</h5>

      <!-- QUICK INFO BADGES -->
      <div class="mb-3">
        <span class="badge bg-success me-2">
          <i class="bi bi-geo-alt"></i> {{ trek.location }}
        </span>
        <span :class="difficultyClass" class="badge me-2">
          {{ trek.difficulty }}
        </span>
        <span class="badge bg-info">
          <i class="bi bi-calendar"></i> {{ trek.duration_days }}d
        </span>
      </div>

      <!-- TREK STATS -->
      <div class="mb-3 small text-muted">
        <div class="mb-1">
          <i class="bi bi-calendar3"></i>
          {{ formatDate(trek.start_date) }} to {{ formatDate(trek.end_date) }}
        </div>
        <div>
          <i class="bi bi-people"></i>
          <span :class="{ 'text-danger': trek.available_slots < 3 }">
            {{ trek.available_slots }} / {{ trek.total_slots }} slots
          </span>
        </div>
      </div>

      <!-- PRICE & DESCRIPTION PREVIEW -->
      <p class="card-text small flex-grow-1">
        {{ truncateText(trek.description, 80) }}
      </p>

      <!-- PRICE -->
      <div class="mb-3 border-top pt-2">
        <span class="h5 text-success">₹{{ formatPrice(trek.price) }}</span>
      </div>

      <!-- ACTIONS -->
      <div class="d-grid gap-2">
        <button @click="emitViewDetails" class="btn btn-outline-primary btn-sm">
          <i class="bi bi-eye"></i> View Details
        </button>
        <button
          @click="emitBook"
          :disabled="trek.available_slots === 0"
          class="btn btn-success btn-sm"
        >
          <i class="bi bi-check-circle"></i> Book Now
        </button>
      </div>

      <!-- SLOTS WARNING -->
      <small v-if="trek.available_slots < 3" class="text-danger mt-2">
        ⚠️ Only {{ trek.available_slots }} slot(s) left!
      </small>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  trek: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['view-details', 'book'])

// COMPUTED
const difficultyClass = computed(() => {
  const difficultyMap = {
    'Easy': 'bg-success',
    'Moderate': 'bg-warning',
    'Hard': 'bg-danger'
  }
  return difficultyMap[props.trek.difficulty] || 'bg-secondary'
})

// METHODS
const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  return new Date(dateStr).toLocaleDateString('en-IN', { 
    day: 'short', 
    month: 'short', 
    year: 'numeric' 
  })
}

const formatPrice = (price) => {
  return price ? price.toLocaleString('en-IN') : '0'
}

const truncateText = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

const emitViewDetails = () => {
  emit('view-details', props.trek.id)
}

const emitBook = () => {
  emit('book', props.trek)
}
</script>

<style scoped>
.trek-card {
  border: 1px solid #e0e0e0;
  transition: transform 0.2s, box-shadow 0.2s;
}

.trek-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}

.card-title {
  color: #2c3e50;
  font-weight: 600;
}

.badge {
  font-weight: 500;
  font-size: 0.75rem;
}

.btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}
</style>
