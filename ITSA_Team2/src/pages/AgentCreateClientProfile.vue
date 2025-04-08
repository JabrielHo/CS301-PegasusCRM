<template>
  <div class="create-client-profile">
    <div class="form">
      <form @submit.prevent="submitForm">
        <input v-model="client.firstName" type="text" placeholder="First Name" required />
        <input v-model="client.lastName" type="text" placeholder="Last Name" required />
        <input v-model="client.dateOfBirth" type="date" placeholder="Date of Birth" required />
        <input v-model="client.Gender" type="radio" value="Male" id="Male" required />
        <label for="Male">Male</label>
        <input v-model="client.Gender" type="radio" value="Female" id="Female" required />
        <label for="Female">Female</label>
        <input v-model="client.Gender" type="radio" value="Other" id="Other" required />
        <label for="Other">Other</label>
        <input v-model="client.Gender" type="radio" value="PNTS" id="PNTS" required />
        <label for="PNTS">Prefer Not To Say</label>
        <input v-model="client.email" type="email" placeholder="Email" required />
        <input v-model="client.phone" type="text" placeholder="Phone" required />
        <input v-model="client.address" type="text" placeholder="Address" required />
        <input v-model="client.city" type="text" placeholder="City" required />
        <input v-model="client.state" type="text" placeholder="State" required />
        <input v-model="client.country" type="dropdown" placeholder="Country" required />
        <input v-model="client.postalCode" type="number" placeholder="Postal Code" required />

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
