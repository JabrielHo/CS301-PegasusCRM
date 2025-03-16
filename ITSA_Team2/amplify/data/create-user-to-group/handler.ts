import type { Schema } from "../resource"
import { env } from "$amplify/env/create-user-to-group"
import {
  CognitoIdentityProviderClient,
  AdminCreateUserCommand
} from "@aws-sdk/client-cognito-identity-provider"

type Handler = Schema["createUserToGroup"]["functionHandler"]
const client = new CognitoIdentityProviderClient()

export const handler: Handler = async (event) => {
  const { email, preferredusername, temporaryPassword  } = event.arguments
  const command = new AdminCreateUserCommand({
    UserPoolId: env.AMPLIFY_AUTH_USERPOOL_ID,
    Username: email,
    UserAttributes: [
        {
            Name: "email",
            Value: email
        },
        {
            Name: "preferred_username",
            Value: preferredusername
        }
    ],
    TemporaryPassword: temporaryPassword
  })
  const response = await client.send(command)
  return response
}