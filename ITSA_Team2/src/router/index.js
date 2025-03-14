// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import { requireAuth, requireAdmin } from '../services/auth-guards';
import HomeView from '../pages/HomeView.vue';
import UserManagementView from '../pages/UserManagementView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/user-management',
    name: 'userManagement',
    component: UserManagementView,
    beforeEnter: requireAdmin
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
