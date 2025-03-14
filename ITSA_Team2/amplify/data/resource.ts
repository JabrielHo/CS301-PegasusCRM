// data/resource.ts
import { a, defineData } from '@aws-amplify/backend';
import { userManagement } from '../functions/userManagement/resource';

const schema = a.schema({
  // Define custom types for return values
  UserResponse: a.customType({
    id: a.string(),
    email: a.string(),
    firstName: a.string(),
    lastName: a.string(),
    role: a.string(),
    status: a.string()
  }),
  
  AdminStatusResponse: a.customType({
    message: a.string(),
    success: a.boolean()
  }),
  
  UserStatusResponse: a.customType({
    message: a.string(),
    success: a.boolean()
  }),
  
  // Add a dummy query to satisfy the schema requirement
  getVersion: a.query()
    .returns(a.string())
    .authorization(allow => [allow.publicApiKey()])
    .handler(a.handler.function(userManagement)),
  
  // Define custom API routes that connect to your Lambda function
  createUser: a.mutation()
    .arguments({ 
      email: a.string().required(),
      password: a.string().required(),
      firstName: a.string().required(),
      lastName: a.string().required(),
      phoneNumber: a.string(),
      role: a.string().required()
    })
    .returns(a.ref('UserResponse'))
    .authorization(allow => [allow.groups(['ADMINS'])])
    .handler(a.handler.function(userManagement)),
  
  disableUser: a.mutation()
    .arguments({ email: a.string().required() })
    .returns(a.ref('AdminStatusResponse'))
    .authorization(allow => [allow.groups(['ADMINS'])])
    .handler(a.handler.function(userManagement)),
  
  updateUser: a.mutation()
    .arguments({ 
      email: a.string().required(),
      firstName: a.string(),
      lastName: a.string(),
      phoneNumber: a.string()
    })
    .returns(a.ref('AdminStatusResponse'))
    .authorization(allow => [allow.groups(['ADMINS'])])
    .handler(a.handler.function(userManagement)),
  
  resetPassword: a.mutation()
    .arguments({ email: a.string().required() })
    .returns(a.ref('UserStatusResponse'))
    .authorization(allow => [allow.authenticated()])
    .handler(a.handler.function(userManagement))
});

export const data = defineData({
    schema,
    authorizationModes: {
      defaultAuthorizationMode: 'userPool',
      apiKeyAuthorizationMode: {
        expiresInDays: 30
      }
    }
  });
  