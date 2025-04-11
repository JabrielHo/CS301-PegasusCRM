<template>
  <div class="admin-dashboard">
    <!-- Header with Profile Summary -->
    <div class="dashboard-header">
      <h1>Client Profile</h1>
      <p class="dashboard-subtitle">Complete client account information</p>
    </div>

    <!-- Client Profile Details -->
    <div class="card profile-card">
      <div class="card-header">
        <h2>Profile Details</h2>
        <button class="btn-edit-profile" @click="openEditModal">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
          Edit Profile
        </button>
      </div>
      <div class="profile-content">
        <div class="profile-info">
          <div class="info-group">
            <div class="info-label">Client ID</div>
            <div class="info-value">{{ client.ClientID }}</div>
          </div>
          <div class="info-group">
            <div class="info-label">Client Name</div>
            <div class="info-value">
              {{ client.FirstName + " " + client.LastName }}
            </div>
          </div>
          <div class="info-group">
            <div class="info-label">Address</div>
            <div class="info-value">{{ client.Address || "Not provided" }}</div>
          </div>
          <div class="info-group">
            <div class="info-label">City</div>
            <div class="info-value">{{ client.City || "Not provided" }}</div>
          </div>
          <div class="info-group">
            <div class="info-label">State</div>
            <div class="info-value">{{ client.State || "Not provided" }}</div>
          </div>
          <div class="info-group">
            <div class="info-label">Postal Code</div>
            <div class="info-value">
              {{ client.PostalCode || "Not provided" }}
            </div>
          </div>
        </div>
        <div class="profile-info">
          <div class="info-group">
            <div class="info-label">Gender</div>
            <div class="info-value">{{ client.Gender || "Not provided" }}</div>
          </div>
          <div class="info-group">
            <div class="info-label">Email</div>
            <div class="info-value">
              {{ client.EmailAddress || "Not provided" }}
            </div>
          </div>
          <div class="info-group">
            <div class="info-label">Phone</div>
            <div class="info-value">
              {{ client.PhoneNumber || "Not provided" }}
            </div>
          </div>
          <div class="info-group">
            <div class="info-label">Date of Birth</div>
            <div class="info-value">
              {{ formatDate(client.DateOfBirth) || "Not provided" }}
            </div>
          </div>
          <div class="info-group">
            <div class="info-label">Status</div>
            <div class="info-value">
              <span :class="['status-badge', client.Verified ? 'confirmed' : 'pending']">
                {{ client.Verified ? "Verified" : "Not Verified" }}
              </span>
            </div>
          </div>
          <div class="info-group" style="display: flex; gap: 10px; margin: 10px 0">
            <!-- Button to view verification documents -->
            <button class="btn-view" @click="fetchVerificationDocuments(client.ClientID)">View Documents</button>
            <!-- Button to send verification -->
            <button class="btn-verify" v-if="!client.Verified" @click="sendVerification(client.ClientID)">
              Send Verification
            </button>
            <!-- Button to verify user -->
            <button class="btn-verify" v-if="!client.Verified" @click="verifyUser(client.ClientID)">Verify User</button>
          </div>
          <div class="info-group">
            <!-- Display list of documents if available -->
            <div v-if="documents.length > 0" style="display: flex; gap: 10px; margin: 10px 0">
              <div v-for="(doc, index) in documents" :key="index">
                <button class="btn-view" @click="getPresignedUrl(doc)">View {{ doc.split("/").pop() }}</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bank Accounts Section -->
    <div class="card accounts-card">
      <div class="card-header">
        <h2>Bank Accounts</h2>
        <button class="btn-add" @click="openAddAccountModal">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M12 5v14M5 12h14"></path>
          </svg>
          Add New Account
        </button>
      </div>

      <!-- Account Search and Filter -->
      <div class="accounts-filter">
        <div class="search-container">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input id="accountSearch" v-model="accountSearchQuery" type="text" placeholder="Search accounts..." />
        </div>
        <div class="filter-container">
          <label for="typeFilter">Filter by type:</label>
          <select id="typeFilter" v-model="accountTypeFilter">
            <option value="">All Types</option>
            <option value="Checking">Checking</option>
            <option value="Savings">Savings</option>
            <option value="Investment">Investment</option>
          </select>
        </div>
      </div>

      <!-- Accounts Table -->
      <div class="accounts-table">
        <table>
          <thead>
            <tr>
              <th>Account ID</th>
              <th>Account Type</th>
              <th>Status</th>
              <th>Opening Date</th>
              <th>Initial Deposit</th>
              <th>Currency</th>
              <th>Branch ID</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="account in filteredBankAccounts" :key="account.id" class="account-row">
              <td>{{ account.id }}</td>
              <td>{{ account.type }}</td>
              <td>
                <span :class="['status-badge', account.active ? 'confirmed' : 'pending']">
                  {{ account.accountStatus }}
                </span>
              </td>
              <td>{{ formatDate(account.openingDate) }}</td>
              <td>{{ formatCurrency(account.initialDeposit, account.currency) }}</td>
              <td>{{ account.currency }}</td>
              <td>{{ account.branchId }}</td>
              <td>
                <div class="action-buttons-cell">
                  <button class="btn-icon" title="View Transactions" @click="viewTransactions(account.id)">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <polyline points="22 12 16 12 14 15 10 15 8 12 2 12"></polyline>
                      <path
                        d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"
                      ></path>
                    </svg>
                  </button>
                  <button class="btn-icon" title="Edit Account" @click="editAccount(account.id)">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                  </button>
                  <button class="btn-icon danger" title="Freeze Account" @click="toggleAccountStatus(account.id)">
                    <svg
                      v-if="account.active"
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path d="M2 12h20M2 12a10 10 0 1 0 20 0 10 10 0 1 0-20 0z"></path>
                    </svg>
                    <svg
                      v-else
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path d="M12 2v20M4.93 4.93l14.14 14.14"></path>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredBankAccounts.length === 0">
              <td colspan="8" class="no-results">
                <div class="empty-state">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="48"
                    height="48"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                  </svg>
                  <p>No bank accounts found for this client</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Account Summary Footer -->
      <div class="account-summary">
        <div class="summary-item">
          <div class="summary-label">Total Accounts</div>
          <div class="summary-value">{{ client.bankAccounts.length }}</div>
        </div>
        <div class="summary-item">
          <div class="summary-label">Active Accounts</div>
          <div class="summary-value">{{ client.bankAccounts.filter((a) => a.active).length }}</div>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <div v-if="showEditProfileModal" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal">
        <div class="modal-header">
          <h3>Edit Client Profile</h3>
          <button class="btn-close" @click="closeEditModal">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div class="modal-content">
          <div class="form-group">
            <label for="editFirstName">First Name</label>
            <input id="editFirstName" v-model="editedClient.FirstName" type="text" />
          </div>

          <div class="form-group">
            <label for="editLastName">Last Name</label>
            <input id="editLastName" v-model="editedClient.LastName" type="text" />
          </div>

          <div class="form-group">
            <label for="editDateOfBirth">Date of Birth</label>
            <input id="editDateOfBirth" v-model="editedClient.DateOfBirth" type="date" />
          </div>

          <div class="form-group">
            <label for="editEmailAddress">Email Address</label>
            <input id="editEmailAddress" v-model="editedClient.EmailAddress" type="email" />
          </div>

          <div class="form-group">
            <label for="phone">Phone Number</label>
            <vue-tel-input
              v-model="editedClient.PhoneNumber"
              :inputOptions="telInputOptions"
              :dropdownOptions="telDropdownOptions"
              mode="international"
              required
              class="tel-input-container"
            ></vue-tel-input>
          </div>

          <div class="form-group">
            <label for="editAddress">Address</label>
            <input id="editAddress" v-model="editedClient.Address" />
          </div>

          <div class="form-group">
            <label for="editCity">City</label>
            <input id="editCity" v-model="editedClient.City" type="text" />
          </div>

          <div class="form-group">
            <label for="editState">State</label>
            <input id="editState" v-model="editedClient.State" type="text" />
          </div>

          <div class="form-group">
            <label for="country">Country</label>
            <select v-model="client.Country" id="country" required @change="updatePhoneCountry">
              <option value="" disabled selected>Select Country</option>
              <option v-for="country in countries" :key="country.name" :value="country.name">
                {{ country.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="editPostalCode">Postal Code</label>
            <input id="editPostalCode" v-model="editedClient.PostalCode" type="text" />
          </div>

          <div class="form-group">
            <label for="editGender">Gender</label>
            <select id="editGender" v-model="editedClient.Gender">
              <option disabled value="">Select Gender</option>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
              <option>Prefer not to say</option>
            </select>
          </div>
        </div>

        <div class="modal-footer">
          <div class="action-buttons">
            <button class="btn-cancel" @click="closeEditModal">Cancel</button>
            <button class="btn-save" @click="saveProfileChanges">Save Changes</button>
            <button class="btn-delete" @click="openDeletePopup('client', client)">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Bank Account Modal -->
    <div v-if="showEditAccountModal" class="modal-overlay" @click.self="closeAccountModal">
      <div class="modal">
        <div class="modal-header">
          <h3>
            {{ isAddingAccount ? "Add New Bank Account" : "Edit Bank Account" }}
          </h3>
          <button class="btn-close" @click="closeAccountModal">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div class="modal-content">
          <div class="account-id" v-if="!isAddingAccount">
            <svg
              class="account-icon"
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect x="2" y="5" width="20" height="14" rx="2"></rect>
              <line x1="2" y1="10" x2="22" y2="10"></line>
            </svg>
            <span>Account ID: {{ editedAccount.id }}</span>
          </div>

          <div class="form-group">
            <label for="accountType">Account Type</label>
            <select id="accountType" v-model="editedAccount.type">
              <option value="Checking">Checking</option>
              <option value="Savings">Savings</option>
              <option value="Investment">Investment</option>
              <option value="Credit">Credit</option>
            </select>
          </div>

          <div class="form-group" v-if="isAddingAccount">
            <label for="initialDeposit">Initial Deposit</label>
            <input id="initialDeposit" v-model="editedAccount.initialDeposit" type="number" min="0" step="0.01" />
          </div>

          <div class="form-group" v-if="isAddingAccount">
            <label for="accountCurrency">Currency</label>
            <select id="accountCurrency" v-model="editedAccount.currency">
              <option value="USD">USD - US Dollar</option>
              <option value="EUR">EUR - Euro</option>
              <option value="GBP">GBP - British Pound</option>
              <option value="JPY">JPY - Japanese Yen</option>
              <option value="CAD">CAD - Canadian Dollar</option>
            </select>
          </div>

          <div class="form-group" v-if="isAddingAccount">
            <label for="branchId">Branch ID</label>
            <select id="branchId" v-model="editedAccount.branchId">
              <template v-for="branch in branches">
                <option :value="branch.branchId">{{ branch.branchName }}</option>
              </template>
            </select>
          </div>

          <div class="form-section" v-if="!isAddingAccount">
            <h4>Account Status</h4>
            <div class="status-toggle">
              <button @click="toggleEditedAccountStatus" :class="editedAccount.active ? 'btn-disable' : 'btn-enable'">
                <svg
                  v-if="editedAccount.active"
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M18.36 6.64a9 9 0 1 1-12.73 0"></path>
                  <line x1="12" y1="2" x2="12" y2="12"></line>
                </svg>
                <svg
                  v-else
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M5 12h14"></path>
                  <path d="M12 5v14"></path>
                </svg>
                {{ editedAccount.active ? "Deactivate Account" : "Activate Account" }}
              </button>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <div class="action-buttons">
            <button class="btn-cancel" @click="closeAccountModal">Cancel</button>
            <button class="btn-save" @click="saveAccountChanges">
              {{ isAddingAccount ? "Create Account" : "Save Changes" }}
            </button>
          </div>

          <div class="danger-zone" v-if="!isAddingAccount">
            <button class="btn-delete" @click="confirmDeleteAccount">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
              Delete Account
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Client/Account Delete Confirmation Popup -->
    <div v-if="showDeleteConfirmation" class="popup-overlay" @click.self="closePopup">
      <div class="popup">
        <div class="popup-header">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <h4>Confirm Deletion</h4>
        </div>
        <div class="popup-content">
          <p>Are you sure you want to delete this {{ itemType }}?</p>
          <!-- If Deleting Client -->
          <p v-if="itemToDelete.ClientID"><strong>Client ID:</strong> {{ itemToDelete.ClientID }}</p>
          <p v-if="itemToDelete.FirstName || itemToDelete.LastName">
            <strong>Name:</strong>
            {{ itemToDelete.FirstName + " " + itemToDelete.LastName }}
          </p>
          <!-- If Deleting Account -->
          <p v-if="itemToDelete.accountID"><strong>ID:</strong> {{ itemToDelete.clientID }}</p>
          <p v-if="itemToDelete.type"><strong>Type:</strong> {{ itemToDelete.type }}</p>
          <p class="warning-text">This action cannot be undone.</p>
        </div>
        <div class="popup-footer">
          <button class="btn-cancel" @click="closePopup">Cancel</button>
          <button class="btn-delete" @click="deleteItem">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../services/axiosInstance";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import postalCodesData from "../postal_codes_regex.json"; // Adjust path as needed

export default {
  name: "ClientProfilePage",
  data() {
    return {
      // Client data
      clientID: null,
      client: {
        bankAccounts: [],
      },

      // Country + Telephone
      countries: [],
      telInputOptions: {
        placeholder: "Phone Number",
        type: "tel",
        inputClass: "tel-input",
      },
      telDropdownOptions: {
        showDialCodeInSelection: true,
        showFlags: true,
        showSearchBox: true,
      },

      // Delete Pop Up
      showDeleteConfirmation: false,
      itemToDelete: {},
      itemType: "",

      // Documents from S3
      documents: [],
      imageUrl: "",

      // UI state variables
      showEditProfileModal: false,
      showEditAccountModal: false,
      isAddingAccount: false,
      editedClient: {},
      editedAccount: {},
      accountSearchQuery: "",
      accountTypeFilter: "",
      branches: "",
    };
  },
  created() {
    // Extract countries from the imported JSON data
    this.countries = postalCodesData
      .map((country) => ({
        code: country.abbrev,
        name: country.name,
      }))
      .sort((a, b) => a.name.localeCompare(b.name));

    // Create a lookup for postal code patterns by country name
    this.postalCodePatterns = postalCodesData.reduce((acc, country) => {
      if (country.postal) {
        acc[country.name] = country.postal;
      }
      return acc;
    }, {});
  },
  computed: {
    // Filter bank accounts based on search and type filter
    filteredBankAccounts() {
      return this.client.bankAccounts.filter((account) => {
        // Search by account ID
        const matchesSearch = account.id.toLowerCase().includes(this.accountSearchQuery.toLowerCase());

        // Filter by account type
        const matchesType = !this.accountTypeFilter || account.type === this.accountTypeFilter;

        return matchesSearch && matchesType;
      });
    },
  },
  mounted() {
    // Retrieve the clientID from the URL params
    this.clientID = this.$route.params.clientID;
    this.loadClient(); // Call the method to load client data using the clientID
    this.getBranches();
  },
  methods: {
    // Format date to a readable format
    formatDate(dateString) {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    },
    // Format currency for display
    formatCurrency(amount, currency = "USD") {
      return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: currency,
      }).format(amount);
    },
    // Open edit profile modal
    openEditModal() {
      this.editedClient = { ...this.client };
      this.showEditProfileModal = true;
    },
    // Close edit profile modal
    closeEditModal() {
      this.showEditProfileModal = false;
      this.editedClient = {};
    },
    // Toggle client status
    toggleClientStatus() {
      this.editedClient.active = !this.editedClient.active;
    },
    loadClient() {
      // Assuming your API is set to retrieve client by ID
      axiosInstance
        .get(`https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/api/clients/${this.clientID}`)
        .then((response) => {
          this.client = response.data.client;
          console.log("Client data loaded:", this.client);
          this.loadClientAccounts(this.clientID);
        })
        .catch((error) => {
          console.error("Error fetching client data:", error);
        });
    },
    async loadClientAccounts(clientId) {
      try {
        const response = await axiosInstance.get(`http://127.0.0.1:5002/manage_account/retrieve/${clientId}`);
        console.log("Client accounts loaded:", response.data);

        if (response.data.accounts && Array.isArray(response.data.accounts)) {
          this.client.bankAccounts = response.data.accounts.map((account) => ({
            id: account.accountId,
            type: account.accountType,
            active: account.accountStatus === "Active",
            accountStatus: account.accountStatus,
            openingDate: account.openingDate,
            initialDeposit: account.initialDeposit,
            currency: account.currency,
            branchId: account.branchId,
          }));
        } else {
          // No accounts or invalid response
          this.client.bankAccounts = [];
        }
      } catch (error) {
        console.error("Error fetching client accounts:", error);
        this.client.bankAccounts = [];
      }
    },
    async getBranches() {
      try {
        const response = await axiosInstance.get(
          "http://account-ecs-lb-852197336.ap-southeast-1.elb.amazonaws.com/api/branches"
        );
        console.log("Branches loaded:", response.data);

        this.branches = response.data.branches;
      } catch (error) {
        console.error("Error fetching branches:", error);
        this.branches = [];
      }
    },
    // Save profile changes
    saveProfileChanges() {
      this.editedClient.PhoneNumber = this.editedClient.PhoneNumber.replace(/\s+/g, "");
      this.client = { ...this.editedClient };

      // TODO: Remove with Actual Endpoint
      axiosInstance
        .put(
          `https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/api/clients/${this.clientID}`,
          this.editedClient
        )
        .then((response) => {
          console.log("Client profile saved successfully:", response.data);
          toast("Client profile saved successfully!", {
            type: "success",
            autoClose: 3000,
          });
          this.closeEditModal();
        })
        .catch((error) => {
          // Handle error response
          // If the error response contains validation errors
          if (error.status == 400) {
            const errors = error.response.data.errors;
            // Display error messages
            for (const error of errors) {
              toast(error, {
                type: "error",
                autoClose: 3000,
              });
            }
          }
          // If the error response indicates a conflict (e.g., duplicate email)
          else if (error.status == 409) {
            toast(error.response.data.error, {
              type: "error",
              autoClose: 3000,
            });
          } else {
            toast("An unexpected error occurred. Please try again.", {
              type: "error",
              autoClose: 3000,
            });
          }
          console.error("Error saving client profile:", error);
        });
    },
    // Fetch Documents from S3
    fetchVerificationDocuments(clientID) {
      axiosInstance
        .get(`https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/api/clients/${clientID}/documents`)
        .then((response) => {
          this.documents = response.data.documents.map((doc) => {
            // Extract the file name by splitting at '/' and returning the last part
            return doc.split("/").pop();
          });
        })
        .catch((error) => {
          console.error("Error fetching documents:", error);
        });
    },
    // Send verification email
    sendVerification(clientID){
      axiosInstance.post(`https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/api/clients/${clientID}/verify`)
        .then(() => {
          toast("Verification email sent successfully!", {
            type: "success",
            autoClose: 3000,
          });
        })
        .catch((error) => {
          console.error("Error sending verification email:", error);
          toast("Error sending verification email. Please try again.", {
            type: "error",
            autoClose: 3000,
          });
        });
    },
    // Verify user
    verifyUser(clientID) {
      axiosInstance
        .put(`https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/api/clients/${clientID}/verify_user`, {
          Verified: true,
        })
        .then(() => {
          toast("User verified successfully!", {
            type: "success",
            autoClose: 3000,
          });
          this.loadClient();
        })
        .catch((error) => {
          console.error("Error verifying user:", error);
          toast("Error verifying user. Please try again.", {
            type: "error",
            autoClose: 3000,
          });
        });
    },
    // Get pre-signed URL for document
    getPresignedUrl(doc) {
      axiosInstance
        .get(
          `https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/api/clients/${this.clientID}/documents/presign/${doc}`
        )
        .then((response) => {
          console.log("Pre-signed URL fetched successfully:", response.data);
          this.imageUrl = response.data.link; // Store the pre-signed URL

        window.open(response.data.link, "_blank"); // Open the pre-signed URL in a new tab
      });
    },
    openDeletePopup(itemType, item) {
      this.itemType = itemType;
      this.itemToDelete = item;
      this.showDeleteConfirmation = true;
    },
    closePopup() {
      this.showDeleteConfirmation = false;
      this.itemToDelete = {};
    },
    deleteItem() {
      if (this.itemType === "client") {
        this.deleteClient(this.itemToDelete.ClientID);
      } else if (this.itemType === "bank account") {
        this.deleteAccount(this.itemToDelete.AccountID);
      }
    },
    deleteClient(clientID) {
      // Your logic to delete client
      console.log("Deleting client:", clientID);
      axiosInstance
        .delete(`https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/api/clients/${clientID}`)
        .then(() => {
          toast("Client deleted successfully!", {
            type: "success",
            autoClose: 3000,
          });
        })
        .catch((error) => {
          console.error("Error deleting client:", error);
          toast("Error deleting client. Please try again.", {
            type: "error",
            autoClose: 3000,
          });
        });
      // Redirect to the agent manage profiles page
      this.$router.push("/agent-manage-profiles");
    },
    deleteAccount(accountID) {
      // Your logic to delete account
      console.log("Deleting account:", accountID);
    },
    // Open add/edit account modal
    openAddAccountModal() {
      this.isAddingAccount = true;
      this.editedAccount = {
        type: "Checking",
        active: true,
        initialDeposit: 0,
        currency: "USD",
        branchId: "BR001",
        openingDate: new Date().toISOString().split("T")[0],
      };
      this.showEditAccountModal = true;
    },
    // Edit existing account
    editAccount(accountId) {
      const account = this.client.bankAccounts.find((a) => a.id === accountId);
      if (account) {
        this.isAddingAccount = false;
        this.editedAccount = { ...account };
        this.showEditAccountModal = true;
      }
    },

    // Close account modal
    closeAccountModal() {
      this.showEditAccountModal = false;
      this.editedAccount = {};
    },

    // Toggle edited account status
    toggleEditedAccountStatus() {
      this.editedAccount.active = !this.editedAccount.active;
    },

    // Save account changes
    saveAccountChanges() {
      if (this.isAddingAccount) {
        // Generate a new account ID (in real app this would come from the server)
        const newId = `BA${String(this.client.bankAccounts.length + 1).padStart(3, "0")}`;
        const newAccount = {
          ...this.editedAccount,
          id: newId,
          balance: this.editedAccount.initialDeposit,
          active: true,
        };
        this.client.bankAccounts.push(newAccount);
      } else {
        // Update existing account
        const index = this.client.bankAccounts.findIndex((a) => a.id === this.editedAccount.id);
        if (index !== -1) {
          this.client.bankAccounts[index] = { ...this.editedAccount };
        }
      }
      this.closeAccountModal();
      // In a real app, this would send an API request to create/update the account
    },

    // Toggle account status
    toggleAccountStatus(accountId) {
      const index = this.client.bankAccounts.findIndex((a) => a.id === accountId);
      if (index !== -1) {
        this.client.bankAccounts[index].active = !this.client.bankAccounts[index].active;
        // In a real app, this would send an API request to update the status
      }
    },

    // Confirm account deletion
    confirmDeleteAccount() {
      this.accountToDelete = { ...this.editedAccount };
      this.closeAccountModal();
      this.showDeleteConfirmation = true;
    },

    // Delete account
    deleteAccount() {
      this.client.bankAccounts = this.client.bankAccounts.filter((account) => account.id !== this.accountToDelete.id);
      this.closePopup();
      // In a real app, this would send an API request to delete the account
    },

    // View transactions (placeholder function - would navigate to transactions page)
    viewTransactions(accountId) {
      console.log(`View transactions for account ${accountId}`);
      // In a real app, this would navigate to a transactions page
      // this.$router.push(`/transactions/${accountId}`);
    },
  },
};
</script>

