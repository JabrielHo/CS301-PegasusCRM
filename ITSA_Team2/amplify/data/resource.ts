import type { ClientSchema } from "@aws-amplify/backend"
import { a, defineData } from "@aws-amplify/backend"
import { addUserToGroup } from "./add-user-to-group/resource"
import { getVersion } from "./get-version/resource"
import { createUserToGroup } from "./create-user-to-group/resource"
import { deleteUserFromGroup } from "./delete-user-from-group/resource"
import { disableUserInGroup } from "./disable-user-in-group/resource"
import { enableUserInGroup } from "./enable-user-in-group/resource"
import { resetUserPassword } from "./reset-user-password/resource"
import { updateUserAttribute } from "./update-user-attribute/resource"
import { getListOfUsers } from "./get-list-of-users/resource"
import { removeUserFromGroup } from "./remove-user-from-group/resource"

const schema = a.schema({
  getVersion: a
  .query()
  .returns(a.string())
  .authorization((allow) => [allow.group("ADMINS")])
  .handler(a.handler.function(getVersion)),

  getListOfUsers: a
  .query()
  .arguments({
    paginationToken : a.string()
  })
  .authorization((allow) => [allow.group("ADMINS")])
  .handler(a.handler.function(getListOfUsers))
  .returns(a.json()),

  addUserToGroup: a
    .mutation()
    .arguments({
      userId: a.string().required(),
      groupName: a.string().required(),
    })
    .authorization((allow) => [allow.group("ADMINS")])
    .handler(a.handler.function(addUserToGroup))
    .returns(a.json()),

  removeUserFromGroup: a
    .mutation()
    .arguments({
      userId: a.string().required(),
      groupName: a.string().required(),
    })
    .authorization((allow) => [allow.group("ADMINS")])
    .handler(a.handler.function(removeUserFromGroup))
    .returns(a.json()),
    
  createUserToGroup: a
    .mutation()
    .arguments({
      email: a.string().required(),
      givenName: a.string().required(),
      familyName: a.string().required(),
      temporaryPassword: a.string().required(), // Optional, system will generate one if not provided
    })
    .authorization((allow) => [allow.group("ADMINS")])
    .handler(a.handler.function(createUserToGroup))
    .returns(a.json()),

  deleteUserFromGroup: a
    .mutation()
    .arguments({
      userId: a.string().required()
    })
    .authorization((allow) => [allow.group("ADMINS")])
    .handler(a.handler.function(deleteUserFromGroup))
    .returns(a.json()),

  disableUserInGroup: a
    .mutation()
    .arguments({
      userId: a.string().required()
    })
    .authorization((allow) => [allow.group("ADMINS")])
    .handler(a.handler.function(disableUserInGroup))
    .returns(a.json()),

  enableUserInGroup: a
    .mutation()
    .arguments({
      userId: a.string().required()
    })
    .authorization((allow) => [allow.group("ADMINS")])
    .handler(a.handler.function(enableUserInGroup))
    .returns(a.json()),

  resetUserPassword: a
    .mutation()
    .arguments({
      userId: a.string().required()
    })
    .authorization((allow) => [allow.group("ADMINS")])
    .handler(a.handler.function(resetUserPassword))
    .returns(a.json()),

  updateUserAttribute: a
    .mutation()
    .arguments({
      email: a.string().required(),
      givenName: a.string().required(),
      familyName: a.string().required(),
    })
    .authorization((allow) => [allow.group("ADMINS")])
    .handler(a.handler.function(updateUserAttribute))
    .returns(a.json()),

})

export type Schema = ClientSchema<typeof schema>

export const data = defineData({
  schema,
  authorizationModes: {
    defaultAuthorizationMode: "iam",
  },
})
