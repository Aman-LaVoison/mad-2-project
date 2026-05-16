<template>
  <div class="container py-5">
    <div class="row">
      <div class="col-lg-5 mx-auto">
        <div class="card">
          <div class="card-body">
            <h3 class="card-title mb-4">Login</h3>
            <form @submit.prevent="handleLogin">
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
                <label for="password" class="form-label">Password</label>
                <input 
                  v-model="form.password" 
                  type="password" 
                  class="form-control" 
                  id="password"
                  required
                >
              </div>
              <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                {{ loading ? 'Logging in...' : 'Login' }}
              </button>
            </form>
            <p class="mt-3 text-center">
              Don't have an account? <router-link to="/auth/register">Register here</router-link>
            </p>
            <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
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
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const form = reactive({
      username: 'admin',
      password: 'admin123'
    })
    
    const loading = ref(false)
    const error = ref(null)
    
    const handleLogin = async () => {
      loading.value = true
      error.value = null
      
      try {
        await authStore.login(form.username, form.password)
        const userType = authStore.userType
        router.push(`/${userType}/dashboard`)
      } catch (err) {
        error.value = err.error || 'Login failed. Please try again.'
      } finally {
        loading.value = false
      }
    }
    
    return {
      form,
      loading,
      error,
      handleLogin
    }
  }
}
</script>
