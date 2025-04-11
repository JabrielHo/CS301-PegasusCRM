<template>
  <div class="admin-dashboard">
    <div class="header-actions">
      <h1>Agent Activity Dashboard</h1>
      <div class="action-buttons">
        <button class="filter-btn" @click="toggleFilterPanel">
          <span class="filter-icon">⚡</span> Filters
        </button>
        <button class="refresh-btn" @click="refreshData" :disabled="isLoading">
          <span class="refresh-icon" :class="{ 'spinning': isLoading }">↻</span> 
          {{ isLoading ? 'Loading...' : 'Refresh' }}
        </button>
      </div>
    </div>
    
    <!-- Filter panel -->
    <div class="filter-panel" v-if="showFilters">
      <div class="filter-row">
        <div class="filter-group">
          <label for="date-range"">Date Range:</label>
          <select id="date-range" v-model="filters.dateRange">
            <option value="today">Today</option>
            <option value="yesterday">Yesterday</option>
            <option value="last7days">Last 7 Days</option>
            <option value="last30days">Last 30 Days</option>
            <option value="custom">Custom Range</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="activity-type">Activity Type:</label>
          <select id="activity-type" v-model="filters.activityType">
            <option value="all">All Activities</option>
            <option value="login">Login</option>
            <option value="client-update">Client Update</option>
            <option value="policy-creation">Policy Creation</option>
            <option value="claim-processing">Claim Processing</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="agent-search">Search Agent:</label>
          <input 
            type="text" 
            id="agent-search" 
            v-model="filters.agentSearch" 
            placeholder="Search by agent name"
          >
        </div>
      </div>
    </div>
    
    <!-- Stats summary boxes -->
    <div class="stats-summary">
      <div class="stat-box">
        <div class="stat-value">{{ stats.totalAgents }}</div>
        <div class="stat-label">Active Agents</div>
      </div>
      <div class="stat-box">
        <div class="stat-value">{{ stats.totalActivities }}</div>
        <div class="stat-label">Total Activities</div>
      </div>
      <div class="stat-box">
        <div class="stat-value">{{ stats.avgActivitiesPerDay }}</div>
        <div class="stat-label">Avg. Activities/Day</div>
      </div>
      <div class="stat-box">
        <div class="stat-value">{{ stats.newClients }}</div>
        <div class="stat-label">New Clients Today</div>
      </div>
    </div>
    
    <!-- Main table -->
    <div id="table-container">
      <div class="status-bar" v-if="isLoading">
        <div class="loading-indicator">Loading agent activity data...</div>
      </div>
      
      <div class="agent-table" v-else>
        <table>
          <thead>
            <tr>
              <th @click="sortBy('agentName')">
                Agent ID
                <span class="sort-indicator" v-if="sortColumn === 'agentName'">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('timestamp')">
                Date & Time
                <span class="sort-indicator" v-if="sortColumn === 'timestamp'">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('activityType')">
                Activity Type
                <span class="sort-indicator" v-if="sortColumn === 'activityType'">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('clientName')">
                Client
                <span class="sort-indicator" v-if="sortColumn === 'clientName'">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="paginatedActivities.length === 0">
              <td colspan="6" class="no-data">No agent activities found</td>
            </tr>
            <tr v-for="activity in paginatedActivities" :key="activity.id" class="activity-row">
              <td>
                <div class="agent-name">
                  {{ activity.agentID }}
                </div>
              </td>
              <td>{{ formatDateTime(activity.dateTime) }}</td>
              <td>
                <span class="activity-badge" :class="activityTypeClass(activity.activityType)">

                </span>
                {{ activity.action }}
              </td>
              <td>{{ activity.clientName }}</td>
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
import axiosInstance from 'axios';
export default {
  data() {
    return {
      isLoading: false,
      showFilters: false,
      filters: {
        dateRange: 'last7days',
        activityType: 'all',
        agentSearch: ''
      },
      stats: {
        totalAgents: 0,
        totalActivities: 0,
        avgActivitiesPerDay: 0,
        newClients: 0
      },
      activities: [],
      currentPage: 1,
      itemsPerPage: 10,
      sortColumn: 'timestamp',
      sortDirection: 'desc'
    };
  },
  computed: {
    filteredActivities() {
      return this.activities.filter(activity => {
        // Apply filters here when implemented
        if (this.filters.agentSearch && !activity.agentName.toLowerCase().includes(this.filters.agentSearch.toLowerCase())) {
          return false;
        }
        if (this.filters.activityType !== 'all' && activity.activityType !== this.filters.activityType) {
          return false;
        }
        // Date filtering would be applied here
        return true;
      }).sort((a, b) => {
        // Apply sorting
        const modifier = this.sortDirection === 'asc' ? 1 : -1;
        if (a[this.sortColumn] < b[this.sortColumn]) return -1 * modifier;
        if (a[this.sortColumn] > b[this.sortColumn]) return 1 * modifier;
        return 0;
      });
    },
    paginatedActivities() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredActivities.slice(start, end);
    },
    totalPages() {
      return Math.max(1, Math.ceil(this.filteredActivities.length / this.itemsPerPage));
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
    // Fetch initial data when component is created
    this.fetchAgentActivities();
    this.fetchDashboardStats();
  },
  methods: {
    // Fetch agent activities from API
    fetchAgentActivities() {
      this.isLoading = true;

      // API endpoint for agent activities
      const endpoint = 'https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/records';
      
      axiosInstance.get(endpoint)
        .then(response => {
          this.activities = response.data;
          this.isLoading = false;
      
          console.log('Fetched agent activities:', [...this.activities]);
        })
        .catch(error => {
          console.error('Error fetching agent activities:', error);
          this.isLoading = false;
        });
    },
    
    // Fetch dashboard statistics
    fetchDashboardStats() {
      // API endpoint for dashboard stats
      const endpoint = '/api/dashboard-stats';
      
      // In a real implementation, you would use axios or fetch
      // axios.get(endpoint)
      //   .then(response => {
      //     this.stats = response.data;
      //   })
      //   .catch(error => {
      //     console.error('Error fetching dashboard stats:', error);
      //   });
      
      // For demonstration, we'll use mock data
      setTimeout(() => {
        this.stats = {
          totalAgents: 8,
          totalActivities: 127,
          avgActivitiesPerDay: 18,
          newClients: 3
        };
      }, 600);
    },
    
    // Refresh data
    refreshData() {
      this.fetchAgentActivities();
      this.fetchDashboardStats();
    },
    
    // Toggle filter panel visibility
    toggleFilterPanel() {
      this.showFilters = !this.showFilters;
    },
    // Sort table by column
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
    
    // Format date and time
    formatDateTime(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    // Get CSS class for activity type
    activityTypeClass(type) {
      const classes = {
        'Login': 'activity-login',
        'Client Update': 'activity-update',
        'Policy Creation': 'activity-create',
        'Claim Processing': 'activity-claim'
      };
      return classes[type] || 'activity-default';
    },
    
    // View activity details
    viewDetails(activityId) {
      // In a real application, this would open a modal or navigate to a details page
      console.log(`Viewing details for activity ID: ${activityId}`);
      alert(`View details for activity ID: ${activityId}`);
    },
    
    // Send notification to agent
    sendNotification(activityId) {
      // In a real application, this would open a notification form or dialog
      console.log(`Sending notification related to activity ID: ${activityId}`);
      alert(`Send notification related to activity ID: ${activityId}`);
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

.agent-table {
  overflow-x: auto;
}

.agent-table table {
  width: 100%;
  border-collapse: collapse;
}

.agent-table th {
  background-color: #f7fafc;
  padding: 12px 15px;
  text-align: left;
  font-weight: 600;
  color: #4a5568;
  border-bottom: 1px solid #e2e8f0;
  cursor: pointer;
  position: relative;
}

.agent-table th:hover {
  background-color: #edf2f7;
}

.sort-indicator {
  position: absolute;
  right: 10px;
}

.agent-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #e2e8f0;
  color: #2d3748;
}

.activity-row:hover {
  background-color: #f7fafc;
}

.no-data {
  text-align: center;
  padding: 30px;
  color: #a0aec0;
}

.agent-name {
  display: flex;
  align-items: center;
  gap: 10px;
}

.agent-avatar {
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

.activity-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.activity-login {
  background-color: #e6fffa;
  color: #2c7a7b;
}

.activity-update {
  background-color: #ebf8ff;
  color: #2b6cb0;
}

.activity-create {
  background-color: #faf5ff;
  color: #6b46c1;
}

.activity-claim {
  background-color: #fff5f5;
  color: #c53030;
}

.activity-default {
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