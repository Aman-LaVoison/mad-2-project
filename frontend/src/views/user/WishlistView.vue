<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h3>Wishlist</h3>
        <p class="text-muted">Your saved treks for later booking.</p>
      </div>
    </div>

    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-if="wishlist.length === 0 && !isLoading" class="alert alert-info">
      Your wishlist is empty. <router-link to="/user/treks">Browse treks</router-link> and add favorites to save them.
    </div>

    <div class="row">
      <div class="col-md-6 mb-4" v-for="item in wishlist" :key="item.id">
        <div class="card h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">{{ item.trek_name }}</h5>
            <p class="text-muted mb-1">{{ item.location }}</p>
            <p class="small text-muted mb-2">{{ formatDate(item.start_date) }}</p>
            <p class="card-text">{{ item.description }}</p>
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
  name: 'WishlistView',

  setup() {
    const wishlist = ref([])
    const isLoading = ref(false)
    const error = ref(null)

    const fetchWishlist = async () => {
      isLoading.value = true
      error.value = null
      try {
        const response = await api.get('/user/dashboard/wishlist')
        wishlist.value = response.data.wishlist
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to load wishlist.'
      } finally {
        isLoading.value = false
      }
    }

    const formatDate = (value) => {
      if (!value) return 'N/A'
      return new Date(value).toLocaleDateString('en-IN', { day: 'short', month: 'short', year: 'numeric' })
    }

    onMounted(fetchWishlist)

    return { wishlist, isLoading, error, formatDate }
  }
}
</script>
