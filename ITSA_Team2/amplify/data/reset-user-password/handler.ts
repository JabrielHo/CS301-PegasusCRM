import type { Schema } from "../resource"
import { env } from "$amplify/env/reset-user-password"
import {
  AdminResetUserPasswordCommand,
  CognitoIdentityProviderClient,
} from "@aws-sdk/client-cognito-identity-provider"
import { validateAdminOrRootAccess } from "../../utils/auth-utils"

type Handler = Schema["resetUserPassword"]["functionHandler"]
const client = new CognitoIdentityProviderClient()

export const handler: Handler = async (event) => {
  await validateAdminOrRootAccess(event);
  const { userId } = event.arguments
  const command = new AdminResetUserPasswordCommand({
    Username: userId,
    UserPoolId: env.AMPLIFY_AUTH_USERPOOL_ID,
  })
  const response = await client.send(command)
  return response
}