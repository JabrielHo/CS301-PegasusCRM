import type { Schema } from "../resource"
import { env } from "$amplify/env/disable-user-in-group"
import {
  AdminEnableUserCommand,
  CognitoIdentityProviderClient,
} from "@aws-sdk/client-cognito-identity-provider"

type Handler = Schema["enableUserInGroup"]["functionHandler"]
const client = new CognitoIdentityProviderClient()

export const handler: Handler = async (event) => {
  const { userId } = event.arguments
  const command = new AdminEnableUserCommand({
    Username: userId,
    UserPoolId: env.AMPLIFY_AUTH_USERPOOL_ID,
  })
  const response = await client.send(command)
  return response
}