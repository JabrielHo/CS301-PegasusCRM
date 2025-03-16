// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../pages/HomeView.vue';
import addUserToGroup from '../components/addUserToGroup.vue';
import createUser from '../components/createUser.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/addUserToGroup',
    name: 'addUserToGroup',
    component: addUserToGroup,
  },
  {
    path: '/createUser',
    name: 'createUser',
    component: createUser,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
