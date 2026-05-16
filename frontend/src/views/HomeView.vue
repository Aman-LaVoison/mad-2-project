<template>
  <div class="container py-5">
    <div class="row">
      <div class="col-lg-8 mx-auto">
        <h1 class="mb-4">Welcome to Trekking Hub</h1>
        <p class="lead">Your gateway to amazing trekking adventures!</p>
        
        <div class="row mt-5">
          <div class="col-md-6 mb-4">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">New to Trekking?</h5>
                <p class="card-text">Register now and start exploring amazing treks.</p>
                <router-link to="/auth/register" class="btn btn-primary">Register</router-link>
              </div>
            </div>
          </div>
          <div class="col-md-6 mb-4">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">Already a Member?</h5>
                <p class="card-text">Log in to view available treks and bookings.</p>
                <router-link to="/auth/login" class="btn btn-primary">Login</router-link>
              </div>
            </div>
          </div>
        </div>

        <div class="row mt-5">
          <div class="col-md-4 mb-4">
            <h6>🏔️ Explore Treks</h6>
            <p>Browse through a curated collection of trekking routes.</p>
          </div>
          <div class="col-md-4 mb-4">
            <h6>📅 Book Adventures</h6>
            <p>Reserve your spot and plan your next adventure.</p>
          </div>
          <div class="col-md-4 mb-4">
            <h6>👥 Community</h6>
            <p>Connect with fellow trekking enthusiasts.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>
