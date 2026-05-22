
<template>
  <div class="container py-5">
    
    <h2>Hii {{ backendData?.user?.username  }}</h2>

    
  </div>
</template>

<script>

import axios from 'axios';

export default {
  name: 'UserDashboard',

  data() {

    return {
     backendData: null
    };

  },
  mounted() {
    // Fetch data from the backend when the component is mounted
    this.fetchBackendData();
  },
  methods: {
    async fetchBackendData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/user/dashboard');
        this.backendData = response.data;
      } catch (error) {
        console.error('Error fetching backend data:', error);
      }
    }
  }
}
</script>
