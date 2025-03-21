// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../pages/HomeView.vue';
import addUserToGroup from '../components/addUserToGroup.vue';
import createUser from '../components/createUser.vue';
import deleteUser from '../components/deleteUser.vue';
import disableUser from '../components/disableUser.vue';
import enableUser from '../components/enableUser.vue';
import resetUserPassword from '../components/resetUserPassword.vue';
import updateUserAttribute from '../components/updateUserAttribute.vue';

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
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
