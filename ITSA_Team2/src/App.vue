<template>
  <div :class="isLoggedIn ? 'app-container' : 'auth-container'">
    <!-- Customized Authenticator -->
    <authenticator :hide-sign-up="true">
      <!-- Custom Header Slot - Logo and branding -->
      <template v-slot:header>
        <div class="auth-header">
          <img src="../src/assets/Pegasus2.png" alt="Pegasus Logo" class="auth-logo">
          <h1 class="auth-title">Pegasus</h1>
        </div>
      </template>

      <!-- Custom Footer Slot -->
      <template v-slot:footer>
        <div class="auth-footer">
          <p>Secure login provided by Pegasus</p>
        </div>
      </template>

      <!-- Main App Content (Same as before) -->
      <template v-slot="{ user, signOut }">
        <div id="app">
          <header class="app-header">
            <div class="logo-container">
              <router-link :to="isAdmin ? '/admin-dashboard' : isAgent ? '/agent-dashboard' : '/'" class="logo-link">
                <img src="../src/assets/Pegasus2.png" alt="">
                <h1 class="logo">Pegasus</h1>
              </router-link>
            </div>
            <div class="user-info">
              <div class="user-details">
                <h3>{{ displayName }}</h3>
                <span class="role-badge">{{ roleName }}</span>
              </div>
              <button class="sign-out-btn" @click="signOut">
                <i class="bi bi-power"></i>
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
              <!-- <router-link to="/agent-view-transactions" class="nav-link">
                <span class="nav-icon">💰</span>
                Transactions
              </router-link> -->
              <router-link to="/agent-manage-profiles" class="nav-link">
                <span class="nav-icon">📁</span>
                Manage Clients
              </router-link>
            </div>
          </nav>

          <!-- Content area -->
          <main class="content-area">
            <router-view />
          </main>
        </div>
      </template>
    </authenticator>
  </div>
</template>

<script setup>
import { Authenticator, useAuthenticator } from "@aws-amplify/ui-vue";
import "@aws-amplify/ui-vue/styles.css";
import { useRouter } from 'vue-router';
import { ref, onMounted, watch } from 'vue';
import { Amplify } from 'aws-amplify';
import { fetchUserAttributes, fetchAuthSession } from 'aws-amplify/auth';
import outputs from '../amplify_outputs.json';
import { cognitoUserPoolsTokenProvider } from 'aws-amplify/auth/cognito';
import { sessionStorage } from 'aws-amplify/utils';


Amplify.configure(outputs);

cognitoUserPoolsTokenProvider.setKeyValueStorage(sessionStorage);

const displayName = ref('');
const roleName = ref('');
const isAdmin = ref(false);
const isAgent = ref(false);
const auth = useAuthenticator();
const router = useRouter();
const isLoggedIn = ref(false);

// Function to fetch user data
const fetchUserData = async () => {
  try {
    const userAttributes = await fetchUserAttributes();

    // Use preferred_username if available, otherwise fall back to username or email
    displayName.value = `${userAttributes.given_name} ${userAttributes.family_name}` || userAttributes.email || 'User';
    const session = await fetchAuthSession();
    const userGroups = session.tokens.accessToken.payload["cognito:groups"] || [];
    // console.log("Session:", session);
    // console.log("User:", userAttributes);
    roleName.value = userGroups.join(', ');

    isAdmin.value = userGroups.includes('ADMINS') || userGroups.includes('ROOT_ADMIN');
    isAgent.value = userGroups.includes('AGENTS');

    if (isAdmin.value) {
      router.push('/admin-dashboard');
    } else if (isAgent.value) {
      router.push('/agent-dashboard');
    } else {
      router.push('/unauthorized');
    }
  } catch (error) {
    console.error('Error fetching user attributes:', error);
    displayName.value = 'User';
  }
};

// Watch for changes in the user object
watch(() => auth.user, (newUser) => {
  if (newUser) {
    isLoggedIn.value = true;
    fetchUserData();
  } else {
    isLoggedIn.value = false;
    displayName.value = '';
    roleName.value = '';
  }
});

// Initial fetch when the component is mounted
onMounted(() => {
  if (auth.user) {
    isLoggedIn.value = true;
    fetchUserData();
  } else {
    isLoggedIn.value = false;
  }
});
</script>

<style>
/* Global Amplify Authenticator overrides */
:root {
  --amplify-colors-background-primary: #ffffff;
  --amplify-colors-background-secondary: #f9fafb;
  --amplify-colors-brand-primary-10: #e6f7ff;
  --amplify-colors-brand-primary-80: #00b8d9;
  --amplify-colors-brand-primary-90: #00a3c4;
  --amplify-colors-brand-primary-100: #00d9e8;
  --amplify-colors-font-interactive: #00a3c4;
  --amplify-components-button-primary-background-color: #00d9e8;
  --amplify-components-button-primary-hover-background-color: #00a3c4;
  --amplify-components-button-primary-focus-background-color: #00a3c4;
  --amplify-components-button-primary-active-background-color: #00b8d9;
  --amplify-components-tabs-item-active-color: #00d9e8;
  --amplify-components-tabs-item-active-border-color: #00d9e8;
  --amplify-components-tabs-item-color: #5f6b7c;
  --amplify-components-text-input-border-color: #d1d5db;
  --amplify-components-field-label-color: #374151;
  --amplify-components-text-color: #374151;
}

/* Card styling */
[data-amplify-authenticator] [data-amplify-container] {
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  padding: 2rem;
  max-width: 450px;
  border: none;
}

/* Input fields */
[data-amplify-authenticator] input {
  border-radius: 6px;
  border: 1px solid #d1d5db;
  padding: 12px;
  transition: all 0.2s ease;
}

[data-amplify-authenticator] input:focus {
  border-color: var(--amplify-colors-brand-primary-80);
  box-shadow: 0 0 0 3px var(--amplify-colors-brand-primary-10);
}

/* Buttons */
[data-amplify-authenticator] [data-amplify-button] {
  border-radius: 6px;
  font-weight: 600;
  font-size: 16px;
  padding: 12px 20px;
  transition: all 0.2s ease;
}

/* Custom slots styling */
.auth-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.5rem;
}

.auth-logo {
  width: 60px;
  height: auto;
  margin-bottom: 0.5rem;
}

.auth-title {
  font-size: 28px;
  font-weight: 700;
  color: #00d9e8;
  margin: 0;
}

.auth-footer {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 14px;
  color: #6b7280;
}
</style>

<style scoped>
.app-container {
  display: block;
}

.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #f9fafb 0%, #e6f7ff 100%);
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
  width: 35px;
  height: auto;
  margin-right: 10px;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
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