<template>
  <div>
    <div v-if="users.length">
      <table>
        <thead>
          <tr>
            <th>Email</th>
            <th>Email Verified</th>
            <th>Given Name</th>
            <th>Family Name</th>
            <th>Sub</th>
            <th>Enabled</th>
            <th>Created Date</th>
            <th>Last Modified</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.Username">
            <td>{{ findAttributeValue(user, 'email') }}</td>
            <td>{{ findAttributeValue(user, 'email_verified') }}</td>
            <td>{{ findAttributeValue(user, 'given_name') }}</td>
            <td>{{ findAttributeValue(user, 'family_name') }}</td>
            <td>{{ findAttributeValue(user, 'sub') }}</td>
            <td>{{ user.Enabled }}</td>
            <td>{{ formatDate(user.UserCreateDate) }}</td>
            <td>{{ formatDate(user.UserLastModifiedDate) }}</td>
            <td>{{ user.UserStatus }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>No users found.</div>

    <div class="pagination">
      <button @click="previousPage" :disabled="!paginationHistory.length">Previous Page</button>
      <button @click="nextPage" :disabled="!hasMoreUsers">Next Page</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { getListOfUsers } from '../services/client.ts'; // Adjust the import path as needed

export default {
  setup() {
    const users = ref([]);
    const paginationToken = ref(null);
    const hasMoreUsers = ref(true);
    const paginationHistory = ref([]);

    const findAttributeValue = (user, attributeName) => {
      const attribute = user.Attributes.find(attr => attr.Name === attributeName);
      return attribute ? attribute.Value : '';
    };

    const formatDate = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString();
    };

    const fetchUsers = async (token = null) => {
      try {
        const result = await getListOfUsers(token);
        
        // No need to parse if result is already an object
        users.value = JSON.parse(result.data) || [];
        users.value = users.value.Users
        
        // Store the pagination token for next page
        paginationToken.value = result.PaginationToken || null;
        hasMoreUsers.value = !!paginationToken.value;
        
        console.log('Users fetched:', users.value);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };

    const nextPage = () => {
      if (hasMoreUsers.value) {
        // Save current token to history for "previous page" functionality
        if (paginationToken.value) {
          paginationHistory.value.push(paginationToken.value);
        }
        fetchUsers(paginationToken.value);
      }
    };

    const previousPage = () => {
      if (paginationHistory.value.length > 0) {
        // Get the previous token (or null for first page)
        const previousToken = paginationHistory.value.length > 1 
          ? paginationHistory.value[paginationHistory.value.length - 2] 
          : null;
        
        // Remove the last token from history
        paginationHistory.value.pop();
        
        fetchUsers(previousToken);
      } else {
        // If no history, go to first page
        fetchUsers();
      }
    };

    onMounted(() => {
      fetchUsers();
    });

    return {
      users,
      nextPage,
      previousPage,
      hasMoreUsers,
      paginationToken,
      paginationHistory,
      findAttributeValue,
      formatDate
    };
  }
}
</script>

<style scoped>
.pagination {
  margin-top: 20px;
}

button {
  margin-right: 10px;
  padding: 5px 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
  font-weight: bold;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}
</style>
