// src/router/auth-guard.js
import { fetchAuthSession } from 'aws-amplify/auth';

export const requireAuth = async (to, from, next) => {
  try {
    const session = await fetchAuthSession();
    if (session.tokens) {
      next();
    } else {
      next('/login');
    }
  } catch (error) {
    console.error('Auth check failed:', error);
    next('/login');
  }
};

export const requireAdmin = async (to, from, next) => {
  try {
    const session = await fetchAuthSession();
    if (session.tokens) {
      const groups = session.tokens.accessToken.payload['cognito:groups'] || [];
      if (groups.includes('ADMINS')) {
        next();
      } else {
        next('/unauthorized');
      }
    } else {
      next('/login');
    }
  } catch (error) {
    console.error('Admin auth check failed:', error);
    next('/login');
  }
};
