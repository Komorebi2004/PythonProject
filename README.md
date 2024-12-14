# PythonProject
Only the initial version was committed for now, I'll revise it later - 12.14/14:43

down the finnal version - 12.14/22:00
### 1. Basic Functions:
- **`deposit(amount)`**: Perform deposit operations.  
- **`withdraw(amount)`**: Perform withdrawal operations.  
- **`transfer(recipient_wallet, amount)`**: Transfer funds to a specified user's wallet.  
- **`view_transaction_history()`**: View the transaction history.  
- **`update_personal_info()`**: Update the user's personal information (e.g., name, email, phone).  
- **`loan_or_repay()`**: Apply for a loan or repay outstanding loan amounts.

### 2. Auxiliary Methods:
- **`_add_transaction(transaction_type, amount, recipient_id)`**: Add a transaction record.  
- **`_check_daily_limit(amount)`**: Check if the daily transaction limit is exceeded.  
- **`add_daily_interest()`**: Calculate daily interest at the specified rate.  
- **`validate_input(input_type, value)`**: Validate input formats (e.g., wallet ID, email, password).

### 3. Login and Registration Module:
- **`login_or_register()`**: Provide login and registration options.  
  - During login, check if the wallet ID exists and if the password is correct.  
  - During registration, validate the user's input format and generate a new wallet file.

### 4. User Interaction Menu:
- **`wallet_menu(wallet)`**: The main menu for wallet functionalities, including the following operations:  
  1. Deposit funds (`deposit`).  
  2. Withdraw funds (`withdraw`).  
  3. Transfer funds (`transfer`).  
  4. Apply for or repay a loan (`loan_or_repay`).  
  5. View or update personal information (`update_personal_info`).  
  6. View transaction history (`view_transaction_history`).  
  7. Exit the system.  

---

### Summary of Features:
#### **Data Storage:**
- Stable and efficient storage of wallet data.  
- All user data is saved in JSON files under the `wallet_data` folder.  
- In-memory cache (`_cache`) improves read efficiency.  

#### **Transaction Features:**
- Supports essential functions like deposits, withdrawals, and transfers.  
- Includes daily transaction limits and single transaction amount caps.  
- Have a daily compounding system

#### **Loan System:**
- Users can apply for loans based on their cumulative deposits.  
- Supports partial or full loan repayment.  

#### **Security:**
- Validates user input and enforces strict format requirements for passwords, emails, etc.  
- Accounts are frozen if daily transaction limits are exceeded.  

#### **Flexible Personal Information Management:**
- Users can update their name, email, and phone number at any time.  
