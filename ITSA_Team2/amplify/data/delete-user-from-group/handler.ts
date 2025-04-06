import type { Schema } from "../resource"
import { env } from "$amplify/env/delete-user-from-group"
import {
  CognitoIdentityProviderClient,
  AdminDeleteUserCommand,
  AdminListGroupsForUserCommand
} from "@aws-sdk/client-cognito-identity-provider"
import type { AppSyncIdentityCognito } from "aws-lambda";

type Handler = Schema["deleteUserFromGroup"]["functionHandler"]
const client = new CognitoIdentityProviderClient()

export const handler: Handler = async (event) => {
  const { userId } = event.arguments

  // Get requester's groups from Cognito token
  const requesterGroups = (
    (event.identity as AppSyncIdentityCognito)?.claims?.["cognito:groups"] || []
  ) as string[];

  const groupsResponse = await client.send(
    new AdminListGroupsForUserCommand({
      Username: userId,
      UserPoolId: env.AMPLIFY_AUTH_USERPOOL_ID
    })
  )
  const targetGroups = groupsResponse.Groups?.map(g => g.GroupName) || [];
  // This is assuming more than one root admin
  if (targetGroups.includes("ROOT_ADMIN") && !requesterGroups.includes("ROOT_ADMIN")) {
    throw new Error("ROOT_ADMIN users cannot be deleted");
  }
  const command = new AdminDeleteUserCommand({
    Username: userId,
    UserPoolId: env.AMPLIFY_AUTH_USERPOOL_ID,
  })
  const response = await client.send(command)
  return response
}