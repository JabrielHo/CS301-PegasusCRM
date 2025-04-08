<template>
  <div class="transaction-table">
    <div class="header-actions">
      <h1>Transactions</h1>
      <button class="refresh-btn" @click="refreshTransactions">
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
        <template v-for="(transaction, index) in paginatedTransactions" :key="transaction.id">
          <tr class="transaction-row" @click="toggleExpand(transaction.id)">
            <td @click.stop>
              <input
                type="checkbox"
                :value="transaction.id"
                v-model="selectedTransactions"
              />
            </td>
            <td>{{ transaction.id }}</td>
            <td>{{ transaction.amount }}</td>
            <td>{{ transaction.status }}</td>
          </tr>
          <tr v-if="expandedTransactions.includes(transaction.id)" class="expanded-details">
            <td colspan="4">
              <div class="transaction-details">
                <h3>Transaction Details</h3>
                <div class="details-grid">
                  <div class="detail-item">
                    <span class="label">Date:</span>
                    <span>{{ transaction.date || '05/04/2025' }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="label">Customer:</span>
                    <span>{{ transaction.customer || 'John Doe' }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="label">Payment Method:</span>
                    <span>{{ transaction.paymentMethod || 'Credit Card' }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="label">Reference:</span>
                    <span>{{ transaction.reference || 'REF-' + transaction.id }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="label">Description:</span>
                    <span>{{ transaction.description || 'Standard transaction' }}</span>
                  </div>
                </div>
              </div>
            </td>
          </tr>
        </template>
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
        { 
          id: '1234', 
          amount: '$500', 
          status: 'Confirmed',
          date: '04/04/2025',
          customer: 'John Smith',
          paymentMethod: 'Credit Card',
          reference: 'REF-1234',
          description: 'Monthly subscription'
        },
        { 
          id: '1235', 
          amount: '$400', 
          status: 'Pending',
          date: '03/04/2025',
          customer: 'Alice Johnson',
          paymentMethod: 'Bank Transfer',
          reference: 'REF-1235',
          description: 'Product purchase'
        },
        { 
          id: '1236', 
          amount: '$300', 
          status: 'Failed',
          date: '02/04/2025',
          customer: 'Robert Brown',
          paymentMethod: 'PayPal',
          reference: 'REF-1236',
          description: 'Service fee'
        }
      ],
      selectedTransactions: [],
      expandedTransactions: [],
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
    toggleExpand(transactionId) {
      if (this.expandedTransactions.includes(transactionId)) {
        this.expandedTransactions = this.expandedTransactions.filter(id => id !== transactionId);
      } else {
        this.expandedTransactions.push(transactionId);
      }
    },
    refreshTransactions() {
      this.isLoading = true;
      
      // Simulating an API call with setTimeout
      setTimeout(() => {
        // In a real application, you would fetch data from an API
        // For demo purposes, we'll just update the existing data
        const newTransaction = {
          id: Math.floor(1000 + Math.random() * 9000).toString(),
          amount: '$' + Math.floor(100 + Math.random() * 900),
          status: ['Confirmed', 'Pending', 'Failed'][Math.floor(Math.random() * 3)],
          date: '05/04/2025',
          customer: 'New Customer',
          paymentMethod: 'Credit Card',
          reference: 'REF-NEW',
          description: 'New transaction'
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

.transaction-row {
  cursor: pointer;
}

.transaction-row:hover {
  background-color: #f5f5f5;
}

.expanded-details {
  background-color: #f9f9f9;
}

.transaction-details {
  padding: 15px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-top: 10px;
}

.detail-item {
  display: flex;
}

.label {
  font-weight: bold;
  margin-right: 10px;
  min-width: 120px;
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