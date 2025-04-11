import axios from 'axios';
import { fetchAuthSession } from 'aws-amplify/auth';

const axiosInstance = axios.create({
  baseURL: 'https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor
axiosInstance.interceptors.request.use(
  async (config) => {
    try {
      // Fetch the current session
      const session = await fetchAuthSession();
      
      // Get the ID token as a string (using toString() method)
      const idToken = session.tokens.idToken.toString();
      
      // Add the token to the Authorization header
      if (idToken) {
        config.headers.Authorization = `Bearer ${idToken}`;
      }
    } catch (error) {
      console.error('Error fetching auth token:', error);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;