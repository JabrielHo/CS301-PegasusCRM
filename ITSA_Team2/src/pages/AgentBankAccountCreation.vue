<template>
    <div class="create-bank-account">
      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="client-id">
            <label>Client ID</label>
            <div class="client-id-display">{{ bankAcc.clientId }}</div>
          </div>
  
          <div class="form-group">
            <label for="accountType">Account Type</label>
            <select v-model="bankAcc.accountType" id="accountType" required>
              <option value="" disabled>Select Account Type</option>
              <option v-for="type in accountTypes" :key="type.value" :value="type.value">
                {{ type.label }}
              </option>
            </select>
          </div>
  
          <div class="form-group">
            <label for="initialDeposit">Initial Deposit</label>
            <input 
              v-model="bankAcc.initialDeposit" 
              id="initialDeposit"
              type="text" 
              inputmode="numeric"
              pattern="[0-9]*\.?[0-9]*"
              placeholder="Enter initial deposit amount"
              required />
          </div>
  
          <div class="form-group">
            <label for="currency">Currency</label> 
            <select v-model="bankAcc.currency" id="currency" required>
              <option value="" disabled>Select Currency</option>
              <option v-for="curr in currencies" :key="curr.code" :value="curr.code">
                {{ curr.code }} - {{ curr.name }}
              </option>
            </select>
          </div>
  
          <div class="form-group">
            <label for="branchId">Branch ID</label>
            <select v-model="bankAcc.branchId" id="branchId" required>
              <option value="" disabled>Select Branch</option>
              <option v-for="branch in branches" :key="branch.id" :value="branch.id">
                {{ branch.id }} - {{ branch.name }}
              </option>
            </select>
          </div>
  
          <button type="submit">Create Account</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      // Accept clientId as a prop from the parent component/route
      clientId: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        bankAcc: {
          clientId: '',
          accountType: '',
          initialDeposit: '',
          currency: '',
          branchId: ''
        },
        // Placeholder arrays for dropdown data - these will be populated from services
        accountTypes: [],
        currencies: [],
        branches: []
      };
    },
    created() {
      // Set the clientId from props
      this.bankAcc.clientId = this.clientId;
      
      // Fetch data for dropdowns
      this.fetchAccountTypes();
      this.fetchCurrencies();
      this.fetchBranches();
    },
    methods: {
      fetchAccountTypes() {
        // Replace with actual API call
        // this.accountTypes = await accountService.getAccountTypes();
        
        // Example placeholder data
        this.accountTypes = [
          { value: 'savings', label: 'Savings Account' },
          { value: 'checking', label: 'Checking Account' },
          { value: 'fixed', label: 'Fixed Deposit' }
        ];
      },
      fetchCurrencies() {
        // Replace with actual API call
        // this.currencies = await currencyService.getCurrencies();
        
        // Example placeholder data
        this.currencies = [
          { code: 'USD', name: 'US Dollar' },
          { code: 'EUR', name: 'Euro' },
          { code: 'GBP', name: 'British Pound' }
        ];
      },
      fetchBranches() {
        // Replace with actual API call
        // this.branches = await branchService.getBranches();
        
        // Example placeholder data
        this.branches = [
          { id: 'B001', name: 'Downtown Branch' },
          { id: 'B002', name: 'North Side Branch' },
          { id: 'B003', name: 'East Wing Branch' }
        ];
      },
      submitForm() {
        // console.log('Creating bank account:', this.bankAcc);
        // Implement save logic here
      }
    }
  };
  </script>
  
  <style scoped>
  .create-bank-account {
    padding: 30px;
    max-width: 600px;
    margin: 0 auto;
  }
  
  .form-container {
    background-color: #fff;
    border-radius: 8px;
    padding: 25px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .form-group {
    margin-bottom: 20px;
  } 
  
  label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    color: #333;
    font-size: 0.9rem;
  }
  
  .client-id-display {
    padding: 12px;
    font-size: 1rem;
    font-weight: 500;
  }
  
  input, select {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
    transition: border-color 0.3s;
  }
  
  input:focus, select:focus {
    outline: none;
    border-color: #4a90e2;
    box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
  }
  
  button {
    padding: 10px 20px;
    background-color: #00f;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
  }
  
  button:hover {
    background-color: #0000cc;
  }
  
  @media (max-width: 600px) {
    .create-bank-account {
      padding: 15px;
    }
    
    .form-container {
      padding: 15px;
    }
    
    button {
      width: 100%;
    }
  }
  </style>