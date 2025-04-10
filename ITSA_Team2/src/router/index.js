// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
// Pages
import HomeView from "../pages/HomeView.vue";
import AdminDashboard from "../pages/AdminDashboard.vue";
import AdminManageAccount from "../pages/AdminManageAccount.vue";
import AdminCreateAccount from "../pages/AdminCreateAccount.vue";
import AdminAgentActivities from "../pages/AdminAgentActivities.vue";
import AgentDashboard from "../pages/AgentDashboard.vue";
import AgentCreateClientProfile from "../pages/AgentCreateClientProfile.vue";
import AgentViewTransactions from "../pages/AgentViewTransactions.vue";
import AgentManageProfiles from "../pages/AgentManageProfiles.vue";

// Components
import addUserToGroup from "../components/addUserToGroup.vue";
import createUser from "../components/createUser.vue";
import deleteUser from "../components/deleteUser.vue";
import disableUser from "../components/disableUser.vue";
import enableUser from "../components/enableUser.vue";
import resetUserPassword from "../components/resetUserPassword.vue";
import updateUserAttribute from "../components/updateUserAttribute.vue";
import getListOfUsers from "../components/getListOfUsers.vue";

const routes = [
  // Pages
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/admin-dashboard",
    name: "Admin Dashboard",
    component: AdminDashboard,
    meta: { roles: ["ADMINS", "ROOT_ADMIN"] }, // Only ADMINS can access
  },
  {
    path: "/admin-manage-account",
    name: "Admin Manage Account",
    component: AdminManageAccount,
    meta: { roles: ["ADMINS", "ROOT_ADMIN"] }, // Only ADMINS can access
  },
  {
    path: "/admin-create-account",
    name: "Admin Create Account",
    component: AdminCreateAccount,
    meta: { roles: ["ADMINS", "ROOT_ADMIN"] },
  },
  {
    path: "/admin-agent-activities",
    name: "Admin Agent Activities",
    component: AdminAgentActivities,
    // Going to delete
  },
  {
    path: "/agent-dashboard",
    name: "Agent Dashboard",
    component: AgentDashboard,
    meta: { roles: ["AGENTS"] },
  },
  {
    path: "/agent-create-client-profile",
    name: "Agent Create Client Profile",
    component: AgentCreateClientProfile,
    meta: { roles: ["AGENTS"] },
  },
  {
    path: "/agent-view-transactions",
    name: "Agent View Transactions",
    component: AgentViewTransactions,
    meta: { roles: ["AGENTS"] },
  },
  {
    path: "/agent-manage-profiles",
    name: "Agent Manage Profiles",
    component: AgentManageProfiles,
    meta: { roles: ["AGENTS"] },
  },

  {
    path: '/unauthorized',
    name: 'Unauthorized',
    component: () => import('../pages/Unauthorized.vue'),
  },  

  // Components
  {
    path: "/addUserToGroup",
    name: "addUserToGroup",
    component: addUserToGroup,
  },
  {
    path: "/createUser",
    name: "createUser",
    component: createUser,
  },
  {
    path: "/deleteUser",
    name: "deleteUser",
    component: deleteUser,
  },
  {
    path: "/disableUser",
    name: "disableUser",
    component: disableUser,
  },
  {
    path: "/enableUser",
    name: "enableUser",
    component: enableUser,
  },
  {
    path: "/resetUserPassword",
    name: "resetUserPassword",
    component: resetUserPassword,
  },
  {
    path: "/updateUserAttribute",
    name: "updateUserAttribute",
    component: updateUserAttribute,
  },
  {
    path: "/getListOfUsers",
    name: "getListOfUsers",
    component: getListOfUsers,
  },
];

import { fetchAuthSession } from "aws-amplify/auth";

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const requiredRoles = to.meta.roles;

  if (!requiredRoles) {
    // If no roles are required, allow access
    return next();
  }

  try {
    const session = await fetchAuthSession();
    const userGroups =
      session.tokens.accessToken.payload["cognito:groups"] || [];

    // Check if the user has at least one of the required roles
    const hasAccess = requiredRoles.some((role) => userGroups.includes(role));

    if (hasAccess) {
      next();
    } else {
      next("/unauthorized"); // Redirect to an unauthorized page or login
    }
  } catch (error) {
    console.error("Error checking user roles:", error);
    next("/"); // Redirect to login if there's an error
  }
});

export default router;
