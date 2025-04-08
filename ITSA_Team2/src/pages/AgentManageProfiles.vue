<template>
  <div class="admin-dashboard">
    <!-- Search and Account Table -->
    <div class="search-container">
      <label for="search">Search:</label>
      <input
        id="search"
        v-model="searchQuery"
        type="text"
        placeholder="Search by Client Name or ID"
      />
    </div>

    <div class="client-table">
      <table>
        <thead>
          <tr>
            <th>Select</th>
            <th>Account ID</th>
            <th>Client Name</th>
            <th>Date Created</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="account in paginatedAccounts" :key="account.id">
            <td>
              <input
                type="checkbox"
                :value="account.id"
                v-model="selectedAccounts"
              />
            </td>
            <td>{{ account.id }}</td>
            <td>{{ account.clientName }}</td>
            <td>{{ account.dateCreated }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination controls -->
    <div class="pagination">
      <button 
        class="pagination-btn" 
        :disabled="currentPage === 1" 
        @click="currentPage--"
      >
        Previous
      </button>
      <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
      <button 
        class="pagination-btn" 
        :disabled="currentPage === totalPages" 
        @click="currentPage++"
      >
        Next
      </button>
    </div>

    <!-- Buttons for Edit and Delete -->
    <div class="button-container">
      <button class="btn" @click="editSelectedAccounts">Edit</button>
      <button class="btn" @click="deleteSelectedAccounts">Delete</button>
    </div>

    <!-- No selection popup -->
    <div v-if="showNoSelectionPopup" class="popup">
      <p>No account is selected. Please select an account.</p>
      <button @click="closePopup">Close</button>
    </div>

    <!-- Deletion confirmation popup -->
    <div v-if="showDeleteConfirmationPopup" class="popup">
      <p>Are you sure you want to delete the following account(s)?</p>
      <ul>
        <li v-for="account in selectedAccountsList" :key="account.id">{{ account.clientName }} (ID: {{ account.id }})</li>
      </ul>
      <button @click="deleteAccounts">Yes</button>
      <button @click="closePopup">No</button>
    </div>

    <!-- Deleted accounts confirmation -->
    <div v-if="showDeletedPopup" class="popup">
      <p>These accounts have been deleted:</p>
      <ul>
        <li v-for="account in deletedAccounts" :key="account.id">{{ account.clientName }} (ID: {{ account.id }})</li>
      </ul>
      <button @click="closePopup">Close</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      accounts: [
        { id: '1234', clientName: 'John Haaland', dateCreated: '20/03/2021' },
        { id: '1235', clientName: 'John Wick', dateCreated: '21/03/2021' },
        { id: '1236', clientName: 'Jane Smith', dateCreated: '22/03/2021' },
        { id: '1237', clientName: 'Alan Turing', dateCreated: '23/03/2021' },
      ],
      selectedAccounts: [], // Array to store selected account IDs
      deletedAccounts: [], // Array to store deleted accounts for confirmation message
      showNoSelectionPopup: false, // Flag to show no selection popup
      showDeleteConfirmationPopup: false, // Flag to show delete confirmation popup
      showDeletedPopup: false, // Flag to show deleted accounts confirmation popup
      currentPage: 1,
      itemsPerPage: 50
    };
  },
  computed: {
    filteredAccounts() {
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
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredAccounts.slice(start, end);
    }
  },
  methods: {
    editSelectedAccounts() {
      if (this.selectedAccounts.length === 0) {
        this.showNoSelectionPopup = true;
        return;
      }
      // Navigate to edit page (example: using Vue Router)
      this.$router.push({ name: 'EditAccount', params: { ids: this.selectedAccounts } });
    },
    deleteSelectedAccounts() {
      if (this.selectedAccounts.length === 0) {
        this.showNoSelectionPopup = true;
        return;
      }
      this.showDeleteConfirmationPopup = true;
    },
    deleteAccounts() {
      // Delete selected accounts from the data (you can make an API call here)
      this.deletedAccounts = this.selectedAccountsList;
      this.accounts = this.accounts.filter(account => !this.selectedAccounts.includes(account.id));
      this.selectedAccounts = []; // Reset selected accounts
      this.showDeleteConfirmationPopup = false;
      this.showDeletedPopup = true;
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
.admin-dashboard {
  padding: 20px;
}

.button-container {
  display: flex;
  gap: 10px;
  margin: 20px 0;
}

.btn:hover {
  background-color: #0056b3;
}

.client-table table {
  width: 100%;
  border-collapse: collapse;
}

.client-table th, td {
  padding: 10px;
  border: 1px solid #ccc;
}

.search-container {
  margin: 20px 0;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 15px;
}

.pagination-btn {
  padding: 8px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.pagination-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
}

.popup {
  position: fixed;
  top: 20%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  padding: 20px;
  color: white;
  border-radius: 10px;
  z-index: 100;
}

.popup button {
  margin-top: 10px;
}
</style>