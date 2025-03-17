<template>
    <div class="user-removal-form">
      <h2>Disable User in Group</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="email">User Email:</label>
          <input 
            id="email"
            v-model="email"
            type="email"
            placeholder="Enter user email"
            required
          />
          <p class="hint">Enter the email of the user you want to disable in the group</p>
        </div>
        
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? 'Processing...' : 'Disable User' }}
        </button>
        
        <div v-if="message" :class="['message', messageType]">
          {{ message }}
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { disableUserInGroup } from '../services/client.ts';
  
  const email = ref('');
  const isLoading = ref(false);
  const message = ref('');
  const messageType = ref('');
  
  async function handleSubmit() {
    if (!email.value) return;
    
    message.value = '';
    isLoading.value = true;
    
    try {
      const result = await disableUserInGroup(email.value);
      message.value = `User ${email.value} successfully disabled from group`;
      messageType.value = 'success';
      email.value = ''; // Clear the input after success
    } catch (error) {
      message.value = `Error: ${error.message || 'Failed to remove user from group'}`;
      messageType.value = 'error';
    } finally {
      isLoading.value = false;
    }
  }
  </script>
  
  <style scoped>
  .user-removal-form {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
  }
  
  .hint {
    margin-top: 5px;
    font-size: 14px;
    color: #666;
  }
  
  button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
  }
  
  button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  
  .message {
    margin-top: 15px;
    padding: 10px;
    border-radius: 4px;
  }
  
  .success {
    background-color: #dff0d8;
    color: #3c763d;
  }
  
  .error {
    background-color: #f2dede;
    color: #a94442;
  }
  </style>
  