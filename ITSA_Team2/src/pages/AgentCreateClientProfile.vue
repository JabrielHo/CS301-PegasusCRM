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
          <label for="email">Email</label>
          <input v-model="client.email" type="email" placeholder="Email" required />
        </div>

        <div class="form-group">
          <label for="phone">Phone Number</label>
          <vue-tel-input
            v-model="client.phone"
            :inputOptions="telInputOptions"
            :dropdownOptions="telDropdownOptions"
            @input="onPhoneInput"
            mode="international"
            required
            class="tel-input-container"
          ></vue-tel-input>
        </div>

        <div class="form-group">
          <label for="address">Address</label>
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
          <select v-model="client.country" id="country" required @change="updatePhoneCountry">
            <option value="" disabled selected>Select Country</option>
            <option v-for="country in countries" :key="country.code" :value="country.code">
              {{ country.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="postalCode">Postal Code</label>
          <input 
            v-model="client.postalCode" 
            type="text" 
            inputmode="numeric"
            pattern="[0-9]*"
            placeholder="Postal Code" 
            @input="validatePostalCode"
            required />
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
        phoneCountry: '',
        phoneNumber: '',
        address: '',
        city: '',
        state: '',
        country: '',
        postalCode: ''
      },
      countries: [],
      telInputOptions: {
        placeholder: 'Phone Number',
        type: 'tel',
        inputClass: 'tel-input'
      },
      telDropdownOptions: {
        showDialCodeInSelection: true,
        showFlags: true,
        showSearchBox: true
      }
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
    validatePostalCode(event) {
      // Remove any non-numeric characters
      this.client.postalCode = this.client.postalCode.replace(/\D/g, '');
    },
    onPhoneInput(formattedNumber, { number, isValid, country }) {
      if (isValid) {
        this.client.phone = number.international;
        this.client.phoneCountry = country.iso2;
        this.client.phoneNumber = number.significant;
      }
    },
    updatePhoneCountry() {
      // If user selects a country from the main country dropdown, 
      // we can optionally sync that with the phone country dropdown
      // This would require accessing the vue-tel-input component via refs
      // and is more complex, so we'll leave this as a placeholder
    },
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

/* Phone input container styling */
.tel-input-container {
  width: 100%;
}

/* Fix the height and style of the phone input to match other inputs */
:deep(.vti__dropdown),
:deep(.vti__input) {
  height: 45px !important;
  min-height: 45px !important;
  padding: 12px !important;
  border-radius: 4px !important;
  font-size: 1rem !important;
  background-color: white !important;
}

/* Make the dropdown button and flag container match the height */
:deep(.vti__dropdown) {
  border-top-right-radius: 0 !important;
  border-bottom-right-radius: 0 !important;
  border-right: none !important;
}

/* Make the input field match styling */
:deep(.vti__input) {
  border-top-left-radius: 0 !important;
  border-bottom-left-radius: 0 !important;
  flex: 1 !important;
}

/* Adjust flag container size */
:deep(.vti__flag) {
  margin-top: 0 !important;
}

/* Focus styles for phone input components */
:deep(.vti__dropdown:focus),
:deep(.vti__input:focus) {
  outline: none !important;
  border-color: #4a90e2 !important;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2) !important;
}

/* Make sure the phone input components stay next to each other */
:deep(.vti__dropdown), 
:deep(.vti__input) {
  display: inline-flex !important;
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