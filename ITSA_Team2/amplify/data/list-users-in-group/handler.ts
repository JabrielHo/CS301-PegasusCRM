import type { Schema } from "../resource"
import { env } from "$amplify/env/disable-user-in-group"
import {
  ListUsersInGroupCommand,
  CognitoIdentityProviderClient,
} from "@aws-sdk/client-cognito-identity-provider"
import { validateAdminOrRootAccess } from "../../utils/auth-utils"

type Handler = Schema["listUsersInGroup"]["functionHandler"]
const client = new CognitoIdentityProviderClient()

export const handler: Handler = async (event) => {
  await validateAdminOrRootAccess(event);
  const { paginationToken, groupName } = event.arguments
  const command = new ListUsersInGroupCommand({
    UserPoolId: env.AMPLIFY_AUTH_USERPOOL_ID,
    GroupName: groupName,
    Limit : 5,
    ...(paginationToken ? { NextToken: paginationToken } : {}),
    // Filter: filter
  })
  const response = await client.send(command)
  return response
}