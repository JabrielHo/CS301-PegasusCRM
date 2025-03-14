// src/services/UserService.js
import { generateClient } from 'aws-amplify/api';

const client = generateClient();

export const UserService = {
  async createUser(userData) {
    try {
      const response = await client.graphql({
        query: `
          mutation CreateUser(
            $email: String!
            $password: String!
            $firstName: String!
            $lastName: String!
            $phoneNumber: String
            $role: String!
          ) {
            createUser(
              email: $email
              password: $password
              firstName: $firstName
              lastName: $lastName
              phoneNumber: $phoneNumber
              role: $role
            ) {
              id
              email
              firstName
              lastName
              role
              status
            }
          }
        `,
        variables: {
          email: userData.email,
          password: userData.password,
          firstName: userData.firstName,
          lastName: userData.lastName,
          phoneNumber: userData.phoneNumber || '',
          role: userData.role
        }
      });
      return response.data.createUser;
    } catch (error) {
      console.error('Error creating user:', error);
      throw error;
    }
  },

  async disableUser(email) {
    try {
      const response = await client.graphql({
        query: `
          mutation DisableUser($email: String!) {
            disableUser(email: $email) {
              message
              success
            }
          }
        `,
        variables: { email }
      });
      return response.data.disableUser;
    } catch (error) {
      console.error('Error disabling user:', error);
      throw error;
    }
  },

  async updateUser(userData) {
    try {
      const response = await client.graphql({
        query: `
          mutation UpdateUser(
            $email: String!
            $firstName: String
            $lastName: String
            $phoneNumber: String
          ) {
            updateUser(
              email: $email
              firstName: $firstName
              lastName: $lastName
              phoneNumber: $phoneNumber
            ) {
              message
              success
            }
          }
        `,
        variables: {
          email: userData.email,
          firstName: userData.firstName,
          lastName: userData.lastName,
          phoneNumber: userData.phoneNumber
        }
      });
      return response.data.updateUser;
    } catch (error) {
      console.error('Error updating user:', error);
      throw error;
    }
  }
};
