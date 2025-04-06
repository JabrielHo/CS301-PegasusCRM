import type { Schema } from "../resource"
import { env } from "$amplify/env/disable-user-in-group"
import {
  AdminDisableUserCommand,
  CognitoIdentityProviderClient,
} from "@aws-sdk/client-cognito-identity-provider"
import { validateAdminOrRootAccess } from "../../utils/auth-utils"

type Handler = Schema["disableUserInGroup"]["functionHandler"]
const client = new CognitoIdentityProviderClient()

export const handler: Handler = async (event) => {
  await validateAdminOrRootAccess(event);
  const { userId } = event.arguments
  const command = new AdminDisableUserCommand({
    Username: userId,
    UserPoolId: env.AMPLIFY_AUTH_USERPOOL_ID,
  })
  const response = await client.send(command)
  return response
}