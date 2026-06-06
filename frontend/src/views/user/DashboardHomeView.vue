<template>
  <div>
    <div class="card mb-4 shadow-sm">
      <div class="card-body">
        <h4 class="card-title">Welcome to your dashboard</h4>
        <p class="card-text text-muted">Use the menu on the left to explore your upcoming treks, wishlist, previous adventures, profile, and vouchers.</p>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6 mb-3">
        <div class="card border-primary h-100">
          <div class="card-body">
            <h5 class="card-title">Upcoming Treks</h5>
            <p class="card-text">See the treks you've booked and plan your next adventure.</p>
          </div>
        </div>
      </div>
      <div class="col-md-6 mb-3">
        <div class="card border-secondary h-100">
          <div class="card-body">
            <h5 class="card-title">My Profile</h5>
            <p class="card-text">Keep your personal details up to date for faster bookings.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardHomeView'
}
</script>
