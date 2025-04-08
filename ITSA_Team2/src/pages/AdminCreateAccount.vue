<template>
  <div class="create-client-profile">
    <div class="form">
      <form @submit.prevent="submitForm">
        <input v-model="client.firstName" placeholder="First Name" required />
        <input v-model="client.lastName" placeholder="Last Name" required />
        <input v-model="client.dateOfBirth" placeholder="Date of Birth" required />
        <input v-model="client.email" placeholder="Email" required />
        <input v-model="client.phone" placeholder="Phone" required />
        <button type="submit">Save</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      client: {
        firstName: '',
        lastName: '',
        dateOfBirth: '',
        email: '',
        phone: ''
      }
    };
  },
  methods: {
    submitForm() {
      console.log('Saving client profile:', this.client);
      // Implement save logic here
    }
  }
};
</script>

<style scoped>
.create-client-profile {
  padding: 20px;
}

header {
  margin-bottom: 20px;
}

h1 {
  font-size: 2rem;
  font-weight: bold;
}

.form input {
  padding: 10px;
  margin: 10px;
  width: 100%;
}

button {
  padding: 10px 20px;
  background-color: #00f;
  color: white;
}
</style>
