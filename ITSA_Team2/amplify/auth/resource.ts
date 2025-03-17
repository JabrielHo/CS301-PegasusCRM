import { defineAuth } from '@aws-amplify/backend';
import { addUserToGroup } from '../data/add-user-to-group/resource'
import { createUserToGroup } from '../data/create-user-to-group/resource';
import { deleteUserFromGroup } from '../data/delete-user-from-group/resource'
import { disableUserInGroup } from '../data/disable-user-in-group/resource';
import { enableUserInGroup } from '../data/enable-user-in-group/resource'
import { resetUserPassword } from '../data/reset-user-password/resource';
/**
 * Define and configure your auth resource
 * @see https://docs.amplify.aws/gen2/build-a-backend/auth
 */
export const auth = defineAuth({
  loginWith: {
    email: true
  },
  // Configure MFA
  // multifactor: {
  //   mode: 'OPTIONAL',
  //   totp: true,
  //   sms: true,
  // },
  // Define user groups
  groups: ["ADMINS", "AGENTS"],
  // Add preferred username for display purposes
  userAttributes: {
    preferredUsername: {
      mutable: true,
      required: true
    },
    // phoneNumber: {
    //   required: true
    // }
  },
  access: (allow) => [
    allow.resource(addUserToGroup).to([
      "addUserToGroup"
    ]),
    allow.resource(createUserToGroup).to([
      "createUser"
    ]),
    allow.resource(deleteUserFromGroup).to([
      "deleteUser"
    ]),
    allow.resource(disableUserInGroup).to([
      "disableUser"
    ]),
    allow.resource(enableUserInGroup).to([
      'enableUser'
    ]),
    allow.resource(resetUserPassword).to([
      'resetUserPassword'
    ]),
  ]
});