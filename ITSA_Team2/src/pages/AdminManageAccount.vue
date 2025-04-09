<template>
  <div class="admin-dashboard">
    <!-- Header with Title -->
    <div class="dashboard-header">
      <h1>User Management Dashboard</h1>
      <p class="dashboard-subtitle">Manage administrators and agents with ease</p>
    </div>

    <!-- Toggle Buttons -->
    <div class="toggle-container">
      <button :class="{ active: selectedGroup === 'ADMINS' }" @click="switchGroup('ADMINS')">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
        Administrators
      </button>
      <button :class="{ active: selectedGroup === 'AGENTS' }" @click="switchGroup('AGENTS')">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
        Agents
      </button>
    </div>

    <!-- Search and Account Table -->
    <div class="card">
      <div class="card-header">
        <div class="search-container">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <input id="search" v-model="searchQuery" type="text" placeholder="Search by email or name..." @keyup.enter="performGlobalSearch" />
          <button class="btn-search" @click="performGlobalSearch" title="Search">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            Search
          </button>
        </div>
        <div class="table-info">
          <span v-if="isSearchMode">
            {{ filteredAccounts.length }} of {{ allSearchResults.length }} users found
          </span>
          <span v-else>
            {{ filteredAccounts.length }} users found
          </span>
          <button v-if="isSearchMode" class="btn-clear" @click="clearSearch">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
            Clear Search
          </button>
        </div>
      </div>

      <div class="client-table">
        <table>
          <thead>
            <tr>
              <th>Email</th>
              <th>Given Name</th>
              <th>Family Name</th>
              <th>Status</th>
              <th>Enabled</th>
              <th>Date Of Birth</th>
              <th>Date Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="account in displayedAccounts" :key="account.sub" :class="{ 'disabled-row': !account.enabled }">
              <td>{{ account.email }}</td>
              <td>{{ account.given_name }}</td>
              <td>{{ account.family_name }}</td>
              <td>
                <span :class="'status-badge ' + account.UserStatus.toLowerCase()">
                  {{ account.UserStatus }}
                </span>
              </td>
              <td>
                <span :class="'enabled-badge ' + (account.enabled ? 'enabled' : 'disabled')">
                  {{ account.enabled ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td>{{ account.UserDateOfBirth }}</td>
              <td>{{ formatDate(account.UserCreateDate) }}</td>
              <td>
                <button class="btn-edit" @click="openEditModal(account)" title="Edit User">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                </button>
              </td>
            </tr>
            <tr v-if="displayedAccounts.length === 0">
              <td colspan="8" class="no-results">
                <div class="empty-state">
                  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                  <p>No users found matching your search criteria</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Buttons -->
      <div class="pagination">
        <!-- Show page numbers for search mode -->
        <div v-if="isSearchMode" class="pagination-pages">
          <button 
            v-for="page in totalPages" 
            :key="page" 
            @click="goToPage(page)"
            :class="['page-number', { active: currentPage === page }]">
            {{ page }}
          </button>
        </div>
        <button class="btn-pagination" @click="previousPage" :disabled="isPreviousDisabled">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
          Previous
        </button>
        <button class="btn-pagination" @click="nextPage" :disabled="isNextDisabled">
          Next
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal">
        <div class="modal-header">
          <h3>Edit User</h3>
          <button class="btn-close" @click="closeEditModal">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>
        
        <div class="modal-content">
          <div class="user-email">
            <svg class="user-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
            <span>{{ editUser.email }}</span>
          </div>
          
          <div class="form-group">
            <label for="givenName">Given Name</label>
            <input id="givenName" v-model="editUser.given_name" type="text" />
          </div>

          <div class="form-group">
            <label for="familyName">Family Name</label>
            <input id="familyName" v-model="editUser.family_name" type="text" />
          </div>

          <div class="form-group">
            <label for="birthDate">Birth Date</label>
            <input id="birthDate" v-model="editUser.UserDateOfBirth" type="date" />
          </div>

          <div class="form-section">
            <h4>Account Status</h4>
            <div class="status-toggle">
              <button v-if="editUser.enabled" @click="disableUser" class="btn-disable">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18.36 6.64a9 9 0 1 1-12.73 0"></path><line x1="12" y1="2" x2="12" y2="12"></line></svg>
                Disable User
              </button>
              <button v-if="!editUser.enabled" @click="enableUser" class="btn-enable">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"></path><path d="M12 5v14"></path></svg>
                Enable User
              </button>
            </div>
          </div>

          <div class="form-section">
            <h4>User Role</h4>
            <div class="role-buttons">
              <button v-if="selectedGroup === 'AGENTS'" @click="promoteToAdmin" class="btn-promote">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
                Promote to Admin
              </button>
              <button v-if="selectedGroup === 'ADMINS'" @click="demoteToAgent" class="btn-demote">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="8" y1="12" x2="16" y2="12"></line></svg>
                Demote to Agent
              </button>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <div class="action-buttons">
            <button class="btn-cancel" @click="closeEditModal">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
              Cancel
            </button>
            <button class="btn-save" @click="saveUserChanges">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>
              Save Changes
            </button>
          </div>
          
          <div class="danger-zone">
            <h4>Danger Zone</h4>
            <button class="btn-delete" @click="deleteUser">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
              Delete User
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isSearching" class="modal-overlay">
      <div class="loading-container">
        <div class="loading-spinner"></div>
        <p>Searching all users...</p>
      </div>
    </div>

    <!-- No selection popup -->
    <div v-if="showNoSelectionPopup" class="popup-overlay" @click.self="closePopup">
      <div class="popup">
        <div class="popup-header">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
          <h4>No Selection</h4>
        </div>
        <p>No account is selected. Please select an account to continue.</p>
        <div class="popup-footer">
          <button class="btn-primary" @click="closePopup">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import {
  getListOfUsersFromGroups,
  updateUserAttribute,
  deleteUserFromGroup,
  addUserToGroup,
  removeUserFromGroup,
  disableUserInGroup,
  enableUserInGroup,
} from '../services/client.ts'; // Adjust the import path as needed

export default {
  data() {
    return {
      searchQuery: '',
      accounts: [], // Fetched user accounts
      showEditModal: false, // Flag to show edit modal
      showNoSelectionPopup: false, // Flag to show no selection popup
      editUser: {}, // User data for editing
      paginationToken: null, // Current pagination token
      paginationHistory: [], // History of pagination tokens for "Previous Page"
      hasMoreUsers: true, // Flag to indicate if there are more users to fetch
      selectedGroup: 'ADMINS', // Default group to display
      
      // New properties for enhanced search
      isSearching: false, // Flag to show loading state during global search
      isSearchMode: false, // Flag to indicate if we're in search mode
      allSearchResults: [], // All users from search across pages
      currentPage: 1, // Current page in search results pagination
      usersPerPage: 5, // Number of users to display per page in search results
    };
  },
  computed: {
    // Filter accounts based on the search query (only for standard mode)
    filteredAccounts() {
      if (this.isSearchMode) {
        return this.allSearchResults;
      }
      
      const query = this.searchQuery.toLowerCase();
      return this.accounts.filter(account => {
        return (
          (account.email && account.email.toLowerCase().includes(query)) ||
          (account.given_name && account.given_name.toLowerCase().includes(query)) ||
          (account.family_name && account.family_name.toLowerCase().includes(query))
        );
      });
    },
    
    // Get accounts to display based on current pagination or search mode
    displayedAccounts() {
      if (this.isSearchMode) {
        const start = (this.currentPage - 1) * this.usersPerPage;
        const end = start + this.usersPerPage;
        return this.allSearchResults.slice(start, end);
      }
      return this.filteredAccounts;
    },
    
    // Total pages for search pagination
    totalPages() {
      return Math.ceil(this.allSearchResults.length / this.usersPerPage);
    },
    
    // Check if Previous button should be disabled
    isPreviousDisabled() {
      if (this.isSearchMode) {
        return this.currentPage <= 1;
      }
      return !this.paginationHistory.length;
    },
    
    // Check if Next button should be disabled
    isNextDisabled() {
      if (this.isSearchMode) {
        return this.currentPage >= this.totalPages;
      }
      return !this.hasMoreUsers;
    }
  },
  methods: {
    async fetchUsers(groupName, token = null) {
      try {
        const result = await getListOfUsersFromGroups(token, groupName);
        const parsedResult = JSON.parse(result.data) || [];
        console.log('Fetched users:', parsedResult);

        // Update accounts with the new data
        this.accounts = parsedResult.Users.map(user => ({
          email: user.Attributes.find(attr => attr.Name === 'email')?.Value || '',
          given_name: user.Attributes.find(attr => attr.Name === 'given_name')?.Value || '',
          family_name: user.Attributes.find(attr => attr.Name === 'family_name')?.Value || '',
          sub: user.Attributes.find(attr => attr.Name === 'sub')?.Value || '',
          UserDateOfBirth: user.Attributes.find(attr => attr.Name === 'birthdate')?.Value || '',
          UserStatus: user.UserStatus,
          UserCreateDate: user.UserCreateDate,
          enabled: user.Enabled,
        }));

        // Update pagination token and state
        this.paginationToken = parsedResult.NextToken || null;
        this.hasMoreUsers = !!this.paginationToken;
        console.log('Updated accounts:', this.accounts);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },
    
    // New method to perform global search across all pages
    async performGlobalSearch() {
      if (!this.searchQuery.trim()) {
        // If search query is empty, switch back to normal mode
        this.isSearchMode = false;
        this.allSearchResults = [];
        this.currentPage = 1;
        return;
      }
      
      this.isSearching = true;
      this.allSearchResults = [];
      let allUsers = [];
      let token = null;
      let hasMorePages = true;
      
      try {
        // Fetch all pages of users
        while (hasMorePages) {
          const result = await getListOfUsersFromGroups(token, this.selectedGroup);
          const parsedResult = JSON.parse(result.data) || [];
          
          const users = parsedResult.Users.map(user => ({
            email: user.Attributes.find(attr => attr.Name === 'email')?.Value || '',
            given_name: user.Attributes.find(attr => attr.Name === 'given_name')?.Value || '',
            family_name: user.Attributes.find(attr => attr.Name === 'family_name')?.Value || '',
            sub: user.Attributes.find(attr => attr.Name === 'sub')?.Value || '',
            UserDateOfBirth: user.Attributes.find(attr => attr.Name === 'birthdate')?.Value || '',
            UserStatus: user.UserStatus,
            UserCreateDate: user.UserCreateDate,
            enabled: user.Enabled,
          }));
          
          allUsers = [...allUsers, ...users];
          
          // Check if there are more pages
          token = parsedResult.NextToken || null;
          hasMorePages = !!token;
        }
        
        // Apply search filter to all users
        const query = this.searchQuery.toLowerCase();
        this.allSearchResults = allUsers.filter(user => {
          return (
            (user.email && user.email.toLowerCase().includes(query)) ||
            (user.given_name && user.given_name.toLowerCase().includes(query)) ||
            (user.family_name && user.family_name.toLowerCase().includes(query))
          );
        });
        
        // Switch to search mode and reset to first page
        this.isSearchMode = true;
        this.currentPage = 1;
        
        console.log('Global search results:', this.allSearchResults);
      } catch (error) {
        console.error('Error performing global search:', error);
      } finally {
        this.isSearching = false;
      }
    },
    
    // Navigation methods for search pagination
    goToPage(page) {
      this.currentPage = page;
    },
    
    nextPage() {
      if (this.isSearchMode) {
        if (this.currentPage < this.totalPages) {
          this.currentPage++;
        }
      } else {
        if (this.hasMoreUsers) {
          if (this.paginationToken) {
            this.paginationHistory.push(this.paginationToken);
          }
          this.fetchUsers(this.selectedGroup, this.paginationToken);
        }
      }
    },
    
    previousPage() {
      if (this.isSearchMode) {
        if (this.currentPage > 1) {
          this.currentPage--;
        }
      } else {
        if (this.paginationHistory.length > 0) {
          const previousToken = this.paginationHistory.length > 1
            ? this.paginationHistory[this.paginationHistory.length - 2]
            : null;

          this.paginationHistory.pop();
          this.fetchUsers(this.selectedGroup, previousToken);
        } else {
          this.fetchUsers(this.selectedGroup);
        }
      }
    },
    
    // Reset search and go back to normal mode
    clearSearch() {
      this.searchQuery = '';
      this.isSearchMode = false;
      this.allSearchResults = [];
      this.currentPage = 1;
      this.fetchUsers(this.selectedGroup);
    },
    
    switchGroup(groupName) {
      this.selectedGroup = groupName;
      this.paginationToken = null;
      this.paginationHistory = [];
      
      // Reset search state when switching groups
      this.isSearchMode = false;
      this.allSearchResults = [];
      this.currentPage = 1;
      this.searchQuery = '';
      
      this.fetchUsers(groupName);
    },

    async disableUser() {
      try {
        const confirmation = confirm('Are you sure you want to disable this user?');
        if (!confirmation) return;

        await disableUserInGroup(this.editUser.email);
        console.log('User disabled successfully');
        this.editUser.enabled = false; // Update the enabled property locally
        
        // Update the user in search results if in search mode
        if (this.isSearchMode) {
          const index = this.allSearchResults.findIndex(user => user.email === this.editUser.email);
          if (index !== -1) {
            this.allSearchResults[index].enabled = false;
          }
        }
        
        this.fetchUsers(this.selectedGroup); // Refresh the user list
      } catch (error) {
        console.error('Error disabling user:', error);
      }
    },
    
    async enableUser() {
      try {
        const confirmation = confirm('Are you sure you want to enable this user?');
        if (!confirmation) return;

        await enableUserInGroup(this.editUser.email);
        console.log('User enabled successfully');
        this.editUser.enabled = true; // Update the enabled property locally
        
        // Update the user in search results if in search mode
        if (this.isSearchMode) {
          const index = this.allSearchResults.findIndex(user => user.email === this.editUser.email);
          if (index !== -1) {
            this.allSearchResults[index].enabled = true;
          }
        }
        
        this.fetchUsers(this.selectedGroup); // Refresh the user list
      } catch (error) {
        console.error('Error enabling user:', error);
      }
    },
    
    openEditModal(account) {
      this.editUser = { ...account }; // Clone the selected user
      console.log('Editing user:', this.editUser);
      this.showEditModal = true;
      document.body.classList.add('modal-open'); // Add class to body
    },
    
    closeEditModal() {
      this.showEditModal = false;
      this.editUser = {};
      document.body.classList.remove('modal-open'); // Remove class from body
    },
    
    async saveUserChanges() {
      try {
        await updateUserAttribute(
          this.editUser.email,
          this.editUser.given_name,
          this.editUser.family_name,
          this.editUser.UserDateOfBirth
        );
        console.log('User updated successfully');
        
        // Update the user in search results if in search mode
        if (this.isSearchMode) {
          const index = this.allSearchResults.findIndex(user => user.email === this.editUser.email);
          if (index !== -1) {
            this.allSearchResults[index] = {...this.editUser};
          }
        }
        
        this.closeEditModal();
        this.fetchUsers(this.selectedGroup); // Refresh the user list
      } catch (error) {
        console.error('Error updating user:', error);
      }
    },
    
    async deleteUser() {
      try {
        const confirmation = confirm('Are you sure you want to delete this user?');
        if (!confirmation) return;

        await deleteUserFromGroup(this.editUser.email);
        console.log('User deleted successfully');
        
        // Remove user from search results if in search mode
        if (this.isSearchMode) {
          this.allSearchResults = this.allSearchResults.filter(
            user => user.email !== this.editUser.email
          );
        }
        
        this.closeEditModal();
        this.fetchUsers(this.selectedGroup); // Refresh the user list
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    },
    
    async promoteToAdmin() {
      try {
        await removeUserFromGroup(this.editUser.email, 'AGENTS');
        await addUserToGroup(this.editUser.email, 'ADMINS');
        console.log('User promoted to Admin successfully');
        
        // If in search mode and viewing agents, remove this user from results
        if (this.isSearchMode && this.selectedGroup === 'AGENTS') {
          this.allSearchResults = this.allSearchResults.filter(
            user => user.email !== this.editUser.email
          );
        }
        
        this.closeEditModal();
        this.fetchUsers(this.selectedGroup); // Refresh the user list
      } catch (error) {
        console.error('Error promoting user to Admin:', error);
      }
    },
    
    async demoteToAgent() {
      try {
        await removeUserFromGroup(this.editUser.email, 'ADMINS');
        await addUserToGroup(this.editUser.email, 'AGENTS');
        console.log('User demoted to Agent successfully');
        
        // If in search mode and viewing admins, remove this user from results
        if (this.isSearchMode && this.selectedGroup === 'ADMINS') {
          this.allSearchResults = this.allSearchResults.filter(
            user => user.email !== this.editUser.email
          );
        }
        
        this.closeEditModal();
        this.fetchUsers(this.selectedGroup); // Refresh the user list
      } catch (error) {
        console.error('Error demoting user to Agent:', error);
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString();
    },
    
    closePopup() {
      this.showNoSelectionPopup = false;
    }
  },
  mounted() {
    this.fetchUsers(this.selectedGroup);
  },
};
</script>

<style scoped>
:root {
  --primary-color: #3b82f6;
  --primary-hover: #2563eb;
  --secondary-color: #e2e8f0;
  --danger-color: #ef4444;
  --danger-hover: #b91c1c;
  --success-color: #10b981;
  --success-hover: #059669;
  --warning-color: #f59e0b;
  --warning-hover: #d97706;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --background-color: #f1f5f9;
  --card-background: #ffffff;
  --border-color: #cbd5e1;
  --shadow-color: rgba(0, 0, 0, 0.1);
  --table-header-bg: #e2e8f0;
  --table-row-hover: #f8fafc;
  --table-row-alternate: #f1f5f9;
  --disabled-row-bg: #e2e8f0;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.admin-dashboard {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: var(--background-color);
  min-height: 100vh;
  padding: 2rem;
  color: var(--text-primary);
}

/* Header Styles */
.dashboard-header {
  margin-bottom: 2rem;
  background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.dashboard-header h1 {
  font-size: 1.8rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* Toggle Buttons */
.toggle-container {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.toggle-container button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  background-color: #e2e8f0;
  color: #475569;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: white;
  border-radius: 0.75rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(59, 130, 246, 0.2);
  border-radius: 50%;
  border-top-color: #3b82f6;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.toggle-container button:hover {
  background-color: #cbd5e1;
  transform: translateY(-1px);
}

.toggle-container button.active {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
  color: white;
  border-color: #2563eb;
  box-shadow: 0 4px 8px rgba(37, 99, 235, 0.25);
}

/* Card Styles */
.card {
  background-color: var(--card-background);
  border-radius: 0.75rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  border: 1px solid #cbd5e1;
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  background-color: #f8fafc;
  border-bottom: 1px solid var(--border-color);
}

.search-container {
  position: relative;
  width: 100%;
  max-width: 500px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-container svg {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
}

.search-container input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 2px solid #cbd5e1;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-primary);
  transition: all 0.2s ease;
  background-color: white;
  flex: 1;
}

.search-container input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.table-info {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* Table Styles */
.client-table {
  overflow-x: auto;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.client-table table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.client-table th {
  text-align: left;
  padding: 1rem;
  background-color: #f1f5f9;
  color: #334155;
  font-weight: 600;
  font-size: 0.875rem;
  border-bottom: 2px solid #cbd5e1;
  position: sticky;
  top: 0;
  z-index: 10;
}

.client-table td {
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
  color: #334155;
  font-size: 0.875rem;
  transition: background-color 0.2s ease;
}

.client-table tr:nth-child(even) {
  background-color: #f8fafc;
}

.client-table tr:hover {
  background-color: #dbeafe;
}

.client-table tr.disabled-row {
  background-color: #f1f5f9;
  color: #94a3b8;
}

/* Status Badges */
.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.status-badge.confirmed {
  background-color: #bbf7d0;
  color: #166534;
}

.status-badge.pending {
  background-color: #fef3c7;
  color: #92400e;
}

.status-badge.force_change_password {
  background-color: #e0f2fe;
  color: #0c4a6e;
}

.enabled-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.enabled-badge.enabled {
  background-color: #bbf7d0;
  color: #166534;
}

.enabled-badge.disabled {
  background-color: #fee2e2;
  color: #991b1b;
}

.no-results {
  text-align: center;
  color: #64748b;
  padding: 3rem !important;
  background-color: #f8fafc;
  font-style: italic;
}

/* Button Styles */
.btn-edit {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e2e8f0;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 0.375rem;
  color: #334155;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-edit:hover {
  background-color: #3b82f6;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(59, 130, 246, 0.3);
}

/* Pagination Styles */
.pagination {
  display: flex;
  justify-content: flex-end;
  padding: 1.25rem;
  border-top: 1px solid #e2e8f0;
  gap: 0.75rem;
  background-color: #f8fafc;
}

.pagination-pages {
  display: flex;
  gap: 0.5rem;
  margin-right: 0.5rem;
}

.page-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  height: 2.25rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.375rem;
  background-color: white;
  color: #334155;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-number.active {
  background-color: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.page-number:hover:not(.active) {
  background-color: #e2e8f0;
}

.btn-pagination {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.375rem;
  background-color: white;
  color: #334155;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-pagination:hover:not(:disabled) {
  background-color: #e2e8f0;
  border-color: #94a3b8;
}

.btn-pagination:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  backdrop-filter: blur(3px);
  overflow: hidden; /* Prevent scrolling of background */
}

body.modal-open {
  overflow: hidden; /* Add this class to body when modal is open */
}

.modal {
  background-color: white;
  border-radius: 0.75rem;
  width: 100%;
  max-width: 550px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  animation: modalFadeIn 0.3s ease forwards;
  max-height: 90vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  color: white;
  border-top-left-radius: 0.75rem;
  border-top-right-radius: 0.75rem;
  position: sticky;
  top: 0;
  z-index: 10;
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.btn-close {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 0.375rem;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-close:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: rotate(90deg);
}

.modal-content {
  padding: 1.5rem;
  background-color: white;
}

.user-email {
  padding: 0.75rem;
  margin-bottom: 1.5rem;
  background-color: #f1f5f9;
  border-radius: 0.5rem;
  font-weight: 500;
  border-left: 4px solid #3b82f6;
}

/* Form Styles */
.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #475569;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  color: #1e293b;
  transition: all 0.2s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.form-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.form-section h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #334155;
  margin-bottom: 1rem;
}

.status-toggle, .role-buttons {
  display: flex;
  gap: 1rem;
}

.btn-search {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 0.5rem;
  background-color: #3b82f6;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem 1rem;
}

.empty-state svg {
  color: #94a3b8;
  margin-bottom: 1rem;
}

.empty-state p {
  color: #64748b;
  font-size: 0.95rem;
  text-align: center;
}

.loading-container p {
  color: #475569;
  font-weight: 500;
}

.btn-search:hover {
  background-color: #2563eb;
  transform: translateY(-1px);
}

.btn-clear {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.375rem;
  background-color: white;
  color: #475569;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-clear:hover {
  background-color: #f1f5f9;
}

.btn-search svg {
  color: white;
}
/* Action Buttons */
.btn-disable, .btn-enable, .btn-promote, .btn-demote, .btn-delete, .btn-cancel, .btn-save, .btn-primary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-disable {
  background-color: #fee2e2;
  color: #b91c1c;
}

.btn-disable:hover {
  background-color: #fecaca;
}

.btn-enable {
  background-color: #dcfce7;
  color: #15803d;
}

.btn-enable:hover {
  background-color: #bbf7d0;
}

.btn-promote {
  background-color: #dbeafe;
  color: #1e40af;
}

.btn-promote:hover {
  background-color: #bfdbfe;
}

.btn-demote {
  background-color: #e2e8f0;
  color: #475569;
}

.btn-demote:hover {
  background-color: #cbd5e1;
}

.modal-footer {
  padding: 1.25rem;
  background-color: #f8fafc;
  border-top: 1px solid #e2e8f0;
  border-bottom-left-radius: 0.75rem;
  border-bottom-right-radius: 0.75rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
}

.btn-cancel {
  background-color: #e2e8f0;
  color: #475569;
}

.btn-cancel:hover {
  background-color: #cbd5e1;
}

.btn-save {
  background-color: #3b82f6;
  color: white;
}

.btn-save:hover {
  background-color: #2563eb;
}

.btn-delete {
  background-color: #fee2e2;
  color: #b91c1c;
}

.btn-delete:hover {
  background-color: #ef4444;
  color: white;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background-color: #2563eb;
}

.danger-zone {
  display: flex;
  align-items: center;
}

/* Popup Styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  backdrop-filter: blur(2px);
}

.popup {
  background-color: white;
  border-radius: 0.5rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  animation: modalFadeIn 0.3s ease forwards;
  overflow: hidden;
}

.popup-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem;
  background-color: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.popup-header svg {
  color: #3b82f6;
}

.popup-header h4 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #334155;
  margin: 0;
}

.popup p {
  padding: 1.5rem;
  color: #475569;
}

.popup-footer {
  padding: 1rem;
  background-color: #f8fafc;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .admin-dashboard {
    padding: 1rem;
  }
  
  .toggle-container {
    flex-direction: column;
  }
  
  .modal-footer {
    flex-direction: column-reverse;
    gap: 1rem;
  }
  
  .action-buttons, .danger-zone {
    width: 100%;
  }
  
  .action-buttons {
    justify-content: flex-end;
  }
  
  .btn-delete, .btn-save, .btn-cancel {
    flex: 1;
    justify-content: center;
  }
  
  .modal {
    width: 90%;
  }
}

/* Transitions */
button, a {
  transition: all 0.2s ease;
}

input, select, textarea {
  transition: border 0.2s ease, box-shadow 0.2s ease;
}

.btn-save:active, .btn-primary:active {
  transform: scale(0.98);
}

</style>