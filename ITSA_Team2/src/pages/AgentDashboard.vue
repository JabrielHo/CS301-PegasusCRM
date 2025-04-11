<template>
  <div class="agent-dashboard">
    <div class="header-actions">
      <h1>Agent Transaction Dashboard</h1>
      <div class="action-buttons">
        <button class="filter-btn" @click="toggleFilterPanel">
          <span class="filter-icon">⚡</span> Filters
        </button>
        <button class="refresh-btn" @click="refreshTransactions" :disabled="isLoading">
          <span class="refresh-icon" :class="{ 'spinning': isLoading }">↻</span> 
          {{ isLoading ? 'Loading...' : 'Refresh' }}
        </button>
      </div>
    </div>
    
    <!-- Filter panel -->
    <div class="filter-panel" v-if="showFilters">
      <div class="filter-row">
        <div class="filter-group">
          <label for="date-range">Date Range:</label>
          <select id="date-range" v-model="filters.dateRange">
            <option value="today">Today</option>
            <option value="yesterday">Yesterday</option>
            <option value="last7days">Last 7 Days</option>
            <option value="last30days">Last 30 Days</option>
            <option value="custom">Custom Range</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="status-type">Status:</label>
          <select id="status-type" v-model="filters.statusType">
            <option value="all">All Statuses</option>
            <option value="completed">Completed</option>
            <option value="pending">Pending</option>
            <option value="failed">Failed</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="client-search">Search Client:</label>
          <input 
            type="text" 
            id="client-search" 
            v-model="filters.clientSearch" 
            placeholder="Search by client name"
          >
        </div>
        
        <button class="apply-filters-btn" @click="applyFilters">Apply Filters</button>
      </div>
    </div>
    
    <!-- Stats summary boxes -->
    <div class="stats-summary">
      <div class="stat-box">
        <div class="stat-value">{{ stats.totalTransactions }}</div>
        <div class="stat-label">Total Transactions</div>
      </div>
      <div class="stat-box">
        <div class="stat-value">{{ stats.completedTransactions }}</div>
        <div class="stat-label">Completed</div>
      </div>
      <div class="stat-box">
        <div class="stat-value">{{ stats.pendingTransactions }}</div>
        <div class="stat-label">Pending</div>
      </div>
      <div class="stat-box">
        <div class="stat-value">{{ stats.todayTransactions }}</div>
        <div class="stat-label">Today's Clients</div>
      </div>
    </div>
    
    <!-- Main table -->
    <div id="table-container">
      <div class="status-bar" v-if="isLoading">
        <div class="loading-indicator">Loading transaction data...</div>
      </div>
      
      <div class="transaction-table" v-else>
        <table>
          <thead>
            <tr>
              <th @click="sortBy('id')">
                Transaction ID
                <span class="sort-indicator" v-if="sortColumn === 'id'">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('clientName')">
                Client Name
                <span class="sort-indicator" v-if="sortColumn === 'clientName'">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('date')">
                Date
                <span class="sort-indicator" v-if="sortColumn === 'date'">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('amount')">
                Amount
                <span class="sort-indicator" v-if="sortColumn === 'amount'">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('status')">
                Status
                <span class="sort-indicator" v-if="sortColumn === 'status'">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="paginatedTransactions.length === 0">
              <td colspan="6" class="no-data">No transactions found</td>
            </tr>
            <tr v-for="transaction in paginatedTransactions" :key="transaction.id" class="transaction-row">
              <td>{{ transaction.id }}</td>
              <td>
                <div class="client-name">
                  <span class="client-avatar">{{ getInitials(transaction.clientName) }}</span>
                  {{ transaction.clientName }}
                </div>
              </td>
              <td>{{ formatDate(transaction.date) }}</td>
              <td>${{ transaction.amount.toFixed(2) }}</td>
              <td>
                <span class="status-badge" :class="statusClass(transaction.status)">
                  {{ transaction.status }}
                </span>
              </td>
              <td>
                <div class="action-icons">
                  <button class="icon-btn view-btn" title="View Details" @click="viewDetails(transaction.id)">👁️</button>
                  <button class="icon-btn edit-btn" title="Edit Transaction" @click="editTransaction(transaction.id)">✏️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
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
      <div class="page-numbers">
        <button 
          v-for="page in displayedPageNumbers" 
          :key="page" 
          class="page-number" 
          :class="{ active: currentPage === page }"
          @click="currentPage = page"
        >
          {{ page }}
        </button>
      </div>
      <button 
        class="pagination-btn" 
        :disabled="currentPage === totalPages" 
        @click="currentPage++"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      agentName: 'John Whitaker',
      isLoading: false,
      showFilters: false,
      filters: {
        dateRange: 'last7days',
        statusType: 'all',
        clientSearch: ''
      },
      stats: {
        totalTransactions: 0,
        completedTransactions: 0,
        pendingTransactions: 0,
        todayTransactions: 0
      },
      transactions: [],
      currentPage: 1,
      itemsPerPage: 10,
      sortColumn: 'date',
      sortDirection: 'desc',
      searchQuery: ''
    };
  },
  computed: {
    filteredTransactions() {
      return this.transactions.filter(transaction => {
        // Apply search filter
        if (this.filters.clientSearch && 
            !transaction.clientName.toLowerCase().includes(this.filters.clientSearch.toLowerCase())) {
          return false;
        }
        
        // Apply status filter
        if (this.filters.statusType !== 'all' && transaction.status !== this.filters.statusType) {
          return false;
        }
        
        // Date filtering would be applied here in a real implementation
        return true;
      }).sort((a, b) => {
        // Apply sorting
        const modifier = this.sortDirection === 'asc' ? 1 : -1;
        
        // Handle different data types
        if (this.sortColumn === 'amount') {
          return (a[this.sortColumn] - b[this.sortColumn]) * modifier;
        } else {
          if (a[this.sortColumn] < b[this.sortColumn]) return -1 * modifier;
          if (a[this.sortColumn] > b[this.sortColumn]) return 1 * modifier;
          return 0;
        }
      });
    },
    paginatedTransactions() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredTransactions.slice(start, end);
    },
    totalPages() {
      return Math.max(1, Math.ceil(this.filteredTransactions.length / this.itemsPerPage));
    },
    displayedPageNumbers() {
      const pages = [];
      const maxPageButtons = 5;
      
      if (this.totalPages <= maxPageButtons) {
        // Show all pages if there are only a few
        for (let i = 1; i <= this.totalPages; i++) {
          pages.push(i);
        }
      } else {
        // Always include first page
        pages.push(1);
        
        // Calculate range around current page
        let startPage = Math.max(2, this.currentPage - 1);
        let endPage = Math.min(this.totalPages - 1, this.currentPage + 1);
        
        // Adjust if we're near the beginning
        if (this.currentPage <= 3) {
          endPage = Math.min(maxPageButtons - 1, this.totalPages - 1);
        }
        
        // Adjust if we're near the end
        if (this.currentPage >= this.totalPages - 2) {
          startPage = Math.max(2, this.totalPages - maxPageButtons + 2);
        }
        
        // Add ellipsis if needed
        if (startPage > 2) {
          pages.push('...');
        }
        
        // Add middle pages
        for (let i = startPage; i <= endPage; i++) {
          pages.push(i);
        }
        
        // Add ellipsis if needed
        if (endPage < this.totalPages - 1) {
          pages.push('...');
        }
        
        // Always include last page
        pages.push(this.totalPages);
      }
      
      return pages;
    }
  },
  created() {
    // Load initial data
    this.fetchTransactions();
    this.calculateStats();
  },
  methods: {
    fetchTransactions() {
      this.isLoading = true;
      
      // In a real application, this would be an API call
      // For demonstration, we'll create mock data
      setTimeout(() => {
        const mockStatuses = ['completed', 'pending', 'failed'];
        const mockClients = [
          'John Smith', 'Mary Johnson', 'Robert Williams', 'Patricia Brown',
          'Michael Jones', 'Linda Garcia', 'James Miller', 'Jennifer Davis'
        ];
        
        this.transactions = Array(50).fill().map((_, index) => {
          const randomDate = new Date();
          randomDate.setDate(randomDate.getDate() - Math.floor(Math.random() * 30));
          
          return {
            id: `TX-${10000 + index}`,
            clientName: mockClients[Math.floor(Math.random() * mockClients.length)],
            date: randomDate.toISOString(),
            amount: Math.floor(Math.random() * 10000) / 100,
            status: mockStatuses[Math.floor(Math.random() * mockStatuses.length)]
          };
        });
        
        this.isLoading = false;
        this.calculateStats();
      }, 800);
    },
    
    calculateStats() {
      const today = new Date().toDateString();
      
      this.stats = {
        totalTransactions: this.transactions.length,
        completedTransactions: this.transactions.filter(t => t.status === 'completed').length,
        pendingTransactions: this.transactions.filter(t => t.status === 'pending').length,
        todayTransactions: this.transactions.filter(t => new Date(t.date).toDateString() === today).length
      };
    },
    
    refreshTransactions() {
      this.fetchTransactions();
    },
    
    toggleFilterPanel() {
      this.showFilters = !this.showFilters;
    },
    
    applyFilters() {
      this.currentPage = 1; // Reset to first page when applying filters
      // In a real application, you might want to fetch filtered data from the server
    },
    
    sortBy(column) {
      if (this.sortColumn === column) {
        // Toggle direction if clicking the same column
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        // Default to ascending order for new column
        this.sortColumn = column;
        this.sortDirection = 'asc';
      }
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    
    getInitials(name) {
      return name
        .split(' ')
        .map(part => part.charAt(0))
        .join('')
        .toUpperCase();
    },
    
    statusClass(status) {
      const classes = {
        'completed': 'status-completed',
        'pending': 'status-pending',
        'failed': 'status-failed'
      };
      return classes[status] || 'status-default';
    },
    
    viewDetails(transactionId) {
      // In a real application, this would open a modal or navigate to details page
      console.log(`Viewing details for transaction ID: ${transactionId}`);
      alert(`View details for transaction ID: ${transactionId}`);
    },
    
    editTransaction(transactionId) {
      // In a real application, this would open an edit form
      console.log(`Editing transaction ID: ${transactionId}`);
      alert(`Edit transaction ID: ${transactionId}`);
    }
  }
};
</script>

