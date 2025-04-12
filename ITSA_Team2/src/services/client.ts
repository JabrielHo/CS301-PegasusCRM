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
    // console.log('User added to group successfully:', result);
    return result
  } catch (error){
    // console.log('Error adding user to group:', error);
    throw error;
  }
}

export async function removeUserFromGroup(userId, groupName) {
  try{
    const result = await client.mutations.removeUserFromGroup({
      groupName: groupName,
      userId: userId,
    })
    // console.log('User remove from group successfully:', result);
    return result
  } catch (error){
    // console.log('Error removing user from group:', error);
    throw error;
  }
}

export async function createUserToGroup(email, firstName, lastName, temporaryPassword, birthDate) {
  try{
    const result = await client.mutations.createUserToGroup({
      email: email,
      givenName: firstName,
      familyName: lastName,
      temporaryPassword: temporaryPassword,
      birthDate: birthDate
    })
    // console.log('User created successfully:', result);
    return result
  } catch (error){
    // console.log('Error creating user in group:', error);
    throw error;
  }
}

export async function deleteUserFromGroup(email){
  try{
    const result = await client.mutations.deleteUserFromGroup({
      userId: email
    })
    // console.log('User deleted from group successfully:', result);
    return result
  } catch (error){
    // console.log('Error deleting user from group:', error);
    throw error;
  }
}

export async function disableUserInGroup(email){
  try{
    const result = await client.mutations.disableUserInGroup({
      userId: email
    })
    // console.log('User disabled from group successfully:', result);
    return result
  } catch (error){
    // console.log('Error disabling user from group:', error);
    throw error;
  }
}

export async function enableUserInGroup(email){
  try{
    const result = await client.mutations.enableUserInGroup({
      userId: email
    })
    // console.log('User enabled from group successfully:', result);
    return result
  } catch (error){
    // console.log('Error enabling user from group:', error);
    throw error;
  }
}

export async function resetUserPassword(email){
  try{
    const result = await client.mutations.resetUserPassword({
      userId: email
    })
    // console.log('User reset password successfully:', result);
    return result
  } catch (error){
    // console.log('Error reset password:', error);
    throw error;
  }
}

export async function updateUserAttribute(email, firstName, lastName, birthDate) {
  try{
    const result = await client.mutations.updateUserAttribute({
      email: email,
      givenName: firstName,
      familyName: lastName,
      birthDate: birthDate
    })
    // console.log('User updated successfully:', result);
    return result
  } catch (error){
    // console.log('Error updating user in group:', error);
    throw error;
  }
}

export async function getListOfUsers(paginationToken) {
  try{
    const result = await client.queries.getListOfUsers({
      paginationToken : paginationToken
    })
    // console.log('User list retrieved successfully:', result);
    return result
  } catch (error){
    // console.log('Error getting user list:', error);
    throw error;
  }
}

export async function getListOfUsersFromGroups(paginationToken, groupName) {
  try{
    const result = await client.queries.listUsersInGroup({
      paginationToken : paginationToken,
      groupName : groupName
    })
    // console.log('User list retrieved successfully:', result);
    return result
  } catch (error){
    // console.log('Error getting user list:', error);
    throw error;
  }
}


export async function getUser(email) {
  try{
    const result = await client.queries.getUser({
      userId : email
    })
    // console.log('User list retrieved successfully:', result);
    return result
  } catch (error){
    // console.log('Error getting user list:', error);
    throw error;
  }
}

