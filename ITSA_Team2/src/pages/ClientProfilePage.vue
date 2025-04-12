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
        <div class="header-actions">
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
              <path
                d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
              ></path>
              <path
                d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"
              ></path>
            </svg>
            Edit Profile
          </button>
          <button class="btn-add" @click="viewTransactions(client.ClientID)">
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
            View Transactions
          </button>
        </div>
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
              <span
                :class="[
                  'status-badge',
                  client.Verified ? 'confirmed' : 'pending',
                ]"
              >
                {{ client.Verified ? "Verified" : "Not Verified" }}
              </span>
            </div>
          </div>
          <div
            class="info-group"
            style="display: flex; gap: 10px; margin: 10px 0"
          >
            <!-- Button to view verification documents -->
            <button
              class="btn-view"
              @click="fetchVerificationDocuments(client.ClientID)"
            >
              View Documents
            </button>
            <!-- Button to send verification -->
            <button
              class="btn-verify"
              v-if="!client.Verified"
              @click="sendVerification(client.ClientID)"
            >
              Send Verification
            </button>
            <!-- Button to verify user -->
            <button
              class="btn-verify"
              v-if="!client.Verified"
              @click="verifyUser(client.ClientID)"
            >
              Verify User
            </button>
          </div>
          <div class="info-group">
            <!-- Display list of documents if available -->
            <div
              v-if="documents.length > 0"
              style="display: flex; gap: 10px; margin: 10px 0"
            >
              <div v-for="(doc, index) in documents" :key="index">
                <button class="btn-view" @click="getPresignedUrl(doc)">
                  View {{ doc.split("/").pop() }}
                </button>
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

      <!-- Account Filter -->
      <div class="accounts-filter">
        <div class="filter-container">
          <label for="typeFilter">Filter by type:</label>
          <select id="typeFilter" v-model="accountTypeFilter">
            <option value="">All Types</option>
            <option value="Checking">Checking</option>
            <option value="Savings">Savings</option>
            <option value="Investment">Investment</option>
            <option value="Business">Business</option>
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
              <th>Currency</th>
              <th>Initial Deposit</th>
              <th>Branch ID</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="account in paginatedAccounts"
              :key="account.id"
              class="account-row"
            >
              <td>{{ account.id }}</td>
              <td>{{ account.type }}</td>
              <td>
                <span
                  :class="[
                    'status-badge',
                    account.accountStatus == 'Active' ? 'confirmed' : 'pending',
                  ]"
                >
                  {{ account.accountStatus }}
                </span>
              </td>
              <td>{{ formatDate(account.openingDate) }}</td>
              <td>{{ account.currency }}</td>
              <td>{{ formatCurrency(account.initialDeposit) }}</td>
              <td>{{ getBranchName(account.branchId) }}</td>
              <td>
                <div class="action-buttons-cell">
                  <button
                    class="btn-icon"
                    title="Edit Account"
                    @click="editAccount(account.id)"
                  >
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
                      <path
                        d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
                      ></path>
                      <path
                        d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"
                      ></path>
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

      <!-- Pagination controls -->
      <div class="pagination">
        <button
          class="btn-pagination"
          :disabled="isPreviousDisabled"
          @click="previousPage"
        >
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
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
          Previous
        </button>

        <div class="pagination-pages">
          <!-- First page button -->
          <button
            v-if="totalPages > 5 && currentPage > 3"
            @click="goToPage(1)"
            class="page-number"
          >
            1
          </button>

          <!-- Left ellipsis -->
          <span v-if="totalPages > 5 && currentPage > 3" class="page-ellipsis"
            >...</span
          >

          <!-- Page numbers -->
          <button
            v-for="page in visiblePageNumbers"
            :key="page"
            @click="goToPage(page)"
            :class="['page-number', { active: currentPage === page }]"
          >
            {{ page }}
          </button>

          <!-- Right ellipsis -->
          <span
            v-if="totalPages > 5 && currentPage < totalPages - 2"
            class="page-ellipsis"
            >...</span
          >

          <!-- Last page button -->
          <button
            v-if="totalPages > 5 && currentPage < totalPages - 2"
            @click="goToPage(totalPages)"
            class="page-number"
          >
            {{ totalPages }}
          </button>
        </div>

        <button
          class="btn-pagination"
          :disabled="isNextDisabled"
          @click="nextPage"
        >
          Next
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
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
      </div>

      <!-- Account Summary Footer -->
      <div class="account-summary">
        <div class="summary-item">
          <div class="summary-label">Total Accounts</div>
          <div class="summary-value">{{ client.bankAccounts.length }}</div>
        </div>
        <div class="summary-item">
          <div class="summary-label">Active Accounts</div>
          <div class="summary-value">
            {{ client.bankAccounts.filter((a) => a.active).length }}
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <div
      v-if="showEditProfileModal"
      class="modal-overlay"
      @click.self="closeEditModal"
    >
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
            <input
              id="editFirstName"
              v-model="editedClient.FirstName"
              type="text"
            />
          </div>

          <div class="form-group">
            <label for="editLastName">Last Name</label>
            <input
              id="editLastName"
              v-model="editedClient.LastName"
              type="text"
            />
          </div>

          <div class="form-group">
            <label for="editDateOfBirth">Date of Birth</label>
            <input
              id="editDateOfBirth"
              v-model="editedClient.DateOfBirth"
              type="date"
            />
          </div>

          <div class="form-group">
            <label for="editEmailAddress">Email Address</label>
            <input
              id="editEmailAddress"
              v-model="editedClient.EmailAddress"
              type="email"
            />
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
            <select
              v-model="client.Country"
              id="country"
              required
              @change="updatePhoneCountry"
            >
              <option value="" disabled selected>Select Country</option>
              <option
                v-for="country in countries"
                :key="country.name"
                :value="country.name"
              >
                {{ country.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="editPostalCode">Postal Code</label>
            <input
              id="editPostalCode"
              v-model="editedClient.PostalCode"
              type="text"
            />
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
            <button class="btn-save" @click="saveProfileChanges">
              Save Changes
            </button>
            <button
              class="btn-delete"
              @click="openDeletePopup('client', client)"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Bank Account Modal -->
    <div
      v-if="showEditAccountModal"
      class="modal-overlay"
      @click.self="closeAccountModal"
    >
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

          <div class="form-group" v-if="isAddingAccount">
            <label for="accountType">Account Type</label>
            <select id="accountType" v-model="editedAccount.type">
              <option value="Checking">Checking</option>
              <option value="Savings">Savings</option>
              <option value="Investment">Investment</option>
              <option value="Business">Business</option>
            </select>
          </div>

          <div class="form-group" v-if="isAddingAccount">
            <label for="initialDeposit">Initial Deposit</label>
            <input
              id="initialDeposit"
              v-model="editedAccount.initialDeposit"
              type="number"
              min="0"
              step="0.01"
            />
          </div>

          <div class="form-group" v-if="isAddingAccount">
            <label for="accountCurrency">Currency</label>
            <select id="accountCurrency" v-model="editedAccount.currency">
              <option
                v-for="currency in currencies"
                :key="currency.code"
                :value="currency.code"
              >
                {{ currency.name }}
              </option>
            </select>
          </div>

          <div class="form-group" v-if="isAddingAccount">
            <label for="branchId">Branch ID</label>
            <select id="branchId" v-model="editedAccount.branchId">
              <template v-for="branch in branches">
                <option :value="branch.branchId">
                  {{ branch.branchName }}
                </option>
              </template>
            </select>
          </div>
          <div class="form-group" v-if="!isAddingAccount">
            <label for="accountStatus">Account Status</label>
            <select id="accountStatus" v-model="editedAccount.accountStatus">
              <option value="Active">Active</option>
              <option value="Pending">Pending</option>
              <option value="Inactive">Inactive</option>
            </select>
          </div>
        </div>

        <div class="modal-footer">
          <div class="action-buttons">
            <button class="btn-cancel" @click="closeAccountModal">
              Cancel
            </button>
            <button class="btn-save" @click="saveAccountChanges">
              {{ isAddingAccount ? "Create Account" : "Save Changes" }}
            </button>
          </div>

          <div class="danger-zone" v-if="!isAddingAccount">
            <button
              class="btn-delete"
              @click="openDeletePopup('account', editedAccount)"
            >
              Delete Account
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Client/Account Delete Confirmation Popup -->
    <div
      v-if="showDeleteConfirmation"
      class="popup-overlay"
      @click.self="closePopup"
    >
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
          <p v-if="itemToDelete.ClientID">
            <strong>Client ID:</strong> {{ itemToDelete.ClientID }}
          </p>
          <p v-if="itemToDelete.FirstName || itemToDelete.LastName">
            <strong>Name:</strong>
            {{ itemToDelete.FirstName + " " + itemToDelete.LastName }}
          </p>
          <!-- If Deleting Account -->
          <p v-if="itemToDelete.id">
            <strong>ID:</strong> {{ itemToDelete.id }}
          </p>
          <p v-if="itemToDelete.type">
            <strong>Type:</strong> {{ itemToDelete.type }}
          </p>
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
import ISOcurrencies from "../currencies.json";

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

      currencies: [],

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
      accountTypeFilter: "",
      branches: "",

      // Pagination for bank accounts
      currentPage: 1,
      itemsPerPage: 5,
    };
  },
  watch: {
    // Reset page to 1 when filter changes
    accountTypeFilter() {
      this.currentPage = 1;
    },
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

    this.currencies = Object.entries(ISOcurrencies)
      .map(([code, name]) => ({
        code,
        name: `${code} - ${name}`,
      }))
      .sort((a, b) => a.code.localeCompare(b.code));
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
      return Math.ceil(this.filteredBankAccounts.length / this.itemsPerPage);
    },
    paginatedAccounts() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredBankAccounts.slice(start, end);
    },
    // Check if Previous button should be disabled
    isPreviousDisabled() {
      return this.currentPage <= 1 || !this.filteredBankAccounts.length;
    },

    isNextDisabled() {
      return (
        this.currentPage >= this.totalPages || !this.filteredBankAccounts.length
      );
    },
    // Filter bank accounts based on type filter
    filteredBankAccounts() {
      return this.client.bankAccounts.filter((account) => {
        // Filter by account type
        const matchesType =
          !this.accountTypeFilter || account.type === this.accountTypeFilter;
        return matchesType;
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
    formatCurrency(value) {
      if (value === undefined || value === null) return "N/A";

      // Convert to number if it's a string
      const numValue = typeof value === "string" ? parseFloat(value) : value;

      // Check if it's a valid number
      if (isNaN(numValue)) return "N/A";

      // Format to always have 2 decimal places
      return numValue.toFixed(2);
    },
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
    // Add this to your methods object
    getBranchName(branchId) {
      if (!branchId) return "N/A";
      if (!this.branches || !Array.isArray(this.branches)) return branchId;

      const branch = this.branches.find((b) => b.branchId === branchId);
      return branch ? branch.branchName : branchId;
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
    async loadClient() {
      // Assuming your API is set to retrieve client by ID
      axiosInstance
        .get(
          `https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/api/clients/${this.clientID}`
        )
        .then((response) => {
          if (response.data && response.data.client) {
            this.client = {
              ...response.data.client,
              bankAccounts: [],
            };
          }
          this.loadClientAccounts(this.clientID);
        })
        .catch((error) => {
          console.error("Error fetching client data:", error);
          // Ensure client has default values
          this.client = { bankAccounts: [] };
        });
    },
    async loadClientAccounts(clientId) {
      try {
        const response = await axiosInstance.get(
          `https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/manage_account/retrieve/${clientId}`
        );

        if (response.data.accounts && Array.isArray(response.data.accounts)) {
          this.client.bankAccounts = response.data.accounts.map((account) => ({
            id: account.accountId,
            type: account.accountType,
            accountStatus: account.accountStatus,
            openingDate: account.openingDate,
            initialDeposit: account.initialDeposit,
            currency: account.currency,
            branchId: account.branchId,
          }));
        } else {
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
          "https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/api/branches"
        );

        this.branches = response.data.branches;
      } catch (error) {
        console.error("Error fetching branches:", error);
        this.branches = [];
      }
    },
    // Save profile changes
    saveProfileChanges() {
      this.editedClient.PhoneNumber = this.editedClient.PhoneNumber.replace(
        /\s+/g,
        ""
      );
      this.client = { ...this.editedClient };

      // TODO: Remove with Actual Endpoint
      axiosInstance
        .put(
          `https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/api/clients/${this.clientID}`,
          this.editedClient
        )
        .then((response) => {
          // console.log("Client profile saved successfully:", response.data);
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
        .get(
          `https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/api/clients/${clientID}/documents`
        )
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
    sendVerification(clientID) {
      axiosInstance
        .post(
          `https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/api/clients/${clientID}/verify`
        )
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
        .put(
          `https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/manage_client/verify/${clientID}`)
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
          // console.log("Pre-signed URL fetched successfully:", response.data);
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
      } else if (this.itemType === "account") {
        this.deleteAccount(this.itemToDelete.id);
      }
    },
    deleteClient(clientID) {
      // console.log("Deleting client:", clientID);
      axiosInstance
        .delete(
          `https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/manage_client/delete`,
          {
            data: {
              client_id: clientID,
            },
          }
        )
        .then(() => {
          toast("Client deleted successfully!", {
            type: "success",
            autoClose: 3000,
          });
          // Redirect *after* toast has time to show (e.g. after 3s)
          setTimeout(() => {
            this.$router.push("/agent-manage-profiles");
          }, 3000);
        })
        .catch((error) => {
          console.error("Error deleting client:", error);
          if (error.response.status === 400) {
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
          this.closePopup();
        });
      // Redirect to the agent manage profiles page
      this.$router.push("/agent-manage-profiles");
    },
    // Open add/edit account modal
    openAddAccountModal() {
      this.isAddingAccount = true;
      this.editedAccount = {
        type: "Savings",
        initialDeposit: 0,
        currency: "SGD",
        branchId: "2aae4c97-16cc-11f0-b5a4-062bdcd6626f",
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

    // Save account changes
    saveAccountChanges() {
      if (this.isAddingAccount) {
        const newAccount = {
          clientId: this.clientID,
          accountType: this.editedAccount.type,
          initialDeposit: parseFloat(this.editedAccount.initialDeposit),
          currency: this.editedAccount.currency,
          branchId: this.editedAccount.branchId,
        };

        axiosInstance
          .post(
            "https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/manage_account/create",
            newAccount
          )
          .then((response) => {
            // console.log("Account created successfully:", response.data);
            toast("Account created successfully!", {
              type: "success",
              autoClose: 3000,
            });
            this.loadClientAccounts(this.clientID);
            this.closeAccountModal();
          })
          .catch((error) => {
            console.error("Error creating account:", error);
            toast(error.response.data.message, {
              type: "error",
              autoClose: 3000,
            });
          });
      } else {
        const updatedAccount = {
          accountStatus: this.editedAccount.accountStatus,
        };

        axiosInstance
          .put(
            `https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/manage_account/update/${this.editedAccount.id}`,
            updatedAccount
          )
          .then((response) => {
            // console.log("Account updated successfully:", response.data);
            toast("Account updated successfully!", {
              type: "success",
              autoClose: 3000,
            });
            this.loadClientAccounts(this.clientID);
            this.closeAccountModal();
          })
          .catch((error) => {
            console.error("Error updating account:", error);
            toast("Error updating account. Please try again.", {
              type: "error",
              autoClose: 3000,
            });
          });
      }
    },
    // Delete account
    deleteAccount(accountId) {
      axiosInstance
        .delete(
          `https://6k8nzfwxjl.execute-api.ap-southeast-1.amazonaws.com/manage_account/delete/${accountId}`
        )
        .then(() => {
          toast("Account deleted successfully!", {
            type: "success",
            autoClose: 3000,
          });
          // Refresh the accounts list
          this.loadClientAccounts(this.clientID);
          this.closePopup();
          this.closeAccountModal();
        })
        .catch((error) => {
          console.error("Error deleting account:", error);
          toast("Error deleting account. Please try again.", {
            type: "error",
            autoClose: 3000,
          });
        });
    },
    // View transactions (placeholder function - would navigate to transactions page)
    viewTransactions(clientId) {
      this.$router.push(`/agent-view-transactions/${clientId}`);
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
  font-family: "Inter", system-ui, -apple-system, sans-serif;
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
  transition: box-shadow 0.3s ease, transform 0.2s ease;
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

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
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
  padding: 8px 15px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 500;
  transition: all 0.2s ease;
  background-color: #3b82f6;
  color: white;
}

.btn-edit-profile:hover {
  background-color: #2b6cb0;
}

.btn-edit-profile svg {
  color: var(--primary-color);
}

.btn-add {
  padding: 8px 15px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 500;
  transition: all 0.2s ease;
  background-color: #3b82f6;
  color: white;
}

.btn-add:hover {
  background-color: #2b6cb0;
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
  justify-content: center;
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
  transition: background-color 0.2s, transform 0.1s;
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

/* Enhanced Mobile Responsive Styles */
@media (max-width: 768px) {
  .admin-dashboard {
    padding: 1rem;
  }

  .dashboard-header {
    padding: 1.25rem;
  }

  .dashboard-header h1 {
    font-size: 1.5rem;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .btn-edit-profile,
  .btn-add {
    width: 100%;
    justify-content: center;
  }

  .profile-content {
    flex-direction: column;
    gap: 1.5rem;
  }

  .profile-info {
    min-width: 100%;
  }

  /* Button group in mobile view */
  .info-group[style*="display: flex"] {
    flex-direction: column;
    width: 100%;
  }

  /* Documents buttons in mobile view */
  .info-group > div[style*="display: flex"] {
    flex-direction: column;
    gap: 0.5rem;
  }

  .info-group button {
    width: 100%;
    margin-bottom: 0.5rem;
  }

  .accounts-filter {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-container {
    width: 100%;
  }

  .filter-container select {
    width: 100%;
  }

  /* Table responsive styles */
  .accounts-table {
    margin: 0 -1rem;
    width: calc(100% + 2rem);
  }

  .accounts-table table {
    width: max-content;
    min-width: 100%;
  }

  .accounts-table th,
  .accounts-table td {
    padding: 0.75rem;
  }

  /* Account summary in mobile */
  .account-summary {
    flex-direction: column;
    gap: 1rem;
  }

  .summary-item {
    width: 100%;
  }

  /* Modal improvements for mobile */
  .modal {
    width: 95%;
    max-height: 85vh;
    margin: 0 0.5rem;
  }

  .modal-header {
    padding: 1rem;
  }

  .modal-content {
    padding: 1.25rem;
  }

  .modal-footer {
    padding: 1rem;
    flex-direction: column-reverse;
    gap: 1rem;
  }

  .action-buttons,
  .danger-zone {
    width: 100%;
    flex-direction: column;
    gap: 0.5rem;
  }

  .btn-delete,
  .btn-save,
  .btn-cancel {
    width: 100%;
  }

  /* Popup for mobile */
  .popup {
    width: 95%;
    max-width: none;
  }
}

/* Extra small devices */
@media (max-width: 480px) {
  .admin-dashboard {
    padding: 0.75rem;
  }

  .dashboard-header {
    padding: 1rem;
    margin-bottom: 1rem;
  }

  .dashboard-header h1 {
    font-size: 1.25rem;
  }

  .dashboard-subtitle {
    font-size: 0.875rem;
  }

  .card {
    margin-bottom: 1rem;
    border-radius: 0.75rem;
  }

  .card-header h2 {
    font-size: 1.125rem;
  }

  /* Table styles for very small screens */
  .accounts-table th:nth-child(4),
  .accounts-table th:nth-child(6),
  .accounts-table th:nth-child(7),
  .accounts-table td:nth-child(4),
  .accounts-table td:nth-child(6),
  .accounts-table td:nth-child(7) {
    display: none; /* Hide less important columns on very small screens */
  }

  .action-buttons-cell {
    flex-wrap: wrap;
  }

  /* Document buttons in XS screens */
  .btn-view,
  .btn-verify {
    padding: 8px 12px;
    font-size: 13px;
  }

  /* Improve modal scrolling on small screens */
  .modal {
    max-height: 80vh;
  }

  .modal-content {
    padding: 1rem;
  }
}

/* Improve scrolling for all tables on mobile */
@media (max-width: 768px) {
  .accounts-table::-webkit-scrollbar {
    height: 4px;
  }

  .accounts-table::-webkit-scrollbar-track {
    background: #f1f1f1;
  }

  .accounts-table::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 4px;
  }

  /* Override some of the flex styles to ensure compact mobile layout */
  .info-group > div[v-if="documents.length > 0"] {
    flex-direction: column !important;
    align-items: stretch !important;
  }

  .info-group > div[v-if="documents.length > 0"] > div {
    margin-bottom: 0.5rem;
  }

  .info-group > div[v-if="documents.length > 0"] button {
    width: 100%;
  }

  /* Make all buttons in the selected info-group stack vertically */
  .info-group[style*="display: flex; gap: 10px; margin: 10px 0"] {
    display: flex !important;
    flex-direction: column !important;
    width: 100% !important;
  }
}

/* Fix for the inline styles using !important */
@media (max-width: 768px) {
  [style*="display: flex; gap: 10px; margin: 10px 0"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;
    width: 100% !important;
    gap: 8px !important;
  }
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

.page-ellipsis {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  height: 2.25rem;
  color: #64748b;
  font-size: 1rem;
  font-weight: 500;
}
</style>