<style scoped>
.agent-dashboard {
  padding: 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h1 {
  font-size: 1.8rem;
  font-weight: 600;
  margin: 0;
  color: #2d3748;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.refresh-btn, .filter-btn {
  padding: 8px 15px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.refresh-btn {
  background-color: #4CAF50;
  color: white;
}

.refresh-btn:hover {
  background-color: #45a049;
}

.filter-btn {
  background-color: #3182ce;
  color: white;
}

.filter-btn:hover {
  background-color: #2b6cb0;
}

.refresh-icon, .filter-icon {
  display: inline-block;
  font-size: 14px;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Filter panel styles */
.filter-panel {
  background-color: #fff;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  min-width: 180px;
}

.filter-group label {
  font-size: 0.85rem;
  margin-bottom: 5px;
  color: #4a5568;
}

.filter-group select, .filter-group input {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 0.9rem;
}

.apply-filters-btn {
  background-color: #3182ce;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  cursor: pointer;
  font-weight: 500;
}

/* Stats summary styles */
.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.stat-box {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: transform 0.2s ease;
}

.stat-box:hover {
  transform: translateY(-3px);
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #3182ce;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 0.9rem;
  color: #4a5568;
}

/* Table styles */
#table-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  overflow: hidden;
  flex-grow: 1;
}

.status-bar {
  padding: 20px;
  text-align: center;
  color: #4a5568;
}

.transaction-table {
  overflow-x: auto;
}

.transaction-table table {
  width: 100%;
  border-collapse: collapse;
}

.transaction-table th {
  background-color: #f7fafc;
  padding: 12px 15px;
  text-align: left;
  font-weight: 600;
  color: #4a5568;
  border-bottom: 1px solid #e2e8f0;
  cursor: pointer;
  position: relative;
}

.transaction-table th:hover {
  background-color: #edf2f7;
}

.sort-indicator {
  position: absolute;
  right: 10px;
}

.transaction-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #e2e8f0;
  color: #2d3748;
}

.transaction-row:hover {
  background-color: #f7fafc;
}

.no-data {
  text-align: center;
  padding: 30px;
  color: #a0aec0;
}

.client-name {
  display: flex;
  align-items: center;
  gap: 10px;
}

.client-avatar {
  background-color: #4299e1;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-completed {
  background-color: #e6fffa;
  color: #2c7a7b;
}

.status-pending {
  background-color: #faf5ff;
  color: #6b46c1;
}

.status-failed {
  background-color: #fff5f5;
  color: #c53030;
}

.status-default {
  background-color: #f7fafc;
  color: #4a5568;
}

.action-icons {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.icon-btn:hover {
  background-color: #edf2f7;
}

/* Pagination styles */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 10px;
}

.pagination-btn {
  padding: 8px 15px;
  background-color: #3182ce;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #2b6cb0;
}

.pagination-btn:disabled {
  background-color: #cbd5e0;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 5px;
}

.page-number {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background-color: #edf2f7;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
}

.page-number.active {
  background-color: #3182ce;
  color: white;
}

.page-number:hover:not(.active) {
  background-color: #e2e8f0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .filter-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-group {
    min-width: 100%;
  }
  
  .stats-summary {
    grid-template-columns: 1fr 1fr;
  }
  
  .header-actions {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  h1 {
    margin-bottom: 10px;
  }
}
</style>