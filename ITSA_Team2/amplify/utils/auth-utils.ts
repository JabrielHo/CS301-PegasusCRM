// amplify/utils/auth-utils.ts
import { CognitoIdentityProviderClient } from "@aws-sdk/client-cognito-identity-provider";
import type { AppSyncIdentityCognito } from "aws-lambda";
import type { Handler } from "aws-lambda";

const client = new CognitoIdentityProviderClient();

export const validateAdminOrRootAccess = async (
  event: Parameters<Handler>[0]
): Promise<void> => {
  const requesterGroups = (
    (event.identity as AppSyncIdentityCognito)?.claims?.["cognito:groups"] || []
  ) as string[];

  const hasAccess = requesterGroups.some(group => 
    ["ROOT_ADMIN", "ADMINS"].includes(group)
  );
// This works
//   if (hasAccess) {
//     throw new Error("Testing Security at handler");
//   }
  if (!hasAccess) {
    throw new Error("Operation requires ROOT_ADMIN or ADMINS privileges");
  }
};
