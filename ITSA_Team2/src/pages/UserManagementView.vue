<template>
    <div class="user-management">
      <h1>User Management</h1>
      
      <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger']">
        {{ message }}
      </div>
      
      <div class="tabs">
        <button 
          :class="['tab-button', activeTab === 'create' ? 'active' : '']" 
          @click="activeTab = 'create'"
        >
          Create User
        </button>
        <button 
          :class="['tab-button', activeTab === 'update' ? 'active' : '']" 
          @click="activeTab = 'update'"
        >
          Update User
        </button>
        <button 
          :class="['tab-button', activeTab === 'disable' ? 'active' : '']" 
          @click="activeTab = 'disable'"
        >
          Disable User
        </button>
      </div>
      
      <!-- Create User Form -->
      <div v-if="activeTab === 'create'" class="tab-content">
        <h2>Create New User</h2>
        <form @submit.prevent="handleCreateUser">
          <div class="form-group">
            <label for="email">Email:</label>
            <input 
              type="email" 
              id="email" 
              v-model="newUser.email" 
              required
              class="form-control"
            />
          </div>
          
          <div class="form-group">
            <label for="password">Password:</label>
            <input 
              type="password" 
              id="password" 
              v-model="newUser.password" 
              required
              class="form-control"
            />
          </div>
          
          <div class="form-group">
            <label for="firstName">First Name:</label>
            <input 
              type="text" 
              id="firstName" 
              v-model="newUser.firstName" 
              required
              class="form-control"
            />
          </div>
          
          <div class="form-group">
            <label for="lastName">Last Name:</label>
            <input 
              type="text" 
              id="lastName" 
              v-model="newUser.lastName" 
              required
              class="form-control"
            />
          </div>
          
          <div class="form-group">
            <label for="phoneNumber">Phone Number:</label>
            <input 
              type="tel" 
              id="phoneNumber" 
              v-model="newUser.phoneNumber" 
              required
              placeholder="+12345678900"
              class="form-control"
            />
          </div>
          
          <div class="form-group">
            <label for="role">Role:</label>
            <select 
              id="role" 
              v-model="newUser.role" 
              required
              class="form-control"
            >
              <option value="ADMINS">Admin</option>
              <option value="AGENTS">Agent</option>
            </select>
          </div>
          
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Creating...' : 'Create User' }}
          </button>
        </form>
      </div>
      
      <!-- Update User Form -->
      <div v-if="activeTab === 'update'" class="tab-content">
        <h2>Update User</h2>
        <form @submit.prevent="handleUpdateUser">
          <div class="form-group">
            <label for="updateEmail">Email:</label>
            <input 
              type="email" 
              id="updateEmail" 
              v-model="updateUserData.email" 
              required
              class="form-control"
            />
          </div>
          
          <div class="form-group">
            <label for="updateFirstName">First Name:</label>
            <input 
              type="text" 
              id="updateFirstName" 
              v-model="updateUserData.firstName" 
              class="form-control"
            />
          </div>
          
          <div class="form-group">
            <label for="updateLastName">Last Name:</label>
            <input 
              type="text" 
              id="updateLastName" 
              v-model="updateUserData.lastName" 
              class="form-control"
            />
          </div>
          
          <div class="form-group">
            <label for="updatePhoneNumber">Phone Number:</label>
            <input 
              type="tel" 
              id="updatePhoneNumber" 
              v-model="updateUserData.phoneNumber" 
              placeholder="+12345678900"
              class="form-control"
            />
          </div>
          
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Updating...' : 'Update User' }}
          </button>
        </form>
      </div>
      
      <!-- Disable User Form -->
      <div v-if="activeTab === 'disable'" class="tab-content">
        <h2>Disable User</h2>
        <form @submit.prevent="handleDisableUser">
          <div class="form-group">
            <label for="disableEmail">Email:</label>
            <input 
              type="email" 
              id="disableEmail" 
              v-model="disableUserEmail" 
              required
              class="form-control"
            />
          </div>
          
          <div class="confirmation">
            <p class="warning-text">Are you sure you want to disable this user? This action cannot be undone.</p>
            <button type="submit" class="btn btn-danger" :disabled="loading">
              {{ loading ? 'Disabling...' : 'Disable User' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { generateClient } from 'aws-amplify/api';
  
  const client = generateClient();
  
  export default {
    setup() {
      const activeTab = ref('create');
      const loading = ref(false);
      const message = ref('');
      const messageType = ref('success');
      
      // Create user form data
      const newUser = ref({
        email: '',
        password: '',
        firstName: '',
        lastName: '',
        phoneNumber: '',
        role: 'AGENTS'
      });
      
      // Update user form data
      const updateUserData = ref({
        email: '',
        firstName: '',
        lastName: '',
        phoneNumber: ''
      });
      
      // Disable user form data
      const disableUserEmail = ref('');
      
      const handleCreateUser = async () => {
        loading.value = true;
        message.value = '';
        
        try {
          const response = await client.graphql({
            query: `
              mutation CreateUser(
                $email: String!
                $password: String!
                $firstName: String!
                $lastName: String!
                $phoneNumber: String
                $role: String!
              ) {
                createUser(
                  email: $email
                  password: $password
                  firstName: $firstName
                  lastName: $lastName
                  phoneNumber: $phoneNumber
                  role: $role
                ) {
                  id
                  email
                  firstName
                  lastName
                  role
                  status
                }
              }
            `,
            variables: {
              email: newUser.value.email,
              password: newUser.value.password,
              firstName: newUser.value.firstName,
              lastName: newUser.value.lastName,
              phoneNumber: newUser.value.phoneNumber || '',
              role: newUser.value.role
            }
          });
          
          message.value = 'User created successfully!';
          messageType.value = 'success';
          
          // Reset form
          newUser.value = {
            email: '',
            password: '',
            firstName: '',
            lastName: '',
            phoneNumber: '',
            role: 'AGENTS'
          };
        } catch (error) {
          message.value = `Error creating user: ${error.message || 'Unknown error'}`;
          messageType.value = 'error';
        } finally {
          loading.value = false;
        }
      };
      
      const handleUpdateUser = async () => {
        loading.value = true;
        message.value = '';
        
        try {
          const response = await client.graphql({
            query: `
              mutation UpdateUser(
                $email: String!
                $firstName: String
                $lastName: String
                $phoneNumber: String
              ) {
                updateUser(
                  email: $email
                  firstName: $firstName
                  lastName: $lastName
                  phoneNumber: $phoneNumber
                ) {
                  message
                  success
                }
              }
            `,
            variables: {
              email: updateUserData.value.email,
              firstName: updateUserData.value.firstName,
              lastName: updateUserData.value.lastName,
              phoneNumber: updateUserData.value.phoneNumber
            }
          });
          
          message.value = 'User updated successfully!';
          messageType.value = 'success';
          
          // Reset form fields except email
          const email = updateUserData.value.email;
          updateUserData.value = {
            email,
            firstName: '',
            lastName: '',
            phoneNumber: ''
          };
        } catch (error) {
          message.value = `Error updating user: ${error.message || 'Unknown error'}`;
          messageType.value = 'error';
        } finally {
          loading.value = false;
        }
      };
      
      const handleDisableUser = async () => {
        loading.value = true;
        message.value = '';
        
        try {
          const response = await client.graphql({
            query: `
              mutation DisableUser($email: String!) {
                disableUser(email: $email) {
                  message
                  success
                }
              }
            `,
            variables: { email: disableUserEmail.value }
          });
          
          message.value = 'User disabled successfully!';
          messageType.value = 'success';
          
          // Reset form
          disableUserEmail.value = '';
        } catch (error) {
          message.value = `Error disabling user: ${error.message || 'Unknown error'}`;
          messageType.value = 'error';
        } finally {
          loading.value = false;
        }
      };
      
      return {
        activeTab,
        loading,
        message,
        messageType,
        newUser,
        updateUserData,
        disableUserEmail,
        handleCreateUser,
        handleUpdateUser,
        handleDisableUser
      };
    }
  };
  </script>
  
  <style scoped>
  .user-management {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 30px;
  }
  
  h2 {
    margin-bottom: 20px;
  }
  
  .alert {
    padding: 10px;
    border-radius: 4px;
    margin-bottom: 20px;
  }
  
  .alert-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
  }
  
  .alert-danger {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }
  
  .tabs {
    display: flex;
    margin-bottom: 20px;
    border-bottom: 1px solid #dee2e6;
  }
  
  .tab-button {
    padding: 10px 15px;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 16px;
    color: #495057;
  }
  
  .tab-button.active {
    color: #007bff;
    border-bottom: 2px solid #007bff;
  }
  
  .tab-content {
    padding: 20px 0;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
  }
  
  .form-control {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-size: 16px;
  }
  
  .btn {
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
  }
  
  .btn-primary {
    background-color: #007bff;
    color: white;
  }
  
  .btn-primary:disabled {
    background-color: #6c757d;
    cursor: not-allowed;
  }
  
  .btn-danger {
    background-color: #dc3545;
    color: white;
  }
  
  .btn-danger:disabled {
    background-color: #6c757d;
    cursor: not-allowed;
  }
  
  .warning-text {
    color: #dc3545;
    font-weight: 500;
    margin-bottom: 15px;
  }
  
  .confirmation {
    margin-top: 20px;
    padding: 15px;
    border: 1px solid #f5c6cb;
    border-radius: 4px;
    background-color: #f8d7da;
  }
  </style>
  