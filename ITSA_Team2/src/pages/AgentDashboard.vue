<template>
  <div class="agent-dashboard">
    <header>
      <h1>Scrooge Global Bank</h1>
      <p>Agent - {{ agentName }}</p>
    </header>

    <div class="search-actions">
      <div class="search-bar">
        <input type="text" v-model="searchQuery" placeholder="Search"/>
        <button @click="searchTransactions">Search</button>
      </div>
      
      <button class="refresh-btn" @click="refreshTransactions">
        <span class="refresh-icon">↻</span> Refresh
      </button>
    </div>

    <div class="transaction-table">
      <table>
        <thead>
          <tr>
            <th>Transaction ID</th>
            <th>Amount</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="transaction in paginatedTransactions" :key="transaction.id">
            <td>{{ transaction.id }}</td>
            <td>{{ transaction.amount }}</td>
            <td>{{ transaction.status }}</td>
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
  </div>
</template>

<script>
export default {
  data() {
    return {
      agentName: 'John Whitaker',
      transactions: [
        { id: '1234', amount: 'John Haaland', status: '20/03/2021' },
        { id: '1235', amount: 'Jane Smith', status: '21/03/2021' },
        { id: '1236', amount: 'Mike Johnson', status: '22/03/2021' }
      ],
      searchQuery: '',
      currentPage: 1,
      itemsPerPage: 50,
      isLoading: false
    };
  },
  computed: {
    filteredTransactions() {
      if (!this.searchQuery) return this.transactions;
      
      const query = this.searchQuery.toLowerCase();
      return this.transactions.filter(transaction => {
        return (
          transaction.id.toLowerCase().includes(query) ||
          transaction.amount.toLowerCase().includes(query) ||
          transaction.status.toLowerCase().includes(query)
        );
      });
    },
    totalPages() {
      return Math.ceil(this.filteredTransactions.length / this.itemsPerPage);
    },
    paginatedTransactions() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredTransactions.slice(start, end);
    }
  },
  methods: {
    searchTransactions() {
      console.log('Searching for:', this.searchQuery);
      // Reset to first page when searching
      this.currentPage = 1;
    },
    refreshTransactions() {
      this.isLoading = true;
      
      // Simulating an API call with setTimeout
      setTimeout(() => {
        // In a real application, you would fetch data from an API
        const newTransaction = {
          id: Math.floor(1000 + Math.random() * 9000).toString(),
          amount: 'New Client',
          status: new Date().toLocaleDateString('en-GB')
        };
        
        this.transactions.unshift(newTransaction);
        this.isLoading = false;
      }, 500);
    }
  }
};
</script>

<style scoped>
.agent-dashboard {
  padding: 20px;
  background-color: #f0f8ff;
}

header {
  margin-bottom: 20px;
}

h1 {
  font-size: 2rem;
  font-weight: bold;
}

.search-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  display: flex;
  align-items: center;
}

.search-bar input {
  padding: 8px;
  margin-right: 10px;
}

.search-bar button {
  padding: 8px 12px;
  background-color: #00f;
  color: white;
}

.refresh-btn {
  padding: 8px 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
}

.refresh-btn:hover {
  background-color: #45a049;
}

.refresh-icon {
  display: inline-block;
}

.transaction-table table {
  width: 100%;
  border-collapse: collapse;
}

.transaction-table th, td {
  padding: 10px;
  border: 1px solid #ccc;
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

button {
  border: none;
  cursor: pointer;
  border-radius: 4px;
}

button:hover {
  opacity: 0.9;
}
</style>