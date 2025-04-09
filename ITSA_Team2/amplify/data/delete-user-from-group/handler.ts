import type { Schema } from "../resource"
import { env } from "$amplify/env/delete-user-from-group"
import {
  CognitoIdentityProviderClient,
  AdminDeleteUserCommand,
  AdminListGroupsForUserCommand
} from "@aws-sdk/client-cognito-identity-provider"
import type { AppSyncIdentityCognito } from "aws-lambda";
import { validateAdminOrRootAccess } from "../../utils/auth-utils"

type Handler = Schema["deleteUserFromGroup"]["functionHandler"]
const client = new CognitoIdentityProviderClient()

export const handler: Handler = async (event) => {
  await validateAdminOrRootAccess(event);
  const { userId } = event.arguments

  // Get requester's userId from Cognito token
  const requesterUserId = (event.identity as AppSyncIdentityCognito)?.username

  const groupsResponse = await client.send(
    new AdminListGroupsForUserCommand({
      Username: userId,
      UserPoolId: env.AMPLIFY_AUTH_USERPOOL_ID
    })
  )
  const targetGroups = groupsResponse.Groups?.map(g => g.GroupName) || [];
  // This is assuming more than one root admin
  if (targetGroups.includes("ROOT_ADMIN")) {
    throw new Error("ROOT_ADMIN users cannot be deleted");
  }

  // Prevent a user from deleting themselves
  if (userId === requesterUserId) {
    throw new Error("You cannot delete your own account.");
  }
  const command = new AdminDeleteUserCommand({
    Username: userId,
    UserPoolId: env.AMPLIFY_AUTH_USERPOOL_ID,
  })
  const response = await client.send(command)
  return response
}