<style scoped>
:root {
  --primary-color: #4f46e5;
  --primary-hover: #4338ca;
  --secondary-color: #e2e8f0;
  --danger-color: #ef4444;
  --danger-hover: #b91c1c;
  --success-color: #10b981;
  --success-hover: #059669;
  --warning-color: #f59e0b;
  --warning-hover: #d97706;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --background-color: #f8fafc;
  --card-background: #ffffff;
  --border-color: #e2e8f0;
  --shadow-color: rgba(0, 0, 0, 0.08);
  --table-header-bg: #f1f5f9;
  --table-row-hover: #f1f5f9;
  --table-row-alternate: #f8fafc;
  --disabled-row-bg: #f1f5f9;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.admin-dashboard {
  font-family:
    "Inter",
    system-ui,
    -apple-system,
    sans-serif;
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
  padding: 1.75rem;
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(79, 70, 229, 0.2);
}

.dashboard-header h1 {
  font-size: 1.875rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  margin-bottom: 0.25rem;
}

.dashboard-subtitle {
  font-size: 1rem;
  opacity: 0.85;
  font-weight: 400;
}

/* Card Styles */
.card {
  background-color: var(--card-background);
  border-radius: 1rem;
  box-shadow: 0 4px 20px var(--shadow-color);
  overflow: hidden;
  border: 1px solid var(--border-color);
  transition:
    box-shadow 0.3s ease,
    transform 0.2s ease;
  margin-bottom: 2rem;
}

