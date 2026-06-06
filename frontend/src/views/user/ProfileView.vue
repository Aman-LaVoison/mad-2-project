<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <div class="mb-4">
          <h2>My Profile</h2>
          <p class="text-muted">Update your profile information as part of the dashboard experience.</p>
        </div>

        <div v-if="isLoading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <div v-else>
          <div v-if="error" class="alert alert-danger alert-dismissible fade show">
            <i class="bi bi-exclamation-triangle"></i>
            {{ error }}
            <button type="button" class="btn-close" @click="error = null"></button>
          </div>

          <div v-if="showSuccess" class="alert alert-success alert-dismissible fade show">
            <i class="bi bi-check-circle"></i>
            Profile updated successfully!
            <button type="button" class="btn-close" @click="showSuccess = false"></button>
          </div>

          <div class="card mb-4">
            <div class="card-body">
              <form @submit.prevent="handleSubmit">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="firstName" class="form-label fw-bold">First Name</label>
                    <input id="firstName" v-model="formData.first_name" type="text" class="form-control" />
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="lastName" class="form-label fw-bold">Last Name</label>
                    <input id="lastName" v-model="formData.last_name" type="text" class="form-control" />
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="fullName" class="form-label fw-bold">Full Name *</label>
                    <input id="fullName" v-model="formData.full_name" type="text" class="form-control" :class="{ 'is-invalid': errors.full_name }" placeholder="Enter your full name" />
                    <div v-if="errors.full_name" class="invalid-feedback d-block">{{ errors.full_name }}</div>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="email" class="form-label fw-bold">Email</label>
                    <input id="email" :value="formData.email" disabled type="email" class="form-control" />
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="phone" class="form-label fw-bold">Phone</label>
                    <input id="phone" v-model="formData.phone" type="tel" class="form-control" :class="{ 'is-invalid': errors.phone }" placeholder="e.g. +91-9876543210" />
                    <div v-if="errors.phone" class="invalid-feedback d-block">{{ errors.phone }}</div>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="gender" class="form-label fw-bold">Gender</label>
                    <select id="gender" v-model="formData.gender" class="form-select">
                      <option value="">Select gender</option>
                      <option>Male</option>
                      <option>Female</option>
                      <option>Other</option>
                    </select>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="dob" class="form-label fw-bold">Date of Birth</label>
                    <input id="dob" v-model="formData.date_of_birth" type="date" class="form-control" :class="{ 'is-invalid': errors.date_of_birth }" />
                    <div v-if="errors.date_of_birth" class="invalid-feedback d-block">{{ errors.date_of_birth }}</div>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="nationality" class="form-label fw-bold">Nationality</label>
                    <input id="nationality" v-model="formData.nationality" type="text" class="form-control" />
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="company" class="form-label fw-bold">Company / College</label>
                    <input id="company" v-model="formData.company_or_college" type="text" class="form-control" />
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="designation" class="form-label fw-bold">Designation / Course</label>
                    <input id="designation" v-model="formData.designation_or_course" type="text" class="form-control" />
                  </div>
                </div>

                <div class="mb-3">
                  <label for="address" class="form-label fw-bold">Address</label>
                  <textarea id="address" v-model="formData.address" class="form-control" rows="3"></textarea>
                </div>

                <div class="row">
                  <div class="col-md-4 mb-3">
                    <label for="city" class="form-label fw-bold">City</label>
                    <input id="city" v-model="formData.city" type="text" class="form-control" />
                  </div>
                  <div class="col-md-4 mb-3">
                    <label for="state" class="form-label fw-bold">State</label>
                    <input id="state" v-model="formData.state" type="text" class="form-control" />
                  </div>
                  <div class="col-md-4 mb-3">
                    <label for="pinCode" class="form-label fw-bold">Pin Code</label>
                    <input id="pinCode" v-model="formData.pin_code" type="text" class="form-control" />
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="country" class="form-label fw-bold">Country</label>
                    <input id="country" v-model="formData.country" type="text" class="form-control" />
                  </div>
                  <div class="col-md-3 mb-3">
                    <label for="height" class="form-label fw-bold">Height (cm)</label>
                    <input id="height" v-model="formData.height_cm" type="number" class="form-control" />
                  </div>
                  <div class="col-md-3 mb-3">
                    <label for="weight" class="form-label fw-bold">Weight (kg)</label>
                    <input id="weight" v-model="formData.weight_kg" type="number" class="form-control" />
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="emergencyName" class="form-label fw-bold">Emergency Contact Name</label>
                    <input id="emergencyName" v-model="formData.emergency_contact_name" type="text" class="form-control" />
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="emergencyPhone" class="form-label fw-bold">Emergency Contact</label>
                    <input id="emergencyPhone" v-model="formData.emergency_contact" type="tel" class="form-control" />
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="emergencyEmail" class="form-label fw-bold">Emergency Email</label>
                    <input id="emergencyEmail" v-model="formData.emergency_email" type="email" class="form-control" />
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="relationship" class="form-label fw-bold">Relationship</label>
                    <input id="relationship" v-model="formData.emergency_relationship" type="text" class="form-control" />
                  </div>
                </div>

                <div class="mb-3">
                  <label for="foodPreference" class="form-label fw-bold">Food Preference</label>
                  <select id="foodPreference" v-model="formData.food_preference" class="form-select">
                    <option value="">Select preference</option>
                    <option>Vegetarian</option>
                    <option>Jain</option>
                    <option>Vegan</option>
                    <option>Gluten-Free</option>
                    <option>Lactose Intolerant</option>
                  </select>
                </div>

                <div class="mb-3">
                  <label for="foodAllergies" class="form-label fw-bold">Food Allergies</label>
                  <textarea id="foodAllergies" v-model="formData.food_allergies" class="form-control" rows="2" placeholder="No or specify allergies"></textarea>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="tshirtSize" class="form-label fw-bold">T-Shirt Size</label>
                    <input id="tshirtSize" v-model="formData.tshirt_size" type="text" class="form-control" placeholder="e.g. Large (L)" />
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="shoeSize" class="form-label fw-bold">Shoe Size</label>
                    <input id="shoeSize" v-model="formData.shoe_size" type="text" class="form-control" placeholder="e.g. UK 12" />
                  </div>
                </div>

                <div class="d-flex gap-2">
                  <button type="submit" :disabled="isSaving || !isFormDirty" class="btn btn-primary flex-grow-1">
                    <i v-if="isSaving" class="spinner-border spinner-border-sm me-2"></i>
                    <span v-if="!isSaving"><i class="bi bi-check-circle"></i> Save Changes</span>
                    <span v-else>Saving...</span>
                  </button>
                  <button type="button" @click="handleReset" class="btn btn-outline-secondary">Reset</button>
                </div>
              </form>
            </div>
          </div>

          <div class="card mt-4">
            <div class="card-header bg-light">
              <h5 class="mb-0">Account Information</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-md-6">
                  <p class="small text-muted mb-1">User Type</p>
                  <p class="fw-bold"><span class="badge bg-info">{{ formData.user_type || 'User' }}</span></p>
                </div>
                <div class="col-md-6">
                  <p class="small text-muted mb-1">Member Since</p>
                  <p class="fw-bold"><span>{{ formatDate(formData.created_at) }}</span></p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import api from '../../services/api'
