<template>
    <div>
      <h1>Welcome to the Home Page</h1>
      <p>This is the main landing page of the application.</p>
      
      <!-- Example of loading state -->
      <div v-if="loading">Loading...</div>
      <div v-else class="container">
        <!-- Your main content here -->
        <div class="content-section">
          <p>This page has been visited 30 times.</p>
        </div>
      </div>
    </div>
</template>
  
<script>
  export default {
    name: 'HomeView',
    data() {
      return {
        loading: false
      };
    },
    created() {
      // Initialize any data or make API calls when component is created
    },
    methods: {
      // Add your methods here
    }
  };
  </script>
  
  <style scoped>
  /* Add your component styles here */
  .container {
    margin: 0 auto;
    padding: 20px;
  }
  
  .content-section {
    margin-top: 20px;
  }
</style>
  