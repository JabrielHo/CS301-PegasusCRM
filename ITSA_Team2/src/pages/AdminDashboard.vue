<template>
  <div class="admin-dashboard">
    <div class="header-actions">
      <h1>Admin Dashboard</h1>
      <button class="refresh-btn" @click="refreshData">
        <span class="refresh-icon">↻</span> Refresh
      </button>
    </div>
    
    <div id="table-container">
      <div class="client-table">
        <table>
          <thead>
            <tr>
              <th>Client Name</th>
              <th>Date</th>
              <th>Activity</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="account in paginatedAccounts" :key="account.clientName" class="clients">
              <td>{{ account.clientName }}</td>
              <td>{{ account.date }}</td>
              <td>{{ account.activity }}</td>
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
      adminName: 'John Doe',
      accounts: [
        { clientName: 'John Haaland', date: '20/03/2021', activity: 'Updated account' },
        { clientName: 'John Wick', date: '21/03/2021', activity: 'Bought new Policy' },
        { clientName: 'Jane Smith', date: '22/03/2021', activity: 'Updated profile' },
        { clientName: 'Alan Turing', date: '23/03/2021', activity: 'Added new account' },
      ],
      currentPage: 1,
      itemsPerPage: 50,
      isLoading: false
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.accounts.length / this.itemsPerPage);
    },
    paginatedAccounts() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.accounts.slice(start, end);
    }
  },
  methods: {
    createNewAccount() {
      console.log('Creating new account...');
      // Implement the account creation logic
    },
    manageAccounts() {
      console.log('Managing accounts...');
      // Implement account management logic
    },
    refreshData() {
      this.isLoading = true;
      
      // Simulating an API call with setTimeout
      setTimeout(() => {
        // In a real application, you would fetch data from an API
        const newAccount = {
          clientName: 'New Client',
          date: new Date().toLocaleDateString('en-GB'),
          activity: 'Created account'
        };
        
        this.accounts.unshift(newAccount);
        this.isLoading = false;
      }, 500);
    }
  }
};
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
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

#admin-container {
  display: flex;
  justify-content: space-between; 
  align-items: center; 
}

.admin-name {
  font-size: 18px;
  margin-bottom: 0;
}

.button-container {
  display: flex;
  gap: 5px;
  margin-top: 20px;
  margin-bottom: 20px;
  justify-content: end;
}

.btn {
  background-color: #007bff;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #0056b3;
}

.client-table {
  border-radius: 10px;
  background-color: #fefefe;
  text-align: center;
}

.client-table table {
  width: 98%;
  border-collapse: collapse;
  margin: 10px;
}

.clients {
  border-top: solid rgb(215, 215, 215) 1px;
}

.client-table th, td {
  padding: 10px;
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
</style>