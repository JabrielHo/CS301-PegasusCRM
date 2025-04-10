<template>
  <div class="create-client-profile">

    <div class="form-container">
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="firstName">First Name</label>
          <input v-model="client.firstName" type="text" placeholder="First Name" required />
        </div>
        
        <div class="form-group">
          <label for="lastName">Last Name</label>
          <input v-model="client.lastName" type="text" placeholder="Last Name" required />
        </div>

        <div class="form-group">
          <label for="dateOfBirth">Date Of Birth</label>
          <input v-model="client.dateOfBirth" type="date" placeholder="Date of Birth" required />
        </div>

        <div class="form-group">
          <label for="gender">Gender</label>
          <select v-model="client.gender" id="gender" required>
            <option value="" disabled selected>Select Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
            <option value="PNTS">Prefer Not To Say</option>
          </select>
        </div>

        <div class="form-group">
          <label for="email">Client Email</label>
          <input v-model="client.email" type="email" placeholder="Email" required />
        </div>

        <div class="form-group">
          <label for="phone">Client Phone Number</label>
          <input v-model="client.phone" type="text" placeholder="Phone" required />
        </div>

        <div class="form-group">
          <label for="address">Client Address</label>
          <input v-model="client.address" type="text" placeholder="Address" required />
        </div>

        <div class="form-group">
          <label for="city">City</label>
          <input v-model="client.city" type="text" placeholder="City" required />
        </div>

        <div class="form-group">
          <label for="state">State</label>
          <input v-model="client.state" type="text" placeholder="State" required />
        </div>

        <div class="form-group">
          <label for="country">Country</label>
          <select v-model="client.country" id="country" required>
            <option value="" disabled selected>Select Country</option>
            <option v-for="country in countries" :key="country.code" :value="country.code">
              {{ country.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="postalCode">Postal Code</label>
          <input v-model="client.postalCode" type="text" placeholder="Postal Code" required />
        </div>

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
        gender: '',
        email: '',
        phone: '',
        address: '',
        city: '',
        state: '',
        country: '',
        postalCode: ''
      },
      countries: []
    };
  },
  created() {
    // Access countries from global properties
    const countryNames = this.$countries.getNames('en');
    const countryCodes = this.$countries.getAlpha3Codes();
    
    this.countries = Object.keys(countryNames).map(code => ({
      code: countryCodes[code] || code,
      name: countryNames[code]
    }));
    
    // Sort countries alphabetically by name
    this.countries.sort((a, b) => a.name.localeCompare(b.name));
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
  padding: 30px;
  max-width: 600px;
  margin: 0 auto;
}

header {
  margin-bottom: 20px;
}

h1 {
  font-size: 2rem;
  font-weight: bold;
}

.form-container {
  background-color: #fff;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
} 

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

input, select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus, select:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

button {
  padding: 10px 20px;
  background-color: #00f;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

button:hover {
  background-color: #0000cc;
}

@media (max-width: 600px) {
  .create-client-profile {
    padding: 15px;
  }
  
  .form-container {
    padding: 15px;
  }
  
  .actions {
    flex-direction: column;
    gap: 10px;
  }
  
  .cancel-button, .submit-button {
    width: 100%;
  }
}
</style>