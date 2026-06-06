
<template>
  <div class="container py-5">
    <div class="row mb-4">
      <div class="col-12">
        <h2 class="mb-1">My Dashboard</h2>
        <p class="text-muted">Manage your bookings, wishlist, vouchers, and profile from one place.</p>
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-lg-3 mb-3">
        <div class="list-group">
          <router-link class="list-group-item list-group-item-action" to="/user/dashboard">
            Overview
          </router-link>
          <router-link class="list-group-item list-group-item-action" to="/user/dashboard/user-upcoming-treks">
            Upcoming Treks
          </router-link>
          <router-link class="list-group-item list-group-item-action" to="/user/dashboard/user-wishlist">
            Wishlist
          </router-link>
          <router-link class="list-group-item list-group-item-action" to="/user/dashboard/user-previous-treks">
            Previous Treks
          </router-link>
          <router-link class="list-group-item list-group-item-action" to="/user/dashboard/user-myprofile">
            My Profile
          </router-link>
          <router-link class="list-group-item list-group-item-action" to="/user/dashboard/user-trekvouchers">
            Trek Vouchers
          </router-link>
        </div>
      </div>

      <div class="col-lg-9">
        <div class="row mb-4" v-if="dashboard">
          <div class="col-md-4 mb-3" v-for="item in stats" :key="item.label">
            <div class="card shadow-sm h-100">
              <div class="card-body">
                <h6 class="card-title text-uppercase text-muted">{{ item.label }}</h6>
                <p class="display-6 mb-0">{{ item.value }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="mb-4" v-if="error">
          <div class="alert alert-danger">{{ error }}</div>
        </div>

        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'UserDashboard',

  data() {
    return {
      dashboard: null,
      error: null
    }
  },

  computed: {
    stats() {
      if (!this.dashboard) return []
      return [
        { label: 'Total Bookings', value: this.dashboard.total_bookings },
        { label: 'Booked Treks', value: this.dashboard.booked_treks },
        { label: 'Completed Treks', value: this.dashboard.completed_treks }
      ]
    }
  },

  mounted() {
    this.fetchDashboard()
  },

  methods: {
    async fetchDashboard() {
      this.error = null
      try {
        const response = await api.get('/user/dashboard')
        this.dashboard = response.data.dashboard
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to load dashboard summary.'
      }
    }
  }
}
</script>
