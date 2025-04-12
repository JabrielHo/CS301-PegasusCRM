<template>
  <div>
    <h1>404 Not Found</h1>
    <p>The page you are looking for does not exist.</p>
    <button @click="goBack()">Go Back</button>
  </div>
</template>

<script>
export default {
  name: "NotFoundPage",
  methods: {
    goBack() {
      this.$router.back();
    }
  }
};
</script>

<style scoped>
div {
  text-align: center;
  margin-top: 50px;
}

h1 {
  font-size: 2rem;
  color: #ff0000;
  /* Optional: Add a red color for emphasis */
}

p {
  font-size: 1.2rem;
  margin: 20px 0;
}

a {
  text-decoration: none;
  color: #007bff;
}

a:hover {
  text-decoration: underline;
}

button {
  background-color: #3b82f6;
  color: white;
}
</style>
