<template>
  <div class="admin-dashboard">
    <!-- Header with Title -->
    <div class="dashboard-header">
      <h1>Client Profile Management</h1>
      <p class="dashboard-subtitle">Manage client profile information</p>
    </div>

    <!-- Search and Account Table -->
    <div class="card">
      <div class="card-header">
        <div class="search-container">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <input id="search" v-model="searchQuery" type="text" placeholder="Search by Client Name or ID..." @keyup.enter="performGlobalSearch" />
          <button class="btn-search" @click="performGlobalSearch" title="Search">
            Search
          </button>
        </div>
        <div class="table-info">
          <span v-if="isSearchMode">
            {{ filteredAccounts.length }} of {{ allSearchResults.length }} accounts found
          </span>
          <span v-else>
            {{ filteredAccounts.length }} accounts found
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
              <th>Account ID</th>
              <th>Client Name</th>
              <th>Status</th>
              <th>Accounts</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="account in paginatedAccounts" 
              :key="account.id"
              @click="navigateToProfile(account.id)"
              class="account-row"
            >
              <td>{{ account.id }}</td>
              <td>{{ account.clientName }}</td>
              <td>
                <span :class="[
                  'status-badge', 
                  account.active ? 'confirmed' : 'pending'
                ]">
                  {{ account.active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td>
                <!-- Placeholder for number of bank accounts -->
                {{ account.bankAccounts ? account.bankAccounts.length : 0 }}
              </td>
            </tr>
            <tr v-if="paginatedAccounts.length === 0">
              <td colspan="5" class="no-results">
                <div class="empty-state">
                  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                  <p>No accounts found matching your search criteria</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination controls -->
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
        <button 
          class="btn-pagination" 
          :disabled="isPreviousDisabled" 
          @click="previousPage"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
        </button>
        <span class="page-info" v-if="!isSearchMode">Page {{ currentPage }} of {{ totalPages }}</span>
        <button 
          class="btn-pagination" 
          :disabled="isNextDisabled" 
          @click="nextPage"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal">
        <div class="modal-header">
          <h3>Edit Client Account</h3>
          <button class="btn-close" @click="closeEditModal">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>
        
        <div class="modal-content">
          <div class="account-id">
            <svg class="account-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
            <span>Account ID: {{ editAccount.id }}</span>
          </div>
          
          <div class="form-group">
            <label for="clientName">Client Name</label>
            <input id="clientName" v-model="editAccount.clientName" type="text" />
          </div>

          <div class="form-group">
            <label for="dateCreated">Date Created</label>
            <input id="dateCreated" v-model="editAccount.dateCreated" type="date" disabled />
          </div>

          <div class="form-section">
            <h4>Account Status</h4>
            <div class="status-toggle">
              <button @click="toggleAccountStatus" :class="editAccount.active ? 'btn-disable' : 'btn-enable'">
                <svg v-if="editAccount.active" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18.36 6.64a9 9 0 1 1-12.73 0"></path><line x1="12" y1="2" x2="12" y2="12"></line></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"></path><path d="M12 5v14"></path></svg>
                {{ editAccount.active ? 'Deactivate Account' : 'Activate Account' }}
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
            <button class="btn-save" @click="saveAccountChanges">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>
              Save Changes
            </button>
          </div>
          
          <div class="danger-zone">
            <button class="btn-delete" @click="deleteAccount">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
              Delete Account
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isSearching" class="modal-overlay">
      <div class="loading-container">
        <div class="loading-spinner"></div>
        <p>Searching all accounts...</p>
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

    <!-- Deletion confirmation popup -->
    <div v-if="showDeleteConfirmationPopup" class="popup-overlay" @click.self="closePopup">
      <div class="popup">
        <div class="popup-header">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
          <h4>Confirm Deletion</h4>
        </div>
        <div class="popup-content">
          <p>Are you sure you want to delete the following account(s)?</p>
          <ul class="delete-list">
            <li v-for="account in selectedAccountsList" :key="account.id">{{ account.clientName }} (ID: {{ account.id }})</li>
          </ul>
          <p class="warning-text">This action cannot be undone.</p>
        </div>
        <div class="popup-footer">
          <button class="btn-cancel" @click="closePopup">Cancel</button>
          <button class="btn-delete" @click="deleteAccounts">Delete</button>
        </div>
      </div>
    </div>

    <!-- Deleted accounts confirmation -->
    <div v-if="showDeletedPopup" class="popup-overlay" @click.self="closePopup">
      <div class="popup">
        <div class="popup-header">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="8 12 12 16 16 12"></polyline><line x1="12" y1="8" x2="12" y2="16"></line></svg>
          <h4>Deletion Successful</h4>
        </div>
        <div class="popup-content">
          <p>The following accounts have been deleted:</p>
          <ul class="delete-list">
            <li v-for="account in deletedAccounts" :key="account.id">{{ account.clientName }} (ID: {{ account.id }})</li>
          </ul>
        </div>
        <div class="popup-footer">
          <button class="btn-primary" @click="closePopup">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      accounts: [
        { 
          id: '1234', 
          clientName: 'John Haaland', 
          dateCreated: '2021-03-20', 
          active: true,
          bankAccounts: [
            { id: 'BA001', type: 'Checking', balance: 5420.75 },
            { id: 'BA002', type: 'Savings', balance: 12500.00 }
          ]
        },
        { 
          id: '1235', 
          clientName: 'John Wick', 
          dateCreated: '2021-03-21', 
          active: true,
          bankAccounts: [
            { id: 'BA003', type: 'Checking', balance: 2340.50 }
          ]
        },
        { 
          id: '1236', 
          clientName: 'Jane Smith', 
          dateCreated: '2021-03-22', 
          active: false,
          bankAccounts: [
            { id: 'BA004', type: 'Savings', balance: 8750.25 },
            { id: 'BA005', type: 'Investment', balance: 45000.00 },
            { id: 'BA006', type: 'Checking', balance: 1250.75 }
          ]
        },
        { 
          id: '1237', 
          clientName: 'Alan Turing', 
          dateCreated: '2021-03-23', 
          active: true,
          bankAccounts: [
            { id: 'BA007', type: 'Checking', balance: 3700.00 }
          ]
        },
        { 
          id: '1238', 
          clientName: 'Ada Lovelace', 
          dateCreated: '2021-03-24', 
          active: true,
          bankAccounts: [
            { id: 'BA008', type: 'Savings', balance: 15800.50 },
            { id: 'BA009', type: 'Investment', balance: 75000.00 }
          ]
        },
        { 
          id: '1239', 
          clientName: 'Grace Hopper', 
          dateCreated: '2021-03-25', 
          active: false,
          bankAccounts: []
        },
        { 
          id: '1240', 
          clientName: 'Dennis Ritchie', 
          dateCreated: '2021-03-26', 
          active: true,
          bankAccounts: [
            { id: 'BA010', type: 'Checking', balance: 4250.75 }
          ]
        },
        { 
          id: '1241', 
          clientName: 'Linus Torvalds', 
          dateCreated: '2021-03-27', 
          active: true,
          bankAccounts: [
            { id: 'BA011', type: 'Checking', balance: 8300.25 },
            { id: 'BA012', type: 'Savings', balance: 27500.00 }
          ]
        },
      ],
      selectedAccounts: [], // Array to store selected account IDs
      deletedAccounts: [], // Array to store deleted accounts for confirmation message
      showNoSelectionPopup: false, // Flag to show no selection popup
      showDeleteConfirmationPopup: false, // Flag to show delete confirmation popup
      showDeletedPopup: false, // Flag to show deleted accounts confirmation popup
      showEditModal: false,
      editAccount: {},
      currentPage: 1,
      itemsPerPage: 5,
      
      // Search mode properties
      isSearching: false,
      isSearchMode: false,
      allSearchResults: [],
    };
  },
  computed: {
    filteredAccounts() {
      if (this.isSearchMode) {
        return this.allSearchResults;
      }
      
      const query = this.searchQuery.toLowerCase();
      return this.accounts.filter(account => {
        return (
          (account.clientName && account.clientName.toLowerCase().includes(query)) ||
          (account.id && account.id.includes(query))
        );
      });
    },
    selectedAccountsList() {
      return this.accounts.filter(account => this.selectedAccounts.includes(account.id));
    },
    totalPages() {
      return Math.ceil(this.filteredAccounts.length / this.itemsPerPage);
    },
    paginatedAccounts() {
      if (this.isSearchMode) {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        return this.allSearchResults.slice(start, end);
      } else {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        return this.filteredAccounts.slice(start, end);
      }
    },
    // Check if Previous button should be disabled
    isPreviousDisabled() {
      return this.currentPage <= 1;
    },
    
    // Check if Next button should be disabled
    isNextDisabled() {
      return this.currentPage >= this.totalPages;
    }
  },
  methods: {
    // Navigate to profile detail page
    navigateToProfile(accountId) {
      if (!accountId){ 
        console.error('Account Id missing')
        return;
      }
      // Use router to navigate
      if (this.$router) {
        this.$router.push({ name: 'Client Profile Page', params: { id: accountId } });
      } else {
        // Fallback if router is not defined (for demo purposes)
        console.log(`Navigating to client profile with ID: ${accountId}`);
        alert(`Navigating to client profile for ID: ${accountId}`);
      }
    },
    
    openEditModal(account) {
      this.editAccount = { ...account }; // Clone the selected account
      console.log('Editing account:', this.editAccount);
      this.showEditModal = true;
      document.body.classList.add('modal-open'); // Add class to body
    },
    
    closeEditModal() {
      this.showEditModal = false;
      this.editAccount = {};
      document.body.classList.remove('modal-open'); // Remove class from body
    },
    
    toggleAccountStatus() {
      this.editAccount.active = !this.editAccount.active;
    },
    
    saveAccountChanges() {
      // Find the account in the array and update it
      const index = this.accounts.findIndex(account => account.id === this.editAccount.id);
      if (index !== -1) {
        this.accounts[index] = { ...this.editAccount };
      }
      
      // If in search mode, update the search results as well
      if (this.isSearchMode) {
        const searchIndex = this.allSearchResults.findIndex(account => account.id === this.editAccount.id);
        if (searchIndex !== -1) {
          this.allSearchResults[searchIndex] = { ...this.editAccount };
        }
      }
      
      this.closeEditModal();
    },
    
    deleteAccount() {
      // Set up for deletion confirmation
      this.selectedAccounts = [this.editAccount.id];
      this.closeEditModal();
      this.showDeleteConfirmationPopup = true;
    },
    
    editSelectedAccounts() {
      if (this.selectedAccounts.length === 0) {
        this.showNoSelectionPopup = true;
        return;
      }
      
      if (this.selectedAccounts.length === 1) {
        // Find the account and open the edit modal
        const accountToEdit = this.accounts.find(account => account.id === this.selectedAccounts[0]);
        if (accountToEdit) {
          this.openEditModal(accountToEdit);
        }
      } else {
        // Navigate to edit page for multiple accounts (example: using Vue Router)
        // This would be implemented in a real application
        console.log('Editing multiple accounts:', this.selectedAccounts);
        this.$router?.push({ name: 'EditAccount', params: { ids: this.selectedAccounts } });
      }
    },
    
    deleteSelectedAccounts() {
      if (this.selectedAccounts.length === 0) {
        this.showNoSelectionPopup = true;
        return;
      }
      this.showDeleteConfirmationPopup = true;
    },
    
    deleteAccounts() {
      // Store deleted accounts for confirmation message
      this.deletedAccounts = this.selectedAccountsList;
      
      // Delete selected accounts from the data
      this.accounts = this.accounts.filter(account => !this.selectedAccounts.includes(account.id));
      
      // If in search mode, update search results
      if (this.isSearchMode) {
        this.allSearchResults = this.allSearchResults.filter(
          account => !this.selectedAccounts.includes(account.id)
        );
      }
      
      this.selectedAccounts = []; // Reset selected accounts
      this.showDeleteConfirmationPopup = false;
      this.showDeletedPopup = true;
    },
    
    // Global search across all accounts
    async performGlobalSearch() {
      if (!this.searchQuery.trim()) {
        // If search query is empty, switch back to normal mode
        this.clearSearch();
        return;
      }
      
      this.isSearching = true;
      
      try {
        // Simulate API search delay
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Apply search filter to all accounts
        const query = this.searchQuery.toLowerCase();
        this.allSearchResults = this.accounts.filter(account => {
          return (
            (account.clientName && account.clientName.toLowerCase().includes(query)) ||
            (account.id && account.id.includes(query))
          );
        });
        
        // Switch to search mode and reset to first page
        this.isSearchMode = true;
        this.currentPage = 1;
      } catch (error) {
        console.error('Error performing global search:', error);
      } finally {
        this.isSearching = false;
      }
    },
    
    // Clear search and go back to normal mode
    clearSearch() {
      this.searchQuery = '';
      this.isSearchMode = false;
      this.allSearchResults = [];
      this.currentPage = 1;
    },
    
    // Pagination methods
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    goToPage(page) {
      this.currentPage = page;
    },
    
    closePopup() {
      this.showNoSelectionPopup = false;
      this.showDeleteConfirmationPopup = false;
      this.showDeletedPopup = false;
    }
  }
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
  justify-content: center;
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