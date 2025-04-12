<template>
  <div class="admin-dashboard">
    <!-- Header with Title -->
    <div class="dashboard-header">
      <h1>Transactions</h1>
      <p class="dashboard-subtitle">View and manage transaction records</p>
    </div>

    <!-- Search and Transaction Table -->
    <div class="card">
      <div class="card-header">
        <div class="search-container">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input id="search" v-model="searchQuery" type="text" placeholder="Search by Transaction ID or Amount..."
            @keyup="searchTransactions" />
          <button class="btn-search" @click="searchTransactions" title="Search">
            Search
          </button>
        </div>
        <div class="table-info">
          <span v-if="isSearchMode">
            {{ paginatedTransactions.length }} of {{ filteredTransactions.length }} transactions found
          </span>
          <span v-else>
            {{ transactions.length }} transactions found
          </span>
          <button class="btn-clear" @click="clearSearch" v-if="isSearchMode">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="15" y1="9" x2="9" y2="15"></line>
              <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
            Clear Search
          </button>
          <button class="refresh-btn" @click="refreshTransactions(this.clientId)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M23 4v6h-6"></path>
              <path d="M1 20v-6h6"></path>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
            </svg>
            Refresh
          </button>
        </div>
      </div>

      <div class="client-table">
        <table>
          <thead>
            <tr>
              <th>Transaction ID</th>
              <th>Amount</th>
              <th>Type</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="transaction in paginatedTransactions" :key="transaction.id">
              <tr class="transaction-row" @click="toggleExpand(transaction.id)">
                <td>{{ transaction.id }}</td>
                <td>{{ transaction.amount }}</td>
                <td>{{ transaction.transaction_type === 'D' ? 'Deposit' : transaction.transaction_type === 'W' ?
                  'Withdraw' : 'Other' }}</td>
                <td>
                  <span :class="[
                    'status-badge',
                    transaction.status === 'Completed' ? 'confirmed' :
                      transaction.status === 'Pending' ? 'pending' : 'force_change_password'
                  ]">
                    {{ transaction.status }}
                  </span>
                </td>
              </tr>
              <tr v-if="expandedTransactions.includes(transaction.id)" class="expanded-details">
                <td colspan="5">
                  <div class="transaction-details">
                    <h3>Transaction Details</h3>
                    <div class="details-grid">
                      <div class="detail-item">
                        <span class="label">Transaction ID:</span>
                        <span>{{ transaction.id ?? 'undefined' }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="label">Amount:</span>
                        <span>{{ transaction.amount ?? 'undefined' }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="label">Client Account ID:</span>
                        <span>{{ transaction.client_account_id ?? 'undefined' }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="label">Client ID:</span>
                        <span>{{ transaction.client_id ?? 'undefined' }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="label">Status:</span>
                        <span>{{ transaction.status ?? 'undefined' }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="label">Transaction Date:</span>
                        <span>{{ transaction.transaction_date ?? transaction.date ?? 'undefined' }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="label">Transaction Type:</span>
                        <span>{{ transaction.transaction_type ?? 'undefined' }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="label">Description:</span>
                        <span>{{ transaction.description ?? 'No description available' }}</span>
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
            </template>
            <tr v-if="paginatedTransactions.length === 0">
              <td colspan="5" class="no-results">
                <div class="empty-state">
                  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                  </svg>
                  <p>No transactions found matching your search criteria</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination controls -->
      <div class="pagination">
        <button class="btn-pagination" :disabled="currentPage === 1" @click="previousPage">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
          Previous
        </button>

        <div class="pagination-pages">
          <button v-if="currentPage > 3 && currentPage - 3 != 1 && currentPage - 4 != 1" @click="goToPage(1)" class="page-number">1</button>
          <span v-if="currentPage > 4 && currentPage - 4 != 1" class="page-ellipsis">...</span>
          <button v-for="page in visiblePageNumbers" :key="page" @click="goToPage(page)"
            :class="['page-number', { active: currentPage === page }]">
            {{ page }}
          </button>
          <span v-if="currentPage < totalPages - 3 && currentPage + 4 != totalPages" class="page-ellipsis">...</span>
          <button v-if="currentPage < totalPages - 2 && totalPages > 1 && currentPage + 3 != totalPages && currentPage + 4 != totalPages" @click="goToPage(totalPages)"
            class="page-number">
            {{ totalPages }}
          </button>
        </div>

        <button class="btn-pagination" :disabled="currentPage === totalPages" @click="nextPage">
          Next
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isLoading" class="modal-overlay">
      <div class="loading-container">
        <div class="loading-spinner"></div>
        <p>Loading transactions...</p>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../services/axiosInstance"; // Adjust the import path as necessary

export default {
  props: ['clientId'],
  data() {
    return {
      searchQuery: '',
      transactions: [],
      expandedTransactions: [],

      //Pagination
      currentPage: 1,
      itemsPerPage: 5,

      isLoading: false,
      isSearchMode: false,
      selectAll: false,
      filteredTransactions: []
    };
  },
  computed: {
    visiblePageNumbers() {
      let start = Math.max(1, this.currentPage - 2);
      let end = Math.min(this.totalPages, this.currentPage + 2);

      // Adjust the range to always show 5 pages if possible
      if (end - start + 1 < 5) {
        if (start === 1) {
          end = Math.min(5, this.totalPages);
        } else if (end === this.totalPages) {
          start = Math.max(1, this.totalPages - 4);
        }
      }

      // Generate array of page numbers
      return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    },
    totalPages() {
      if (this.isSearchMode) {
        return Math.ceil(this.filteredTransactions.length / this.itemsPerPage);
      } else {
        return Math.ceil(this.transactions.length / this.itemsPerPage);
      }
    },
    paginatedTransactions() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      if (this.isSearchMode) {
        return this.filteredTransactions.slice(start, end);
      } else {
        return this.transactions.slice(start, end);
      }
    },
    // Check if Previous button should be disabled
    isPreviousDisabled() {
      return this.currentPage <= 1;
    },

    // Check if Next button should be disabled
    isNextDisabled() {
      return this.currentPage >= this.totalPages;
    },
  },
  methods: {
    goBack() {
      this.$router.push({ name: 'agent-dashboard' });
    },
    toggleExpand(transactionId) {
      if (this.expandedTransactions.includes(transactionId)) {
        this.expandedTransactions = this.expandedTransactions.filter(id => id !== transactionId);
      } else {
        this.expandedTransactions.push(transactionId);
      }
    },
    async refreshTransactions(client_id) {
      this.isLoading = true;
      try {
        // Reuse the loadTransactions method to fetch data
        this.clearSearch();
        await this.loadTransactions(client_id);
        this.currentPage = 1;
      } catch (error) {
        console.error('Error refreshing transactions:', error);
      } finally {
        this.isLoading = false;
      }
    },
    async loadTransactions(client_id) {
      this.isLoading = true;
      try {
        // axios get transactions
        const response = await axiosInstance.get(`https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/api/transactions/client/${client_id ?? "ce139e65-be8a-4506-8c5a-bf45fd58d41f"}`);
        // console.log(response);
        this.transactions = response.data;
      } catch (error) {
        console.error('Error fetching transactions:', error);
        // Keep the demo data in case of error
      } finally {
        this.isLoading = false;
      }
    },
    searchTransactions() {
      if (!this.searchQuery.trim()) {
        this.clearSearch();
        return;
      }

      this.isLoading = true;
      this.currentPage = 1;

      // Simulate search delay
      try {
        const query = this.searchQuery.toLowerCase();
        this.filteredTransactions = this.transactions.filter(transaction => {
          return (
            (transaction.id && String(transaction.id).toLowerCase().includes(query)) ||
            (transaction.amount && String(transaction.amount).toLowerCase().includes(query)) ||
            (transaction.status && transaction.status.toLowerCase().includes(query)) ||
            (transaction.transaction_type && transaction.transaction_type.toLowerCase().includes(query))
          );
        });
        this.isSearchMode = true;
        this.isLoading = false;

      } catch (error) {
        console.error("Error during search:", error);
      }
      finally {
        this.isLoading = false;
      }
        
    },
    clearSearch() {
      this.searchQuery = '';
      this.isSearchMode = false;
      this.filteredTransactions = [];
      this.currentPage = 1;
    },
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    goToPage(page) {
      this.currentPage = page;
    }
  },
  created() {
    // console.log(this.clientId);
    this.loadTransactions(this.clientId);
  },
  watch: {
    // Reset selectAll when page changes or search results change
    paginatedTransactions() {
      this.selectAll = false;
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

.dashboard-subtitle {
  margin-top: 0.5rem;
  font-size: 1rem;
  opacity: 0.9;
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
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* Button Styles */
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

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  background-color: #059669;
  transform: translateY(-1px);
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

.client-table tr:nth-child(even):not(.expanded-details) {
  background-color: #f8fafc;
}

.transaction-row {
  cursor: pointer;
}

.transaction-row:hover {
  background-color: #dbeafe;
}

.expanded-details {
  background-color: #f8fafc;
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
  background-color: #fee2e2;
  color: #991b1b;
}

/* Empty State */
.no-results {
  text-align: center;
  color: #64748b;
  padding: 3rem !important;
  background-color: #f8fafc;
  font-style: italic;
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

/* Transaction Details */
.transaction-details {
  padding: 1.5rem;
}

.transaction-details h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #334155;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.detail-item {
  display: flex;
}

.label {
  font-weight: 600;
  margin-right: 0.75rem;
  min-width: 140px;
  color: #475569;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
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

.page-info {
  font-size: 0.875rem;
  color: #475569;
}

/* Loading Overlay */
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

.loading-container p {
  color: #475569;
  font-weight: 500;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .admin-dashboard {
    padding: 1rem;
  }

  .details-grid {
    grid-template-columns: 1fr;
  }

  .card-header {
    flex-direction: column;
    gap: 1rem;
  }

  .table-info {
    width: 100%;
    justify-content: space-between;
  }

  .search-container {
    max-width: 100%;
  }
}
</style>