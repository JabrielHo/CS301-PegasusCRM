<template>
    <div>
      <h2>Admin Panel</h2>
      <button @click="handleAddUserToAdmins">Add User to Admins</button>
    </div>
  </template>
  
  <script>
  import { addUserToGroup } from '../services/client';
  
  export default {
    name: 'AdminPanel',
    methods: {
      async handleAddUserToAdmins() {
        try {
          const userId = "695a756c-60e1-706f-8371-ec05ecc78111"; // Get this from your app state or form
          await addUserToGroup(userId, "ADMINS");
          alert("User added to ADMINS group successfully!");
        } catch (error) {
          alert("Failed to add user to group: " + error.message);
        }
      }
    }
  }
  </script>