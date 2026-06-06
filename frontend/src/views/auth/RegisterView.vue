<template>
  <div class="container py-5">
    <div class="row">
      <div class="col-lg-5 mx-auto">
        <div class="card">
          <div class="card-body">
            <h3 class="card-title mb-4">Register</h3>
            <form @submit.prevent="handleRegister">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input 
                  v-model="form.username" 
                  type="text" 
                  class="form-control" 
                  id="username"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input 
                  v-model="form.email" 
                  type="email" 
                  class="form-control" 
                  id="email"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="full_name" class="form-label">Full Name</label>
                <input 
                  v-model="form.full_name" 
                  type="text" 
                  class="form-control" 
                  id="full_name"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input 
                  v-model="form.password" 
                  type="password" 
                  class="form-control" 
                  id="password"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="confirm_password" class="form-label">Confirm Password</label>
                <input 
                  v-model="form.confirm_password" 
                  type="password" 
                  class="form-control" 
                  id="confirm_password"
                  required
                >
              </div>
              <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                {{ loading ? 'Registering...' : 'Register' }}
              </button>
            </form>
            <p class="mt-3 text-center" v-if="!isLoggedIn">
              Already have an account? <router-link to="/auth/login">Login here</router-link>
            </p>
            <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
            <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'

export default {
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const form = reactive({
      username: '',
      email: '',
      full_name: '',
      password: '',
      confirm_password: ''
    })
    
    const loading = ref(false)
    const error = ref(null)
    const success = ref(null)
    
    const handleRegister = async () => {
      if (form.password !== form.confirm_password) {
        error.value = 'Passwords do not match'
        return
      }
      
      loading.value = true
      error.value = null
      success.value = null
      
      try {
        await authStore.register(
          form.username,
          form.email,
          form.password,
          form.full_name
        )
        success.value = 'Registration successful! Redirecting to login...'
        setTimeout(() => {
          router.push('/auth/login')
        }, 2000)
      } catch (err) {
        error.value = err.error || 'Registration failed. Please try again.'
      } finally {
        loading.value = false
      }
    }
    
    return {
      form,
      loading,
      error,
      success,
      handleRegister,
      isLoggedIn: authStore.isLoggedIn
    }
  }
}
</script>