.card:hover {
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background-color: #f8fafc;
  border-bottom: 1px solid var(--border-color);
}

.card-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.025em;
}

/* Profile Card Styles */
.profile-card {
  margin-bottom: 2rem;
}

.profile-content {
  display: flex;
  flex-wrap: wrap;
  padding: 1.5rem;
  gap: 2rem;
}

.profile-info {
  flex: 1;
  min-width: 250px;
}

.info-group {
  margin-bottom: 1.25rem;
}

.info-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.375rem;
  font-weight: 500;
}

.info-value {
  font-size: 1rem;
  color: var(--text-primary);
  font-weight: 500;
}

/* Status Badges */
.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.375rem 0.875rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.status-badge.confirmed {
  background-color: rgba(16, 185, 129, 0.15);
  color: #065f46;
}

.status-badge.pending {
  background-color: rgba(245, 158, 11, 0.15);
  color: #92400e;
}

/* Button Styles */
.btn-edit-profile {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: white;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  color: var(--text-primary);
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-edit-profile:hover {
  background-color: #f8fafc;
  border-color: #cbd5e1;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.btn-edit-profile svg {
  color: var(--primary-color);
}

.btn-add {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: white;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  color: var(--text-primary);
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-add:hover {
  background-color: #f8fafc;
  border-color: #cbd5e1;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

/* Accounts Filter */
.accounts-filter {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background-color: #f8fafc;
  border-bottom: 1px solid var(--border-color);
  flex-wrap: wrap;
  gap: 1rem;
}

.search-container {
  position: relative;
  width: 100%;
  max-width: 350px;
  display: flex;
  align-items: center;
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
  padding: 0.625rem 1rem 0.625rem 2.5rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-primary);
  transition: all 0.2s ease;
  background-color: white;
}

.search-container input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
}

.filter-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.filter-container label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.filter-container select {
  padding: 0.625rem 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-primary);
  background-color: white;
  transition: all 0.2s ease;
}

