<template>
  <div class="transaction-table">
    <div class="header-actions">
      <h1>Agent Activities</h1>
      <button class="refresh-btn" @click="refreshActivities">
        <span class="refresh-icon">↻</span> Refresh
      </button>
    </div>
    
    <table>
      <thead>
        <tr>
          <th>Select</th>
          <th>Transaction ID</th>
          <th>Amount</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="transaction in paginatedTransactions" :key="transaction.id">
          <td>
            <input
              type="checkbox"
              :value="transaction.id"
              v-model="selectedAccounts"
            />
          </td>
          <td>{{ transaction.id }}</td>
          <td>{{ transaction.amount }}</td>
          <td>{{ transaction.status }}</td>
        </tr>
      </tbody>
    </table>
    
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
      transactions: [
        { id: '1234', amount: '500', status: 'Confirmed' },
        { id: '1235', amount: '400', status: 'Pending' },
        { id: '1236', amount: '300', status: 'Failed' },
      ],
      selectedAccounts: [],
      currentPage: 1,
      itemsPerPage: 50,
      isLoading: false
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.transactions.length / this.itemsPerPage);
    },
    paginatedTransactions() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.transactions.slice(start, end);
    }
  },
  methods: {
    goBack() {
      this.$router.push({ name: 'agent-dashboard' });
    },
    refreshActivities() {
      this.isLoading = true;
      
      // Simulating an API call with setTimeout
      setTimeout(() => {
        // In a real application, you would fetch data from an API
        const newTransaction = {
          id: Math.floor(1000 + Math.random() * 9000).toString(),
          amount: Math.floor(100 + Math.random() * 900).toString(),
          status: ['Confirmed', 'Pending', 'Failed'][Math.floor(Math.random() * 3)]
        };
        
        this.transactions.unshift(newTransaction);
        this.isLoading = false;
      }, 500);
    }
  }
};
</script>

<style scoped>
.transaction-table {
  padding: 20px;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h1 {
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
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
  padding: 10px 15px;
  background-color: #00f;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}

button:hover {
  background-color: #0056b3;
}
</style>