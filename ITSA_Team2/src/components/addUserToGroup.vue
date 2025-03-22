<template>
  <div class="admin-panel">
    <h2>User Group Management</h2>
    
    <div class="user-input">
      <label for="email">User Email:</label>
      <input 
        id="email" 
        v-model="email" 
        type="email" 
        placeholder="Enter user email"
      />
    </div>
    
    <div class="group-actions">
      <div class="group-section">
        <h3>ADMINS Group</h3>
        <div class="button-group">
          <button 
            @click="handleAddUserToGroup('ADMINS')" 
            :disabled="!email"
            class="add-button"
          >
            Add to ADMINS
          </button>
          <button 
            @click="handleRemoveUserFromGroup('ADMINS')" 
            :disabled="!email"
            class="remove-button"
          >
            Remove from ADMINS
          </button>
        </div>
      </div>
      
      <div class="group-section">
        <h3>AGENTS Group</h3>
        <div class="button-group">
          <button 
            @click="handleAddUserToGroup('AGENTS')" 
            :disabled="!email"
            class="add-button"
          >
            Add to AGENTS
          </button>
          <button 
            @click="handleRemoveUserFromGroup('AGENTS')" 
            :disabled="!email"
            class="remove-button"
          >
            Remove from AGENTS
          </button>
        </div>
      </div>
    </div>
    
    <div v-if="message" :class="['message', messageType]">
      {{ message }}
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { addUserToGroup, removeUserFromGroup } from '../services/client';

export default {
  name: 'AdminPanel',
  setup() {
    const email = ref('');
    const message = ref('');
    const messageType = ref('');
    
    // Helper to get userId from email
    const getUserIdFromEmail = async (email) => {
      try {
        // This is a placeholder - you'll need to implement a function to look up
        // a user's ID based on their email, possibly using the Cognito ListUsers API
        // with a filter for the email attribute
        
        // For example:
        // const result = await listUsers({ filter: `email = "${email}"` });
        // return result.Users[0]?.Username;
        
        // For now, we'll just return a mock implementation
        // Replace this with your actual implementation
        return "user-id-for-" + email;
      } catch (error) {
        throw new Error(`Failed to find user with email ${email}: ${error.message}`);
      }
    };
    
    const showMessage = (text, type = 'success') => {
      message.value = text;
      messageType.value = type;
      
      // Clear message after 5 seconds
      setTimeout(() => {
        message.value = '';
      }, 5000);
    };
    
    const handleAddUserToGroup = async (groupName) => {
      if (!email.value) {
        showMessage('Please enter a valid email address', 'error');
        return;
      }
      
      try {
        // const userId = await getUserIdFromEmail(email.value);
        // if (!userId) {
        //   showMessage(`No user found with email ${email.value}`, 'error');
        //   return;
        // }
        
        await addUserToGroup(email.value, groupName);
        showMessage(`User ${email.value} added to ${groupName} group successfully!`);
      } catch (error) {
        showMessage(`Failed to add user to group: ${error.message}`, 'error');
      }
    };
    
    const handleRemoveUserFromGroup = async (groupName) => {
      if (!email.value) {
        showMessage('Please enter a valid email address', 'error');
        return;
      }
      
      try {
        // const userId = await getUserIdFromEmail(email.value);
        // if (!userId) {
        //   showMessage(`No user found with email ${email.value}`, 'error');
        //   return;
        // }
        
        await removeUserFromGroup(email.value, groupName);
        showMessage(`User ${email.value} removed from ${groupName} group successfully!`);
      } catch (error) {
        showMessage(`Failed to remove user from group: ${error.message}`, 'error');
      }
    };
    
    return {
      email,
      message,
      messageType,
      handleAddUserToGroup,
      handleRemoveUserFromGroup
    };
  }
}
</script>

<style scoped>
.admin-panel {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

h3 {
  color: #555;
  margin-bottom: 10px;
}

.user-input {
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
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.group-actions {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.group-section {
  flex: 1;
  padding: 15px;
  background-color: #fff;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

button {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.add-button {
  background-color: #4CAF50;
  color: white;
}

.add-button:hover:not(:disabled) {
  background-color: #45a049;
}

.remove-button {
  background-color: #f44336;
  color: white;
}

.remove-button:hover:not(:disabled) {
  background-color: #d32f2f;
}

.message {
  padding: 10px;
  border-radius: 4px;
  margin-top: 20px;
}

.success {
  background-color: #dff0d8;
  color: #3c763d;
  border: 1px solid #d6e9c6;
}

.error {
  background-color: #f2dede;
  color: #a94442;
  border: 1px solid #ebccd1;
}
</style>
