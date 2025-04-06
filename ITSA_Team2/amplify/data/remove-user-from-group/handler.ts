import type { Schema } from "../resource"
import { env } from "$amplify/env/remove-user-from-group"
import {
  AdminRemoveUserFromGroupCommand,
  CognitoIdentityProviderClient,
} from "@aws-sdk/client-cognito-identity-provider"
import { validateAdminOrRootAccess } from "../../utils/auth-utils"

type Handler = Schema["removeUserFromGroup"]["functionHandler"]
const client = new CognitoIdentityProviderClient()

export const handler: Handler = async (event) => {
  await validateAdminOrRootAccess(event);
  const { userId, groupName } = event.arguments
  const command = new AdminRemoveUserFromGroupCommand({
    Username: userId,
    GroupName: groupName,
    UserPoolId: env.AMPLIFY_AUTH_USERPOOL_ID,
  })
  const response = await client.send(command)
  return response
}