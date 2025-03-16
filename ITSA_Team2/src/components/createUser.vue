<template>
    <div class="user-creation-form">
      <h2>Create New User</h2>
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
          <label for="username">Username:</label>
          <input 
            type="text" 
            id="username" 
            v-model="formData.username" 
            required
            placeholder="johndoe"
          />
        </div>
        
        <div class="form-group">
          <label for="temporaryPassword">Temporary Password:</label>
          <input 
            type="password" 
            id="temporaryPassword" 
            v-model="formData.temporaryPassword" 
            required
            placeholder="Minimum 8 characters"
          />
        </div>
        
        <button type="submit" :disabled="isSubmitting">
          {{ isSubmitting ? 'Creating...' : 'Create User' }}
        </button>
      </form>
      
      <div v-if="message" :class="['message', messageType]">
        {{ message }}
      </div>
    </div>
  </template>
  
  <script>
  import { createUserToGroup } from '../services/client';

  export default {
    name: 'UserCreationForm',
    data() {
      return {
        formData: {
          email: '',
          username: '',
          temporaryPassword: ''
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
          // Replace this with your actual API call
          // For example: await createUserToGroup(this.formData.email, this.formData.username, this.formData.temporaryPassword);
          
          await createUserToGroup(this.formData.email, this.formData.username, this.formData.temporaryPassword);
          alert(this.formData.username + "account created successfully!");
          
          // Simulate API call
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          this.message = 'User created successfully!';
          this.messageType = 'success';
          
          // Reset form after successful submission
          this.formData = {
            email: '',
            username: '',
            temporaryPassword: ''
          };
        } catch (error) {
          console.error('Error creating user:', error);
          this.message = `Failed to create user: ${error.message || 'Unknown error'}`;
          this.messageType = 'error';
        } finally {
          this.isSubmitting = false;
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .user-creation-form {
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
  