.filter-container select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
}

/* Table Styles */
.accounts-table {
  overflow-x: auto;
}

.accounts-table table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.accounts-table th {
  padding: 1rem 1.5rem;
  background-color: var(--table-header-bg);
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid var(--border-color);
  text-align: left;
}

.accounts-table td {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-primary);
  font-size: 0.875rem;
  transition: background-color 0.2s ease;
}

.accounts-table tr {
  transition: background-color 0.15s ease;
}

.accounts-table tr:hover {
  background-color: var(--table-row-hover);
}

/* Action Buttons in Table */
.action-buttons-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 0.375rem;
  background-color: white;
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-icon:hover {
  background-color: #f8fafc;
  border-color: #cbd5e1;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.btn-icon.danger {
  color: var(--danger-color);
}

.btn-icon.danger:hover {
  background-color: #fee2e2;
  border-color: #fecaca;
}

/* Account Summary */
.account-summary {
  display: flex;
  padding: 1.25rem 1.5rem;
  background-color: #f8fafc;
  border-top: 1px solid var(--border-color);
  gap: 2rem;
  flex-wrap: wrap;
}

.summary-item {
  flex: 1;
  min-width: 120px;
}

.summary-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.summary-value {
  font-size: 1.125rem;
  color: var(--text-primary);
  font-weight: 600;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem 1rem;
}

