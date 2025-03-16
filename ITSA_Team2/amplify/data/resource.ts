import type { ClientSchema } from "@aws-amplify/backend"
import { a, defineData } from "@aws-amplify/backend"
import { addUserToGroup } from "./add-user-to-group/resource"
import { getVersion } from "./get-version/resource"
import { createUserToGroup } from "./create-user-to-group/resource"

const schema = a.schema({
  getVersion: a
  .query()
  .returns(a.string())
  .authorization((allow) => [allow.group("ADMINS")])
  .handler(a.handler.function(getVersion)),

  addUserToGroup: a
    .mutation()
    .arguments({
      userId: a.string().required(),
      groupName: a.string().required(),
    })
    .authorization((allow) => [allow.group("ADMINS")])
    .handler(a.handler.function(addUserToGroup))
    .returns(a.json()),
    
  createUserToGroup: a
    .mutation()
    .arguments({
      email: a.string().required(),
      preferredusername: a.string().required(),
      temporaryPassword: a.string().required(), // Optional, system will generate one if not provided
    })
    .authorization((allow) => [allow.group("ADMINS")])
    .handler(a.handler.function(createUserToGroup))
    .returns(a.json())
})

export type Schema = ClientSchema<typeof schema>

export const data = defineData({
  schema,
  authorizationModes: {
    defaultAuthorizationMode: "iam",
  },
})