import { useToast } from '../../composables/useToast'

const toast = useToast()
const isLoading = ref(false)
const isSaving = ref(false)
const error = ref(null)
const showSuccess = ref(false)

const formData = reactive({
  id: null,
  username: '',
  email: '',
  full_name: '',
  first_name: '',
  last_name: '',
  phone: '',
  address: '',
  date_of_birth: '',
  gender: '',
  nationality: '',
  company_or_college: '',
  designation_or_course: '',
  pin_code: '',
  city: '',
  state: '',
  country: '',
  height_cm: null,
  weight_kg: null,
  emergency_contact_name: '',
  emergency_contact: '',
  emergency_email: '',
  emergency_relationship: '',
  food_preference: '',
  food_allergies: '',
  tshirt_size: '',
  shoe_size: '',
  user_type: '',
  profile_completed: false,
  created_at: ''
})

const originalData = reactive({ ...formData })

const errors = reactive({
  full_name: null,
  phone: null,
  date_of_birth: null
})

const isFormDirty = computed(() => {
  return [
    'full_name', 'first_name', 'last_name', 'phone', 'address', 'date_of_birth',
    'gender', 'nationality', 'company_or_college', 'designation_or_course',
    'pin_code', 'city', 'state', 'country', 'height_cm', 'weight_kg',
    'emergency_contact_name', 'emergency_contact', 'emergency_email',
    'emergency_relationship', 'food_preference', 'food_allergies',
    'tshirt_size', 'shoe_size'
  ].some((key) => formData[key] !== originalData[key])
})