.empty-state svg {
  color: #94a3b8;
  margin-bottom: 1rem;
  opacity: 0.7;
}

.empty-state p {
  color: #64748b;
  font-size: 0.95rem;
  text-align: center;
  font-weight: 500;
}

/* Modal Styles */
.modal-overlay {
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
  backdrop-filter: blur(4px);
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal {
  background-color: white;
  border-radius: 1rem;
  width: 100%;
  max-width: 550px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  animation: modalSlideIn 0.3s ease forwards;
  max-height: 90vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

@keyframes modalSlideIn {
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
  padding: 1.5rem;
  background: linear-gradient(135deg, #4338ca 0%, #6366f1 100%);
  color: white;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
  position: sticky;
  top: 0;
  z-index: 10;
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  letter-spacing: -0.025em;
}

.btn-close {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.15);
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 0.5rem;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-close:hover {
  background-color: rgba(255, 255, 255, 0.25);
  transform: rotate(90deg);
}

.modal-content {
  padding: 1.75rem;
  background-color: white;
}

/* Account ID display in modal */
.account-id {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background-color: #f1f5f9;
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
  font-weight: 500;
  color: var(--text-secondary);
  border-left: 3px solid var(--primary-color);
}

.account-icon {
  color: var(--primary-color);
}

/* Form Styles */
.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  color: var(--text-primary);
  transition: all 0.2s ease;
  background-color: white;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
}

.form-section {
  margin-top: 1.75rem;
  padding-top: 1.75rem;
  border-top: 1px solid #e2e8f0;
}

.form-section h4 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.status-toggle {
  display: flex;
  gap: 1rem;
}

/* Modal Footer Buttons */
.modal-footer {
  padding: 1.5rem;
  background-color: #f8fafc;
  border-top: 1px solid #e2e8f0;
  border-bottom-left-radius: 1rem;
  border-bottom-right-radius: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
}

.btn-cancel,
.btn-save,
.btn-delete {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-cancel {
  background-color: #f1f5f9;
  color: #475569;
}

.btn-cancel:hover {
  background-color: #e2e8f0;
}

.btn-save {
  background-color: #f1f5f9;
  color: #475569;
}

.btn-save:hover {
  background-color: #e2e8f0;
}

.btn-delete {
  background-color: #fee2e2;
  color: #b91c1c;
}

.btn-delete:hover {
  background-color: #ef4444;
  color: white;
}

.btn-disable,
.btn-enable {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  border-radius: 0.5rem;
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

/* Delete Confirmation Popup */
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
  z-index: 60;
  backdrop-filter: blur(4px);
}

.popup {
  background-color: white;
  border-radius: 1rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  animation: modalSlideIn 0.3s ease forwards;
  overflow: hidden;
}

.popup-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem;
  background-color: #fee2e2;
  border-bottom: 1px solid #fecaca;
}

.popup-header svg {
  color: #b91c1c;
}

.popup-header h4 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #b91c1c;
  margin: 0;
}

.popup-content {
  padding: 1.5rem;
  color: var(--text-primary);
}

.popup-content p {
  margin-bottom: 0.75rem;
}

.warning-text {
  color: #b91c1c;
  font-weight: 500;
  margin-top: 1rem;
}

.popup-footer {
  padding: 1.25rem 1.5rem;
  background-color: #f8fafc;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .admin-dashboard {
    padding: 1rem;
  }

  .profile-content {
    flex-direction: column;
    gap: 1rem;
  }

  .accounts-filter {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-container {
    max-width: 100%;
  }

  .modal-footer {
    flex-direction: column-reverse;
    gap: 1rem;
  }

  .action-buttons,
  .danger-zone {
    width: 100%;
  }

  .action-buttons {
    justify-content: flex-end;
  }

  .btn-delete,
  .btn-save,
  .btn-cancel {
    flex: 1;
    justify-content: center;
  }

  .modal {
    width: 90%;
    max-height: 80vh;
  }
}

/* Button animations */
.btn-save:active,
.btn-add:active,
.btn-delete:active {
  transform: scale(0.98);
}

/* Improve focus states for accessibility */
button:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

/* Phone input container styling */
.tel-input-container {
  width: 100%;
}

/* Fix the height and style of the phone input to match other inputs */
:deep(.vti__dropdown),
:deep(.vti__input) {
  height: 45px !important;
  min-height: 45px !important;
  padding: 12px !important;
  border-radius: 4px !important;
  font-size: 1rem !important;
  background-color: #fff !important;
}

/* Make the dropdown button and flag container match the height */
:deep(.vti__dropdown) {
  border-top-right-radius: 0 !important;
  border-bottom-right-radius: 0 !important;
  border-right: none !important;
}

/* Make the input field match styling */
:deep(.vti__input) {
  border-top-left-radius: 0 !important;
  border-bottom-left-radius: 0 !important;
  flex: 1 !important;
}

/* Adjust flag container size */
:deep(.vti__flag) {
  margin-top: 0 !important;
}

/* Focus styles for phone input components */
:deep(.vti__dropdown:focus),
:deep(.vti__input:focus) {
  outline: none !important;
  border-color: #4a90e2 !important;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2) !important;
}

/* Make sure the phone input components stay next to each other */
:deep(.vti__dropdown),
:deep(.vti__input) {
  display: inline-flex !important;
}

/* Base button styles */
.info-group button {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  font-weight: 500;
  cursor: pointer;
  font-size: 14px;
  transition:
    background-color 0.2s,
    transform 0.1s;
  flex: 1; /* Make buttons take equal space */
  white-space: nowrap;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* View Documents button - blue style */
.btn-view {
  background-color: #3498db;
  color: white;
}

.btn-view:hover {
  background-color: #2980b9;
}

.btn-view:active {
  transform: scale(0.98);
}

/* Verify User button - green style */
.btn-verify {
  background-color: #2ecc71;
  color: white;
}

.btn-verify:hover {
  background-color: #27ae60;
}

.btn-verify:active {
  transform: scale(0.98);
}
</style>
