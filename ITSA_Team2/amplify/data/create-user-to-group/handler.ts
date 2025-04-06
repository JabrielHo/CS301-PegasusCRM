import type { Schema } from "../resource"
import { env } from "$amplify/env/create-user-to-group"
import {
  CognitoIdentityProviderClient,
  AdminCreateUserCommand
} from "@aws-sdk/client-cognito-identity-provider"
import { validateAdminOrRootAccess } from "../../utils/auth-utils"

type Handler = Schema["createUserToGroup"]["functionHandler"]
const client = new CognitoIdentityProviderClient()

export const handler: Handler = async (event) => {
  await validateAdminOrRootAccess(event);
  const { email, givenName, familyName, temporaryPassword  } = event.arguments
  const command = new AdminCreateUserCommand({
    UserPoolId: env.AMPLIFY_AUTH_USERPOOL_ID,
    Username: email,
    UserAttributes: [
        {
            Name: "email",
            Value: email
        },
        {
            Name: "given_name",
            Value: givenName
        },
        {
            Name: "family_name",
            Value: familyName
        }
    ],
    TemporaryPassword: temporaryPassword
  })
  const response = await client.send(command)
  return response
}