const formatDate = (value) => {
  if (!value) return 'N/A'
  return new Date(value).toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' })
}

const loadProfile = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await api.get('/user/dashboard/profile')
    const profile = response.data.profile
    Object.assign(formData, {
      ...profile,
      date_of_birth: profile.date_of_birth ? profile.date_of_birth.split('T')[0] : ''
    })
    Object.assign(originalData, formData)
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to load profile.'
  } finally {
    isLoading.value = false
  }
}

const validateForm = () => {
  Object.keys(errors).forEach((key) => { errors[key] = null })

  let valid = true
  if (!formData.full_name || formData.full_name.trim().length === 0) {
    errors.full_name = 'Full name is required'
    valid = false
  }

  if (formData.phone && !/^[0-9+\-\s()]+$/.test(formData.phone)) {
    errors.phone = 'Invalid phone number format'
    valid = false
  }

  if (formData.date_of_birth) {
    const dob = new Date(formData.date_of_birth)
    const today = new Date()
    const age = today.getFullYear() - dob.getFullYear()
    if (age < 13) {
      errors.date_of_birth = 'You must be at least 13 years old'
      valid = false
    }
  }

  return valid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  isSaving.value = true
  error.value = null
  try {
    await api.put('/user/dashboard/profile', {
      full_name: formData.full_name,
      first_name: formData.first_name,
      last_name: formData.last_name,
      phone: formData.phone,
      address: formData.address,
      date_of_birth: formData.date_of_birth || null,
      gender: formData.gender,
      nationality: formData.nationality,
      company_or_college: formData.company_or_college,
      designation_or_course: formData.designation_or_course,
      pin_code: formData.pin_code,
      city: formData.city,
      state: formData.state,
      country: formData.country,
      height_cm: formData.height_cm,
      weight_kg: formData.weight_kg,
      emergency_contact_name: formData.emergency_contact_name,
      emergency_contact: formData.emergency_contact,
      emergency_email: formData.emergency_email,
      emergency_relationship: formData.emergency_relationship,
      food_preference: formData.food_preference,
      food_allergies: formData.food_allergies,
      tshirt_size: formData.tshirt_size,
      shoe_size: formData.shoe_size
    })

    showSuccess.value = true
    setTimeout(() => {
      showSuccess.value = false
    }, 3000)
    Object.assign(originalData, formData)
    toast.success('Profile updated successfully')
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to save profile.'
  } finally {
    isSaving.value = false
  }
}

const handleReset = () => {
  Object.assign(formData, originalData)
}

onMounted(loadProfile)
</script>

<style scoped>
.form-label {
  margin-bottom: 0.5rem;
}

.invalid-feedback {
  font-size: 0.875rem;
}
</style>
