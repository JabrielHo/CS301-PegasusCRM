<template>
    <div class="user-update-form">
      <h2>Update User</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="email">Email:</label>
          <input 
            type="email" 
            id="email" 
            v-model="formData.email" 
            required
            placeholder="user@example.com"
          />
        </div>
        
        <div class="form-group">
          <label for="firstName">First Name:</label>
          <input 
            type="text" 
            id="firstName" 
            v-model="formData.firstName" 
            required
            placeholder="John"
          />
        </div>
  
        <div class="form-group">
          <label for="lastName">Last Name:</label>
          <input 
            type="text" 
            id="lastName" 
            v-model="formData.lastName" 
            required
            placeholder="Doe"
          />
        </div>
        
        <button type="submit" :disabled="isSubmitting">
          {{ isSubmitting ? 'Updating...' : 'Update User' }}
        </button>
      </form>
      
      <div v-if="message" :class="['message', messageType]">
        {{ message }}
      </div>
    </div>
  </template>
  
  <script>
  import { updateUserAttribute } from '../services/client.ts';
  
  export default {
    name: 'UserUpdateForm',
    data() {
      return {
        formData: {
          email: '',
          firstName: '',
          lastName: ''
        },
        isSubmitting: false,
        message: '',
        messageType: 'success'
      }
    },
    methods: {
      async handleSubmit() {
        this.isSubmitting = true;
        this.message = '';
        
        try {
          await updateUserAttribute(this.formData.email, this.formData.firstName, this.formData.lastName);
          alert(this.formData.firstName + "account updated successfully!");

          this.message = 'User updated successfully!';
          this.messageType = 'success';

        // Reset form after successful submission
        this.formData = {
            email: '',
            username: '',
            temporaryPassword: ''
          };
        
        } catch (error) {
          console.error('Error updating user:', error);
          this.message = `Failed to update user: ${error.message || 'Unknown error'}`;
          this.messageType = 'error';
        } finally {
          this.isSubmitting = false;
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .user-update-form {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
  }
  
  h2 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
  }
  
  input:disabled {
    background-color: #f0f0f0;
    cursor: not-allowed;
  }
  
  button {
    width: 100%;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    margin-top: 10px;
  }
  
  button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  
  .message {
    margin-top: 15px;
    padding: 10px;
    border-radius: 4px;
    text-align: center;
  }
  
  .success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
  }
  
  .error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }
  </style>
  