<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-6">
        <!-- HEADER -->
        <div class="mb-4">
          <h2>My Profile</h2>
          <p class="text-muted">Manage your personal information</p>
        </div>

        <!-- LOADING STATE -->
        <div v-if="profileStore.isLoading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <!-- PROFILE FORM -->
        <div v-else class="card">
          <div class="card-body">
            <!-- ERROR MESSAGE -->
            <div v-if="profileStore.error" class="alert alert-danger alert-dismissible fade show">
              <i class="bi bi-exclamation-triangle"></i>
              {{ profileStore.error }}
              <button type="button" class="btn-close" @click="profileStore.error = null"></button>
            </div>

            <!-- SUCCESS MESSAGE -->
            <div v-if="showSuccess" class="alert alert-success alert-dismissible fade show">
              <i class="bi bi-check-circle"></i>
              Profile updated successfully!
              <button type="button" class="btn-close" @click="showSuccess = false"></button>
            </div>

            <!-- FORM -->
            <form @submit.prevent="handleSubmit">
              <!-- USERNAME (READ-ONLY) -->
              <div class="mb-3">
                <label class="form-label fw-bold">Username</label>
                <input
                  type="text"
                  class="form-control"
                  :value="profileStore.profile?.username"
                  disabled
                />
                <small class="text-muted">Cannot be changed</small>
              </div>

              <!-- EMAIL (READ-ONLY) -->
              <div class="mb-3">
                <label class="form-label fw-bold">Email</label>
                <input
                  type="email"
                  class="form-control"
                  :value="profileStore.profile?.email"
                  disabled
                />
                <small class="text-muted">Cannot be changed</small>
              </div>

              <!-- FULL NAME -->
              <div class="mb-3">
                <label for="fullName" class="form-label fw-bold">Full Name *</label>
                <input
                  id="fullName"
                  v-model="formData.full_name"
                  type="text"
                  class="form-control"
                  :class="{ 'is-invalid': errors.full_name }"
                  placeholder="Enter your full name"
                />
                <div v-if="errors.full_name" class="invalid-feedback d-block">
                  {{ errors.full_name }}
                </div>
              </div>

              <!-- PHONE -->
              <div class="mb-3">
                <label for="phone" class="form-label fw-bold">Phone Number</label>
                <input
                  id="phone"
                  v-model="formData.phone"
                  type="tel"
                  class="form-control"
                  :class="{ 'is-invalid': errors.phone }"
                  placeholder="e.g., +91-9876543210"
                />
                <div v-if="errors.phone" class="invalid-feedback d-block">
                  {{ errors.phone }}
                </div>
              </div>

              <!-- ADDRESS -->
              <div class="mb-3">
                <label for="address" class="form-label fw-bold">Address</label>
                <textarea
                  id="address"
                  v-model="formData.address"
                  class="form-control"
                  :class="{ 'is-invalid': errors.address }"
                  rows="3"
                  placeholder="Enter your address"
                ></textarea>
                <div v-if="errors.address" class="invalid-feedback d-block">
                  {{ errors.address }}
                </div>
              </div>

              <!-- DATE OF BIRTH -->
              <div class="mb-3">
                <label for="dob" class="form-label fw-bold">Date of Birth</label>
                <input
                  id="dob"
                  v-model="formData.date_of_birth"
                  type="date"
                  class="form-control"
                  :class="{ 'is-invalid': errors.date_of_birth }"
                />
                <div v-if="errors.date_of_birth" class="invalid-feedback d-block">
                  {{ errors.date_of_birth }}
                </div>
              </div>

              <!-- MEMBER SINCE (READ-ONLY) -->
              <div class="mb-3">
                <label class="form-label fw-bold">Member Since</label>
                <input
                  type="text"
                  class="form-control"
                  :value="formatDate(profileStore.profile?.created_at)"
                  disabled
                />
              </div>

              <!-- PROFILE COMPLETION -->
              <div class="alert alert-info mb-3">
                <i class="bi bi-info-circle"></i>
                <span v-if="profileStore.profile?.profile_completed" class="ms-2">
                  <strong>Your profile is complete!</strong>
                </span>
                <span v-else class="ms-2">
                  <strong>Please complete your profile</strong> to improve your trek experience.
                </span>
              </div>

              <!-- ACTION BUTTONS -->
              <div class="d-flex gap-2">
                <button
                  type="submit"
                  :disabled="profileStore.isSaving || !isFormDirty"
                  class="btn btn-primary flex-grow-1"
                >
                  <i v-if="profileStore.isSaving" class="spinner-border spinner-border-sm me-2"></i>
                  <span v-if="!profileStore.isSaving"><i class="bi bi-check-circle"></i> Save Changes</span>
                  <span v-else>Saving...</span>
                </button>
                <button
                  type="button"
                  @click="handleReset"
                  class="btn btn-outline-secondary"
                >
                  <i class="bi bi-arrow-clockwise"></i> Reset
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- ADDITIONAL INFO CARD -->
        <div class="card mt-4">
          <div class="card-header bg-light">
            <h5 class="mb-0">Account Information</h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6">
                <p class="small text-muted mb-1">User Type</p>
                <p class="fw-bold">
                  <span class="badge bg-info">{{ profileStore.profile?.user_type || 'User' }}</span>
                </p>
              </div>
              <div class="col-md-6">
                <p class="small text-muted mb-1">Account Status</p>
                <p class="fw-bold">
                  <span class="badge bg-success">Active</span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { useUserProfileStore } from '../../store/userProfile'
