<script setup>
import { Authenticator } from "@aws-amplify/ui-vue";
import "@aws-amplify/ui-vue/styles.css";

import { Amplify } from 'aws-amplify';
import outputs from '../amplify_outputs.json';

Amplify.configure(outputs);
</script>

<template>
  <authenticator :hide-sign-up="true">
    <template v-slot="{ user, signOut }">

      <div id="app">
        <div class="user-header">
          <h2>Hello {{ user.username }}!</h2>
          <button @click="signOut">Sign Out</button>
        </div>
        
        <!-- Navigation links -->
        <nav>
          <router-link to="/">Home</router-link> |
          <router-link to="/user-management">User Management</router-link>
        </nav>
        
        <!-- This is where your route components will be rendered -->
        <router-view/>
      </div>

    </template>
  </authenticator>
</template>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.user-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #f5f5f5;
}

.user-header button {
  padding: 8px 16px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.user-header button:hover {
  background-color: #3aa876;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  text-decoration: none;
  margin: 0 10px;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
