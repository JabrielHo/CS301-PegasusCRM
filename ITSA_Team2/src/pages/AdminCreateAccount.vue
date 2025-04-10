<template>
  <div class="create-agent-profile">
    <header>
      <h1>Create  Profile</h1>
      <p class="subtitle">Please fill in the details below to create a new Agent/Admin account</p>
    </header>
    
    <div class="form-container">
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="firstName">First Name</label>
          <input id="firstName" v-model="client.firstName" placeholder="Enter first name" required />
        </div>
        
        <div class="form-group">
          <label for="lastName">Last Name</label>
          <input id="lastName" v-model="client.lastName" placeholder="Enter last name" required />
        </div>
        
        <div class="form-group">
          <label for="dateOfBirth">Date of Birth</label>
          <input id="dateOfBirth" type="date" v-model="client.dateOfBirth" required />
        </div>
        
        <div class="form-group">
          <label for="email">Email</label>
          <input id="email" type="email" v-model="client.email" placeholder="Enter email address" required />
        </div>
        
        <div class="form-group">
          <label for="temporaryPassword">Temporary Password</label>
          <input id="temporaryPassword" type="tel" v-model="client.temporaryPassword" placeholder="Enter temporary password" required />
        </div>
        
        <div class="form-group">
          <label>Role</label>
          <div class="role-selector">
            <button 
              type="button" 
              class="role-button" 
              :class="{ active: client.role === 'AGENTS' }"
              @click="selectRole('Agent')">
              Agent
            </button>
            <button 
              type="button" 
              class="role-button" 
              :class="{ active: client.role === 'ADMINS' }"
              @click="selectRole('Admin')">
              Admin
            </button>
          </div>
        </div>
        
        <div class="actions">
          <button type="button" class="cancel-button" @click="resetForm">Clear</button>
          <button type="submit" class="submit-button">Create Account</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { createUserToGroup, addUserToGroup } from '../services/client'; // Adjust the import based on your project structure

export default {
  data() {
    return {
      client: {
        firstName: '',
        lastName: '',
        dateOfBirth: '',
        email: '',
        temporaryPassword: '',
        phone: '',
        role: 'AGENTS' // Default role
      }
    };
  },
  methods: {
    async submitForm() {
      try{
      console.log('Saving client profile:', this.client);

      if (new Date(this.client.dateOfBirth) > new Date()) {
        alert('Date of Birth cannot be in the future.');
        return;
      }
      console.log(this.client.dateOfBirth);
      const createStatus = await createUserToGroup(
        this.client.email,
        this.client.firstName,
        this.client.lastName,
        this.client.temporaryPassword,
        this.client.dateOfBirth
      );
      console.log('Create status:', createStatus);

      if (!createStatus) {
        alert('Failed to create account. Please try again.');
        return;
      }

      const addStatus = await addUserToGroup(this.client.email, this.client.role);

      if (!addStatus) {
        alert('Failed to add user to group. Please try again.');
        return;
      }

      alert(`Account created successfully as ${this.client.role}`);
      this.resetForm(); // Reset the form after successful submission
    } catch (error) {
      console.error('Error creating account:', error);
      alert('An error occurred while creating the account. Please try again later.');
    }
    },
    selectRole(role) {
      // Map UI roles to backend roles
      const roleMapping = {
        Admin: 'ADMINS',
        Agent: 'AGENTS',
      };
      this.client.role = roleMapping[role];
    },
    resetForm() {
      this.client = {
        firstName: '',
        lastName: '',
        dateOfBirth: '',
        email: '',
        phone: '',
        role: 'AGENTS'
      };
    }
  }
};
</script>

<style scoped>
.create-agent-profile {
  padding: 30px;
  max-width: 600px;
  margin: 0 auto;
  font-family: 'Arial', sans-serif;
}

header {
  margin-bottom: 30px;
  text-align: center;
}

h1 {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.subtitle {
  color: #666;
  font-size: 1rem;
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

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.role-selector {
  display: flex;
  gap: 10px;
  margin-top: 5px;
}

.role-button {
  flex: 1;
  padding: 12px;
  background-color: #f1f1f1;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  color: #333;
}

.role-button.active {
  background-color: #4a90e2;
  color: white;
  border-color: #3a80d2;
}

.actions {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.cancel-button {
  padding: 12px 20px;
  background-color: #fff;
  color: #333;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-button:hover {
  background-color: #f1f1f1;
}

.submit-button {
  padding: 12px 20px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
}

.submit-button:hover {
  background-color: #3a80d2;
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