import { useToast } from '../../composables/useToast'

const profileStore = useUserProfileStore()
const toast = useToast()

// FORM STATE
const formData = reactive({
  full_name: '',
  phone: '',
  address: '',
  date_of_birth: ''
})

const originalData = reactive({
  full_name: '',
  phone: '',
  address: '',
  date_of_birth: ''
})

const errors = reactive({
  full_name: null,
  phone: null,
  address: null,
  date_of_birth: null
})

const showSuccess = ref(false)

// COMPUTED
const isFormDirty = computed(() => {
  return Object.keys(formData).some(
    key => formData[key] !== originalData[key]
  )
})

// METHODS
const formatDate = (isoString) => {
  if (!isoString) return 'N/A'
  return new Date(isoString).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const loadProfile = async () => {
  try {
    await profileStore.fetchProfile()
    populateForm()
  } catch (err) {
    toast.error('Failed to load profile')
  }
}

const populateForm = () => {
  const profile = profileStore.profile
  if (!profile) return

  formData.full_name = profile.full_name || ''
  formData.phone = profile.phone || ''
  formData.address = profile.address || ''
  formData.date_of_birth = profile.date_of_birth ? profile.date_of_birth.split('T')[0] : ''

  Object.assign(originalData, formData)
}

const validateForm = () => {
  Object.keys(errors).forEach(key => {
    errors[key] = null
  })

  let isValid = true

  if (!formData.full_name || formData.full_name.trim().length === 0) {
    errors.full_name = 'Full name is required'
    isValid = false
  }

  if (formData.phone && !/^[0-9+\-\s()]+$/.test(formData.phone)) {
    errors.phone = 'Invalid phone number format'
    isValid = false
  }

  if (formData.date_of_birth) {
    const dob = new Date(formData.date_of_birth)
    const today = new Date()
    const age = today.getFullYear() - dob.getFullYear()

    if (age < 13) {
      errors.date_of_birth = 'You must be at least 13 years old'
      isValid = false
    }
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  try {
    await profileStore.updateProfile({
      full_name: formData.full_name,
      phone: formData.phone,
      address: formData.address,
      date_of_birth: formData.date_of_birth || null
    })

    showSuccess.value = true
    setTimeout(() => {
      showSuccess.value = false
    }, 3000)

    Object.assign(originalData, formData)
    toast.success('Profile updated successfully')
  } catch (err) {
    toast.error(err)
  }
}

const handleReset = () => {
  Object.assign(formData, originalData)
}

// LIFECYCLE
onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.form-label {
  margin-bottom: 0.5rem;
}

.invalid-feedback {
  font-size: 0.875rem;
}
</style>
