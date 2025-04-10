<template>
  <div :class="isLoggedIn ? 'app-container' : 'auth-container'">
  <authenticator :hide-sign-up="true">
    <template v-slot="{ user, signOut }">
      <div id="app">
        <header class="app-header">
          <div class="logo-container">
            <router-link
              :to="isAdmin ? '/admin-dashboard' : isAgent ? '/agent-dashboard' : '/'"
              class="logo-link"
            >
              <img src="../src/assets/pegasus.png" alt="">
              <h1 class="logo">Pegasus</h1>
            </router-link>
          </div>
          <div class="user-info">
            <div class="user-details">
              <h3>{{ displayName }}</h3>
              <span class="role-badge">{{ roleName }}</span>
            </div>
            <button class="sign-out-btn" @click="signOut">
              <span class="sign-out-icon">⏻</span>
              Sign Out
            </button>
          </div>
        </header>
        
        <!-- Enhanced Navigation Bar -->
        <nav class="main-nav">
          <!-- Admin Links -->
          <div v-if="isAdmin" class="nav-links">
            <router-link to="/admin-dashboard" class="nav-link">
              <span class="nav-icon">📊</span>
              Dashboard
            </router-link>
            <router-link to="/admin-create-account" class="nav-link">
              <span class="nav-icon">➕</span>
              Create Account
            </router-link>
            <router-link to="/admin-manage-account" class="nav-link">
              <span class="nav-icon">⚙️</span>
              Manage Accounts
            </router-link>
            <router-link to="/admin-agent-activities" class="nav-link">
              <span class="nav-icon">📝</span>
              Agent Activities
            </router-link>
          </div>
          
          <!-- Agent links -->
          <div v-if="isAgent" class="nav-links">
            <router-link to="/agent-dashboard" class="nav-link">
              <span class="nav-icon">📊</span>
              Dashboard
            </router-link>
            <router-link to="/agent-create-client-profile" class="nav-link">
              <span class="nav-icon">👤</span>
              New Client
            </router-link>
            <router-link to="/agent-view-transactions" class="nav-link">
              <span class="nav-icon">💰</span>
              Transactions
            </router-link>
            <router-link to="/agent-manage-profiles" class="nav-link">
              <span class="nav-icon">📁</span>
              Manage Clients
            </router-link>
          </div>
        </nav>
        
        <!-- Content area -->
        <main class="content-area">
          <router-view/>
        </main>
      </div>
    </template>
  </authenticator>
  </div>
</template>

<script setup>
import { Authenticator, useAuthenticator } from "@aws-amplify/ui-vue";
import "@aws-amplify/ui-vue/styles.css";
import { useRouter } from 'vue-router'; // Import useRouter from vue-router
import { ref, onMounted, watch } from 'vue';
import { Amplify } from 'aws-amplify';
import { fetchUserAttributes, fetchAuthSession } from 'aws-amplify/auth';
import outputs from '../amplify_outputs.json';

Amplify.configure(outputs);

const displayName = ref('');
const roleName = ref('');
const isAdmin = ref(false);
const isAgent = ref(false);
const auth = useAuthenticator();
const router = useRouter(); // Use the router instance
const isLoggedIn = ref(false);

// Function to fetch user data
const fetchUserData = async () => {
  try {
    const userAttributes = await fetchUserAttributes();

    // Use preferred_username if available, otherwise fall back to username or email
    displayName.value = `${userAttributes.given_name} ${userAttributes.family_name}` || userAttributes.email || 'User';
    const session = await fetchAuthSession();
    const userGroups = session.tokens.accessToken.payload["cognito:groups"] || [];
    console.log("Session:", session); // Log user groups for debugging
    console.log("User:", userAttributes); // Log user groups for debugging
    roleName.value = userGroups.join(', '); // Join groups for display

    isAdmin.value = userGroups.includes('ADMINS') || userGroups.includes('ROOT_ADMIN');
    isAgent.value = userGroups.includes('AGENTS');

    if(isAdmin.value) {
      router.push('/admin-dashboard'); // Redirect to admin dashboard
    } else if (isAgent.value) {
      router.push('/agent-dashboard'); // Redirect to agent dashboard
    } else {
      router.push('/unauthorized'); // Redirect to home page for other users
    }
  } catch (error) {
    console.error('Error fetching user attributes:', error);
    displayName.value = 'User';
  }
};

// Watch for changes in the user object
watch(() => auth.user, (newUser) => {
  if (newUser) {
    isLoggedIn.value = true; // Set logged-in state to true
    fetchUserData(); // Fetch user data when the user logs in
  } else {
    isLoggedIn.value = false; // Set logged-in state to false
    displayName.value = ''; // Clear display name
    roleName.value = ''; // Clear role name
  }
});

// Initial fetch when the component is mounted
onMounted(() => {
  if (auth.user) {
    isLoggedIn.value = true; // Set logged-in state to true
    fetchUserData();
  } else {
    isLoggedIn.value = false; // Set logged-in state to false
  }
});
</script>

<style scoped>
.app-container {
  display: block; /* Default layout for logged-in state */
}

.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5; /* Optional background for the login page */
}

#app {
  font-family: 'Roboto', Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #333;
  width: 100%;
  min-height: 100vh;
  background-color: #f9fafb;
}

/* Header styling */
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-container img {
  width: 35px; /* Adjust the width as needed */
  height: auto; /* Maintain aspect ratio */
  margin-right: 10px; /* Space between image and text */
}

.logo-link {
  display: flex;
  align-items: center; /* Vertically align the image and text */
  text-decoration: none; /* Remove underline from the link */
}


.logo {
  font-size: 24px;
  font-weight: 700;
  color: #00d9e8;
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-details {
  text-align: right;
}

.user-details h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.role-badge {
  font-size: 12px;
  background-color: #e8f5e9;
  color: #2e7d32;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.sign-out-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background-color: #f5f5f5;
  color: #333;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.sign-out-btn:hover {
  background-color: #e0e0e0;
}

.sign-out-icon {
  font-size: 14px;
}

/* Navigation bar styling */
.main-nav {
  background-color: #ffffff;
  padding: 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.nav-links {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  padding: 10px 20px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: #555;
  text-decoration: none;
  padding: 10px 16px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background-color: #f5f7fa;
  color: #42b983;
}

.nav-icon {
  font-size: 18px;
}

.nav-link.router-link-exact-active {
  color: #42b983;
  background-color: #e8f5e9;
  font-weight: 600;
}

/* Content area */
.content-area {
  padding: 24px;
  background-color: #ffffff;
  margin: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  min-height: 500px;
}

@media (max-width: 768px) {
  .app-header {
    flex-direction: column;
    padding: 12px;
  }
  
  .user-info {
    margin-top: 10px;
    flex-direction: column;
    gap: 10px;
  }
  
  .nav-links {
    flex-direction: column;
    width: 100%;
  }
  
  .nav-link {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>