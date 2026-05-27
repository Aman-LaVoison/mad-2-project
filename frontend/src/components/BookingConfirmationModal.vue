<template>
  <div class="modal show d-block" style="background-color: rgba(0, 0, 0, 0.5);">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <!-- HEADER -->
        <div class="modal-header bg-primary text-white">
          <h5 class="modal-title">Confirm Booking</h5>
          <button @click="$emit('cancel')" type="button" class="btn-close btn-close-white"></button>
        </div>

        <!-- CONTENT -->
        <div class="modal-body">
          <div class="alert alert-info mb-3">
            <i class="bi bi-info-circle"></i>
            You are about to book the following trek:
          </div>

          <!-- TREK INFO SUMMARY -->
          <div class="card mb-3 border-light">
            <div class="card-body">
              <h6 class="card-title mb-2">{{ trek.trek_name }}</h6>
              <div class="row small mb-2">
                <div class="col-6">
                  <p class="text-muted mb-1">Location</p>
                  <p>{{ trek.location }}</p>
                </div>
                <div class="col-6">
                  <p class="text-muted mb-1">Difficulty</p>
                  <p>
                    <span :class="difficultyClass" class="badge">
                      {{ trek.difficulty }}
                    </span>
                  </p>
                </div>
              </div>

              <div class="row small">
                <div class="col-6">
                  <p class="text-muted mb-1">Duration</p>
                  <p>{{ trek.duration_days }} days</p>
                </div>
                <div class="col-6">
                  <p class="text-muted mb-1">Price</p>
                  <p class="text-success fw-bold">₹{{ formatPrice(trek.price) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- BOOKING DETAILS -->
          <div class="border-top pt-3">
            <h6>Booking Summary</h6>
            <div class="row mb-2">
              <div class="col-6">Start Date</div>
              <div class="col-6 text-end">{{ formatDate(trek.start_date) }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-6">End Date</div>
              <div class="col-6 text-end">{{ formatDate(trek.end_date) }}</div>
            </div>
            <div class="row">
              <div class="col-6">Amount</div>
              <div class="col-6 text-end fw-bold text-success">₹{{ formatPrice(trek.price) }}</div>
            </div>
          </div>

          <!-- CHECKBOX AGREEMENT -->
          <div class="form-check mt-3">
            <input
              v-model="agreeTerms"
              class="form-check-input"
              type="checkbox"
              id="agree"
            />
            <label class="form-check-label" for="agree">
              I agree to the terms and conditions
            </label>
          </div>

          <!-- ERROR MESSAGE -->
          <div v-if="error" class="alert alert-danger mt-3 mb-0">
            {{ error }}
          </div>
        </div>

        <!-- FOOTER -->
        <div class="modal-footer">
          <button
            @click="$emit('cancel')"
            type="button"
            class="btn btn-outline-secondary"
          >
            Cancel
          </button>
          <button
            @click="handleConfirm"
            :disabled="!agreeTerms || isConfirming"
            type="button"
            class="btn btn-success"
          >
            <i v-if="isConfirming" class="spinner-border spinner-border-sm me-2"></i>
            <span v-if="!isConfirming"><i class="bi bi-check-circle"></i> Confirm Booking</span>
            <span v-else>Processing...</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  trek: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['confirm', 'cancel'])

const agreeTerms = ref(false)
const isConfirming = ref(false)
const error = ref(null)

const difficultyClass = computed(() => {
  const difficulty = props.trek.difficulty
  if (difficulty === 'Easy') return 'bg-success'
  if (difficulty === 'Moderate') return 'bg-warning text-dark'
  if (difficulty === 'Hard') return 'bg-danger'
  return 'bg-secondary'
})

const formatDate = (isoString) => {
  return new Date(isoString).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatPrice = (price) => {
  return price.toLocaleString('en-IN')
}

const handleConfirm = async () => {
  if (!agreeTerms.value) return
  
  isConfirming.value = true
  error.value = null
  
  try {
    emit('confirm')
  } catch (err) {
    error.value = err
  } finally {
    isConfirming.value = false
  }
}
</script>

<style scoped>
.modal.show {
  display: block;
}
</style>
