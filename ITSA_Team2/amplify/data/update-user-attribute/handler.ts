import type { Schema } from "../resource"
import { env } from "$amplify/env/create-user-to-group"
import {
  CognitoIdentityProviderClient,
  AdminUpdateUserAttributesCommand
} from "@aws-sdk/client-cognito-identity-provider"

type Handler = Schema["updateUserAttribute"]["functionHandler"]
const client = new CognitoIdentityProviderClient()

export const handler: Handler = async (event) => {
  const { email, givenName, familyName  } = event.arguments
  const command = new AdminUpdateUserAttributesCommand({
    UserPoolId: env.AMPLIFY_AUTH_USERPOOL_ID,
    Username: email,
    UserAttributes: [
        // {
        //     Name: "email",
        //     Value: email
        // },
        {
            Name: "given_name",
            Value: givenName
        },
        {
            Name: "family_name",
            Value: familyName
        }
    ],
  })
  const response = await client.send(command)
  return response
}