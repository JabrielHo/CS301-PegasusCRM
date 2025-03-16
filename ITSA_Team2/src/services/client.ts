import type { Schema } from "../../amplify/data/resource"
import { generateClient } from "aws-amplify/data"

const client = generateClient<Schema>({
  authMode: 'userPool' // Use the appropriate auth mode for your API
})

// await client.mutations.addUserToGroup({
//   groupName: "ADMINS",
//   userId: "5468d468-4061-70ed-8870-45c766d26225",
// })

export async function addUserToGroup(userId, groupName) {
  try{
    const result = await client.mutations.addUserToGroup({
      groupName: groupName,
      userId: userId,
    })
    console.log('User added to group successfully:', result);
    return result
  } catch (error){
    console.log('Error adding user to group:', error);
    throw error;
  }
}

export async function createUserToGroup(email, userName, temporaryPassword) {
  try{
    const result = await client.mutations.createUserToGroup({
      email: email,
      preferredusername: userName,
      temporaryPassword: temporaryPassword
    })
    console.log('User created successfully:', result);
    return result
  } catch (error){
    console.log('Error creating user in group:', error);
    throw error;
  }
}