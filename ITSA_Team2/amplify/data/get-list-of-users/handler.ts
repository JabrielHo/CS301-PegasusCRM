import type { Schema } from "../resource"
import { env } from "$amplify/env/disable-user-in-group"
import {
  ListUsersCommand,
  CognitoIdentityProviderClient,
} from "@aws-sdk/client-cognito-identity-provider"
import { validateAdminOrRootAccess } from "../../utils/auth-utils"

type Handler = Schema["getListOfUsers"]["functionHandler"]
const client = new CognitoIdentityProviderClient()

export const handler: Handler = async (event) => {
  await validateAdminOrRootAccess(event);
  const { paginationToken } = event.arguments
  const command = new ListUsersCommand({
    UserPoolId: env.AMPLIFY_AUTH_USERPOOL_ID,
    // AttributesToGet : AttributesToGet,
    Limit : 2,
    ...(paginationToken ? { PaginationToken: paginationToken } : {}),
    // Filter: filter
  })
  const response = await client.send(command)
  return response
}