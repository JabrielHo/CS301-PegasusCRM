// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../pages/HomeView.vue';
<<<<<<< Updated upstream
=======
import AdminDashboard from '../pages/AdminDashboard.vue';
import AdminManageAccount from '../pages/AdminManageAccount.vue';
import AdminCreateAccount from '../pages/AdminCreateAccount.vue';
import AdminAgentActivities from '../pages/AdminAgentActivities.vue';
import AgentDashboard from '../pages/AgentDashboard.vue';
import AgentCreateClientProfile from '../pages/AgentCreateClientProfile.vue';
import AgentViewTransactions from '../pages/AgentViewTransactions.vue';
import AgentManageProfiles from '../pages/AgentManageProfiles.vue';

// Components
>>>>>>> Stashed changes
import addUserToGroup from '../components/addUserToGroup.vue';
import createUser from '../components/createUser.vue';
import deleteUser from '../components/deleteUser.vue';
import disableUser from '../components/disableUser.vue';
import enableUser from '../components/enableUser.vue';
import resetUserPassword from '../components/resetUserPassword.vue';
import updateUserAttribute from '../components/updateUserAttribute.vue';
import getListOfUsers from '../components/getListOfUsers.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
<<<<<<< Updated upstream
=======
    path: '/admin-dashboard',
    name: 'Admin Dashboard',
    component: AdminDashboard
  },
  {
    path: '/admin-manage-account',
    name: 'Admin Manage Account',
    component: AdminManageAccount
  },
  {
    path: '/admin-create-account',
    name: 'Admin Create Account',
    component: AdminCreateAccount
  },
  {
    path: '/admin-agent-activities',
    name: 'Admin Agent Activities',
    component: AdminAgentActivities
  },
  {
    path: '/agent-dashboard',
    name: 'Agent Dashboard',
    component: AgentDashboard
  },
  {
    path: '/agent-create-client-profile',
    name: 'Agent Create Client Profile',
    component: AgentCreateClientProfile
  },
  {
    path: '/agent-view-transactions',
    name: 'Agent View Transactions',
    component: AgentViewTransactions
  },
  {
    path: '/agent-manage-profiles',
    name: 'Agent Manage Profiles',
    component: AgentManageProfiles
  },



  // Components
  {
>>>>>>> Stashed changes
    path: '/addUserToGroup',
    name: 'addUserToGroup',
    component: addUserToGroup,
  },
  {
    path: '/createUser',
    name: 'createUser',
    component: createUser,
  },
  {
    path: '/deleteUser',
    name: 'deleteUser',
    component: deleteUser,
  },
  {
    path: '/disableUser',
    name: 'disableUser',
    component: disableUser,
  },
  {
    path: '/enableUser',
    name: 'enableUser',
    component: enableUser,
  },
  {
    path: '/resetUserPassword',
    name: 'resetUserPassword',
    component: resetUserPassword,
  },
  {
    path: '/updateUserAttribute',
    name: 'updateUserAttribute',
    component: updateUserAttribute,
  },
  {
    path: '/getListOfUsers',
    name: 'getListOfUsers',
    component: getListOfUsers,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
