<template>
  <div class="create-client-profile">
    <div class="form-container">
      <form @submit.prevent="submitForm">
        <div class="form-columns">
          <div class="form-column">
            <div class="form-group">
              <label for="firstName">First Name</label>
              <input v-model="client.FirstName" type="text" placeholder="First Name" required />
            </div>
            
            <div class="form-group">
              <label for="lastName">Last Name</label>
              <input v-model="client.LastName" type="text" placeholder="Last Name" required />
            </div>

            <div class="form-group">
              <label for="dateOfBirth">Date Of Birth</label>
              <input v-model="client.DateOfBirth" type="date" placeholder="Date of Birth" required />
            </div>

            <div class="form-group">
              <label for="gender">Gender</label>
              <select v-model="client.Gender" id="gender" required>
                <option value="" disabled selected>Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
                <option value="Prefer not to say">Prefer Not To Say</option>
              </select>
            </div>

            <div class="form-group">
              <label for="email">Email</label>
              <input v-model="client.EmailAddress" type="email" placeholder="Email" required />
            </div>

            <div class="form-group">
              <label for="phone">Phone Number</label>
              <vue-tel-input
                ref="phoneInput"
                v-model="client.PhoneNumber"
                :inputOptions="telInputOptions"
                :dropdownOptions="telDropdownOptions"
                :default-country="defaultCountryCode"
                mode="international"
                required
                class="tel-input-container"
              ></vue-tel-input>
            </div>
          </div>

          <div class="form-column">
            <div class="form-group">
              <label for="address">Address</label>
              <input v-model="client.Address" type="text" placeholder="Address" required />
            </div>

            <div class="form-group">
              <label for="city">City</label>
              <input v-model="client.City" type="text" placeholder="City" required />
            </div>

            <div class="form-group">
              <label for="state">State</label>
              <input v-model="client.State" type="text" placeholder="State" required />
            </div>

            <div class="form-group">
              <label for="country">Country</label>
              <select v-model="client.Country" id="country" required @change="updatePhoneCountry">
                <option value="" disabled selected>Select Country</option>
                <option v-for="country in countries" :key="country.name" :value="country.name">
                  {{ country.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="postalCode">Postal Code</label>
              <input 
                v-model="client.PostalCode" 
                type="text" 
                :inputmode="getInputMode()"
                placeholder="Postal Code" 
                @blur="validatePostalCodeOnBlur"
                required />
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit">Save</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../services/axiosInstance";
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
// Import the postal codes JSON file
import postalCodesData from '../postal_codes_regex.json'; // Adjust path as needed
// Get AgentID
import { fetchUserAttributes } from 'aws-amplify/auth'

export default {
  data() {
    return {
      client: {
        AgentID: '',
        FirstName: '',
        LastName: '',
        DateOfBirth: '',
        EmailAddress: '',
        PhoneNumber: '',
        Address: '',
        City: '',
        State: '',
        Country: '',
        PostalCode: '',
        Gender: ''
      },
      defaultCountryCode: 'us', // Default country code for phone input
      countries: [],
      postalCodePatterns: {}, // Store postal code patterns by country name
      telInputOptions: {
        placeholder: 'Phone Number',
        type: 'tel',
        inputClass: 'tel-input'
      },
      telDropdownOptions: {
        showDialCodeInSelection: true,
        showFlags: true,
        showSearchBox: true
      },
      lastValidatedPostalCode: '', // Track the last validated value to prevent duplicate toasts
      isPostalCodeValid: true, // Track if postal code is valid
    };
  },
  created() {
    // Extract countries from the imported JSON data
    this.countries = postalCodesData
      .map(country => ({
        code: country.abbrev,
        name: country.name
      }))
      .sort((a, b) => a.name.localeCompare(b.name));
    
    // Create a lookup for postal code patterns by country name
    this.postalCodePatterns = postalCodesData.reduce((acc, country) => {
      if (country.postal) {
        acc[country.name] = country.postal;
      }
      return acc;
    }, {});
  },
  methods: {
    async getUserAttributes() {
      const user = await fetchUserAttributes();
      this.client.AgentID = user.sub;
    },
    submitForm() {
      // Validate the postal code before submitting
      if (!this.validatePostalCode()) {
        return; // Stop if postal code is invalid
      }

      // Remove spaces from the phone number before submitting
      this.client.PhoneNumber = this.client.PhoneNumber.replace(/\s+/g, '');
      // Get AgentID
      this.getUserAttributes();
      
      console.log('Saving client profile:', this.client);

      // Call the save function to handle the data
      // TODO: Replace with Actual Endpoint
      axiosInstance.post('http://127.0.0.1:5001/clients', this.client)
        .then(response => {
          console.log('Client profile saved successfully:', response.data);
          toast("Client profile saved successfully!", {
            type: 'success',
            autoClose: 3000
          });
        })
        .catch(error => {
          // Handle error response
          // If the error response contains validation errors
          if(error.response && error.response.status === 400){
            const errors = error.response.data.errors;
            // Display error messages 
            for (const errorMsg of errors) {
              toast(errorMsg, {
                type: 'error',
                autoClose: 3000
              });
            }
          }
          // If the error response indicates a conflict (e.g., duplicate email)
          else if(error.response && error.response.status === 409){
            toast(error.response.data.error, {
              type: 'error',
              autoClose: 3000
            });
          }
          else {
            toast("An unexpected error occurred. Please try again.", {
              type: 'error',
              autoClose: 3000
            });
          }
          console.error('Error saving client profile:', error);
        });
    },
    updatePhoneCountry() {
      if (this.client.Country) {
        const country = postalCodesData.find(c => c.name === this.client.Country);
        if (country && country.abbrev) {
          this.defaultCountryCode = country.abbrev.toLowerCase();
        }
      }
      // Clear postal code when country changes to avoid validation errors
      this.client.PostalCode = '';
      this.isPostalCodeValid = true;
      this.lastValidatedPostalCode = '';
    },
    validatePostalCodeOnBlur() {
      // Only validate on blur if postal code has changed
      if (this.client.PostalCode !== this.lastValidatedPostalCode) {
        this.validatePostalCode();
      }
    },
    validatePostalCode() {
      const country = this.client.Country;
      const postalCode = this.client.PostalCode;
      
      // Skip validation if postal code is empty or no country is selected
      if (!postalCode || !country) {
        return true;
      }
      
      // Get pattern for the selected country
      const pattern = this.postalCodePatterns[country];
      if (!pattern) {
        return true; // No validation pattern for this country
      }
      
      try {
        const regex = new RegExp(`^${pattern}$`);
        
        // Update last validated postal code to prevent duplicate toasts
        this.lastValidatedPostalCode = postalCode;
        
        if (!regex.test(postalCode)) {
          const errorMsg = `Invalid postal code format for ${country}`;
          toast(errorMsg, {
            type: 'error',
            autoClose: 3000
          });
          this.isPostalCodeValid = false;
          return false;
        }
        
        this.isPostalCodeValid = true;
        return true;
      } catch (error) {
        console.error('Invalid regex pattern:', error);
        return true; // Allow submission if regex is invalid
      }
    },
    getInputMode() {
      // Determine the input mode based on the selected country's postal code format
      const country = this.client.Country;
      if (!country) return 'text';
      
      const pattern = this.postalCodePatterns[country];
      // If the pattern only contains numeric characters, use numeric input mode
      if (pattern && pattern.includes('[0-9]') && !pattern.includes('[A-Z]') && !pattern.includes('[a-z]')) {
        return 'numeric';
      }
      return 'text'; // Default to text for alphanumeric postal codes
    }
  },
  watch: {
    // Watch for country changes and update accordingly
    'client.Country': function() {
      this.updatePhoneCountry();
    },
    // Reset validation when postal code is changed
    'client.PostalCode': function() {
      // If user is changing the postal code, don't show the error until they finish (blur)
      if (this.client.PostalCode !== this.lastValidatedPostalCode) {
        this.isPostalCodeValid = true;
      }
    }
  }
};
</script>

<style scoped>
.create-client-profile {
  padding: 30px;
  max-width: 900px; /* Increased from 600px to accommodate two columns */
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

/* New styles for two-column layout */
.form-columns {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -10px; /* Negative margin to offset padding in columns */
}

.form-column {
  flex: 1;
  padding: 0 10px;
  min-width: 300px; /* Ensures column doesn't get too narrow */
}

.form-actions {
  margin-top: 20px;
  text-align: right;
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
  background-color: #fff !important;
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

/* Responsive styles for mobile devices */
@media (max-width: 768px) {
  .create-client-profile {
    padding: 15px;
    max-width: 100%;
  }
  
  .form-container {
    padding: 15px;
  }
  
  .form-columns {
    flex-direction: column;
  }
  
  .form-column {
    width: 100%;
  }
  
  .form-actions {
    text-align: center;
  }
  
  button {
    width: 100%;
  }
}
</style>