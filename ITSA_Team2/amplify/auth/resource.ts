import { defineAuth } from '@aws-amplify/backend';
import { userManagement } from '../functions/userManagement/resource';
/**
 * Define and configure your auth resource
 * @see https://docs.amplify.aws/gen2/build-a-backend/auth
 */
export const auth = defineAuth({
  loginWith: {
    email: true
  },
  // Configure MFA
  multifactor: {
    mode: 'OPTIONAL',
    totp: true,
    sms: true,
  },
  // Define user groups
  groups: ["ADMINS", "AGENTS"],
  // Add preferred username for display purposes
  userAttributes: {
    preferredUsername: {
      mutable: true,
      required: false
    },
    phoneNumber: {
      required: true
    }
  },
  access: (allow) => [
    allow.resource(userManagement).to([
      "manageUsers", 
      "manageGroupMembership",
      "addUserToGroup",
      "createUser",
      "deleteUser",
      "disableUser",
      "enableUser",
      "getUser",
      "listUsers",
      "listGroupsForUser",
      "listUsersInGroup",
      "removeUserFromGroup",
      "resetUserPassword",
      "setUserPassword",
      "updateUserAttributes"
    ])
  ]
});