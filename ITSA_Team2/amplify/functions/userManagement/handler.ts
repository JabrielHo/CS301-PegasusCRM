// functions/user-management/handler.ts
import { CognitoIdentityProviderClient, AdminCreateUserCommand, AdminSetUserPasswordCommand, AdminAddUserToGroupCommand, AdminDisableUserCommand, AdminUpdateUserAttributesCommand, AdminResetUserPasswordCommand } from '@aws-sdk/client-cognito-identity-provider';
import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';

const cognito = new CognitoIdentityProviderClient();

// Define interfaces for our data types
interface UserData {
  email: string;
  password?: string;
  firstName?: string;
  lastName?: string;
  role?: string;
  phoneNumber?: string;
}

export const handler = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
  console.log('Event:', JSON.stringify(event));
  
  try {
    const { path, httpMethod } = event;
    const body: UserData = event.body ? JSON.parse(event.body) : {};
    
    // Route to appropriate handler
    if (path === '/api/users' && httpMethod === 'POST') {
      return await createUser(body, event);
    } else if (path === '/api/users/disable' && httpMethod === 'POST') {
      return await disableUser(body, event);
    } else if (path === '/api/users' && httpMethod === 'PUT') {
      return await updateUser(body, event);
    } else if (path === '/api/reset-password' && httpMethod === 'POST') {
      return await resetPassword(body, event);
    }
    
    return {
      statusCode: 404,
      body: JSON.stringify({ message: 'Not Found' })
    };
  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ 
        message: 'Internal Server Error', 
        error: error instanceof Error ? error.message : 'Unknown error' 
      })
    };
  }
};

// Create User function
async function createUser(data: UserData, event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> {
  // Check if requester is admin
  const requesterGroups = getGroupsFromToken(event);
  if (!requesterGroups.includes('ADMINS')) {
    return {
      statusCode: 403,
      body: JSON.stringify({ message: 'Only admins can create users' })
    };
  }
  
  // Validate input
  if (!data.email || !data.password || !data.firstName || !data.lastName || !data.role) {
    return {
      statusCode: 400,
      body: JSON.stringify({ message: 'Missing required fields' })
    };
  }
  
  try {
    // Create user in Cognito
    await cognito.send(new AdminCreateUserCommand({
      UserPoolId: process.env.USER_POOL_ID,
      Username: data.email,
      TemporaryPassword: data.password,
      MessageAction: 'SUPPRESS',
      UserAttributes: [
        { Name: 'email', Value: data.email },
        { Name: 'email_verified', Value: 'true' },
        { Name: 'given_name', Value: data.firstName },
        { Name: 'family_name', Value: data.lastName },
        { Name: 'phone_number', Value: data.phoneNumber || '+12345678900' }
      ]
    }));
    
    // Set permanent password
    await cognito.send(new AdminSetUserPasswordCommand({
      UserPoolId: process.env.USER_POOL_ID,
      Username: data.email,
      Password: data.password,
      Permanent: true
    }));
    
    // Add user to group
    await cognito.send(new AdminAddUserToGroupCommand({
      UserPoolId: process.env.USER_POOL_ID,
      Username: data.email,
      GroupName: data.role
    }));
    
    return {
      statusCode: 201,
      body: JSON.stringify({
        message: 'User created successfully',
        user: {
          email: data.email,
          firstName: data.firstName,
          lastName: data.lastName,
          role: data.role
        }
      })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ 
        message: 'Error creating user', 
        error: error instanceof Error ? error.message : 'Unknown error' 
      })
    };
  }
}

// Disable User function
async function disableUser(data: UserData, event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> {
  // Check if requester is admin
  const requesterGroups = getGroupsFromToken(event);
  if (!requesterGroups.includes('ADMINS')) {
    return {
      statusCode: 403,
      body: JSON.stringify({ message: 'Only admins can disable users' })
    };
  }
  
  if (!data.email) {
    return {
      statusCode: 400,
      body: JSON.stringify({ message: 'Email is required' })
    };
  }
  
  try {
    await cognito.send(new AdminDisableUserCommand({
      UserPoolId: process.env.USER_POOL_ID,
      Username: data.email
    }));
    
    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'User disabled successfully' })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ 
        message: 'Error disabling user', 
        error: error instanceof Error ? error.message : 'Unknown error' 
      })
    };
  }
}

// Update User function
async function updateUser(data: UserData, event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> {
  if (!data.email) {
    return {
      statusCode: 400,
      body: JSON.stringify({ message: 'Email is required' })
    };
  }
  
  try {
    const userAttributes = [];
    
    if (data.firstName) {
      userAttributes.push({
        Name: 'given_name',
        Value: data.firstName
      });
    }
    
    if (data.lastName) {
      userAttributes.push({
        Name: 'family_name',
        Value: data.lastName
      });
    }
    
    if (data.phoneNumber) {
      userAttributes.push({
        Name: 'phone_number',
        Value: data.phoneNumber
      });
    }
    
    if (userAttributes.length > 0) {
      await cognito.send(new AdminUpdateUserAttributesCommand({
        UserPoolId: process.env.USER_POOL_ID,
        Username: data.email,
        UserAttributes: userAttributes
      }));
    }
    
    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'User updated successfully' })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ 
        message: 'Error updating user', 
        error: error instanceof Error ? error.message : 'Unknown error' 
      })
    };
  }
}

// Reset Password function
async function resetPassword(data: UserData, event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> {
  if (!data.email) {
    return {
      statusCode: 400,
      body: JSON.stringify({ message: 'Email is required' })
    };
  }
  
  try {
    await cognito.send(new AdminResetUserPasswordCommand({
      UserPoolId: process.env.USER_POOL_ID,
      Username: data.email
    }));
    
    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'Password reset initiated. Check email for confirmation code.' })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ 
        message: 'Error resetting password', 
        error: error instanceof Error ? error.message : 'Unknown error' 
      })
    };
  }
}

// Helper function to get groups from token
function getGroupsFromToken(event: APIGatewayProxyEvent): string[] {
  const claims = event.requestContext?.authorizer?.claims;
  if (claims && 'cognito:groups' in claims) {
    return (claims['cognito:groups'] as string).split(',');
  }
  return [];
}
