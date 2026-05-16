<template>
  <div id="app" class="d-flex flex-column min-vh-100">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand fw-bold">🏔️ Trekking Hub</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li v-if="!isLoggedIn" class="nav-item">
              <router-link to="/auth/register" class="nav-link">Register</router-link>
            </li>
            <li v-if="!isLoggedIn" class="nav-item">
              <router-link to="/auth/login" class="nav-link">Login</router-link>
            </li>
            <li v-if="isLoggedIn" class="nav-item">
              <router-link :to="`/${userType}/dashboard`" class="nav-link">Dashboard</router-link>
            </li>
            <li v-if="isLoggedIn" class="nav-item">
              <a href="#" @click.prevent="logout" class="nav-link">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <main class="flex-grow-1">
      <router-view />
    </main>

    <footer class="bg-dark text-white text-center py-4 mt-5">
      <p>&copy; 2024 Trekking Management System. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
import { useAuthStore } from './store/auth'

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore()

    const logout = async () => {
      await authStore.logout()
      this.$router.push('/auth/login')
    }

    return {
      logout,
      isLoggedIn: () => authStore.isLoggedIn,
      userType: () => authStore.userType
    }
  },
  computed: {
    isLoggedIn() {
      return useAuthStore().isLoggedIn
    },
    userType() {
      return useAuthStore().userType
    }
  }
}
</script>

<style scoped>
.min-vh-100 {
  min-height: 100vh;
}
</style>
