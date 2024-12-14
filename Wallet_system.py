import os
import json
import datetime

DATA_FOLDER = "wallet_data"
DAILY_INTEREST_RATE = 0.0005  # Daily interest rate (e.g., 0.05%)

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


class WalletSystem:
    def __init__(self, wallet_id, balance, name, email, phone, password):
        self.wallet_id = wallet_id
        self.balance = balance
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.transaction_history = []
        self.total_deposits = 0
        self.daily_limit = 20000
        self.daily_transactions = 0
        self.last_transaction_date = None
        self.frozen = False
        self.loan_total = 0

    def save_to_file(self):
        filepath = os.path.join(DATA_FOLDER, f"{self.wallet_id}.json")
        data = {
            "wallet_id": self.wallet_id,
            "balance": self.balance,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "password": self.password,
            "transaction_history": self.transaction_history,
            "total_deposits": self.total_deposits,
            "daily_limit": self.daily_limit,
            "loan_total": self.loan_total,
        }
        with open(filepath, "w") as file:
            json.dump(data, file)

    @classmethod
    def load_from_file(cls, wallet_id):
        filepath = os.path.join(DATA_FOLDER, f"{wallet_id}.json")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Information file for wallet {wallet_id} not found.")
        with open(filepath, "r") as file:
            data = json.load(file)
        wallet = cls(                   #create a new instance named wallet and provide values to the instance in order
            data["wallet_id"],
            data["balance"],
            data["name"],
            data["email"],
            data["phone"],
            data["password"],
        )
        wallet.transaction_history = data["transaction_history"]
        wallet.total_deposits = data["total_deposits"]
        wallet.daily_limit = data["daily_limit"]
        wallet.loan_total = data["loan_total"]
        return wallet

    def deposit(self, amount):
        if self.frozen:
            raise Exception("Daily transactions cannot exceed $20,000. The account is frozen; please contact the bank for assistance.")
        if amount <= 0:
            raise ValueError("The deposit amount must be positive.")
        if amount > 10000:
            raise ValueError("Single deposit amount cannot exceed $10,000.")

        self._check_daily_limit(amount)
        self.balance += amount
        self.total_deposits += amount
        self._add_transaction("Deposit", amount)
        print(f"Deposited ${amount:.2f}. Current balance: ${self.balance:.2f}")
        self.save_to_file()

    def withdraw(self, amount):
        if self.frozen:
            raise Exception("The account is frozen; please contact the bank for assistance.")
        if amount <= 0:
            raise ValueError("The withdrawal amount must be positive.")
        if amount > 10000:
            raise ValueError("Single withdrawal amount cannot exceed $10,000.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")

        self._check_daily_limit(amount)
        self.balance -= amount
        self._add_transaction("Withdrawal", amount)
        print(f"Withdrew ${amount:.2f}. Current balance: ${self.balance:.2f}")
        self.save_to_file()

    def transfer(self, recipient_wallet, amount):
        if self.frozen:
            raise Exception("Daily transactions cannot exceed $20,000. The account is frozen; please contact the bank for assistance.")
        if amount <= 0:
            raise ValueError("The transfer amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")

        if amount > 5000:
            confirm = input(f"The transfer amount is ${amount:.2f}. Continue? (yes/no): ")
            if confirm.lower() != "yes":
                print("Transfer canceled.")
                return

        self._check_daily_limit(amount)
        self.balance -= amount
        recipient_wallet.balance += amount
        self._add_transaction("Transfer Out", amount, recipient_wallet.wallet_id)
        recipient_wallet._add_transaction("Transfer In", amount, self.wallet_id)
        print(f"Transferred ${amount:.2f} to wallet {recipient_wallet.wallet_id}. Current balance: ${self.balance:.2f}")
        self.save_to_file()
        recipient_wallet.save_to_file()

    def view_transaction_history(self):
        if len(self.transaction_history) == 0:
                print("No transaction history available.")
        else:
            for tx in self.transaction_history:
                if 'recipient_id' in tx and tx['recipient_id']:
                    recipient = " -> Wallet " + str(tx['recipient_id'])
                else:
                    recipient = ""
                print(tx['timestamp'] + ": " + tx['type'] + " $" + str(tx['amount']) + recipient)
        self.save_to_file()

    def update_personal_info(self):
        while True:
            print("\n====== Update Personal Information ======")
            print(f"Current Name: {self.name}")
            print(f"Current Email: {self.email}")
            print(f"Current Phone: {self.phone}")
            print("1. Update Name")
            print("2. Update Email")
            print("3. Update Phone")
            print("4. Back to Menu")
            choice = input("Please select an option (enter number): ")

            if choice == "1":
                self.name = input("Enter new name: ")
                print("Name updated!")
            elif choice == "2":
                self.email = input("Enter new email: ")
                print("Email updated!")
            elif choice == "3":
                self.phone = input("Enter new phone number: ")
                print("Phone updated!")
            elif choice == "4":
                print("Returning to personal info menu.")
                break
            else:
                print("Invalid option, please try again.")
                continue

            self.save_to_file()
            print("Updated information has been saved.")

    def loan_or_repay(self):
        if self.total_deposits < 10000:
            print("Total deposits must reach $10,000 to apply for a loan.")
            return

        if self.loan_total > 0:
            print(f"Outstanding loan amount: ${self.loan_total:.2f}.")
            repay_amount = float(input("Enter repayment amount (or 0 to skip): "))
            if repay_amount > 0:
                if repay_amount > self.loan_total:
                    repay_amount = self.loan_total
                if repay_amount > self.balance:
                    print("Insufficient balance for repayment.")
                    return
                self.loan_total -= repay_amount
                self.balance -= repay_amount
                self._add_transaction("Repayment", repay_amount)
                print(f"Repaid ${repay_amount:.2f}. Remaining loan balance: ${self.loan_total:.2f}")
                self.save_to_file()
                return

        loan_options = [
            {"Amount": 1000, "Interest Rate": 5},
            {"Amount": 5000, "Interest Rate": 4.5},
            {"Amount": 10000, "Interest Rate": 4},
            {"Amount": 20000, "Interest Rate": 3.5},
        ]
        print("Available loan amounts and interest rates:")
        for i, option in enumerate(loan_options, start=1):
            print(f"{i}. Loan Amount: ${option['Amount']}, Annual Interest Rate: {option['Interest Rate']}%")

        choice = int(input("Select a loan option (enter number): "))
        if choice < 1 or choice > len(loan_options):
            print("Invalid option.")
            return

        loan = loan_options[choice - 1]
        self.loan_total += loan["Amount"]
        self.balance += loan["Amount"]
        self._add_transaction("Loan", loan["Amount"])
        print(f"You have taken a loan of ${loan['Amount']} with an annual interest rate of {loan['Interest Rate']}%.")
        self.save_to_file()

    def add_daily_interest(self):
        self.balance += self.balance * DAILY_INTEREST_RATE
        self.save_to_file()

    def _add_transaction(self, transaction_type, amount, recipient_id=None):
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "recipient_id": recipient_id,
        }
        self.transaction_history.append(transaction)

    def _check_daily_limit(self, amount):
        today = datetime.date.today()
        if self.last_transaction_date != today:
            self.last_transaction_date = today
            self.daily_transactions = 0

        self.daily_transactions += amount
        if self.daily_transactions > self.daily_limit:
            self.frozen = True
            raise Exception("Daily transaction limit exceeded. The account is frozen.")

#    def verify_password(self, password):
#        return self.password == password


def login_or_register():
    print("========== Welcome to the Digital Wallet System ==========")
    while True:
        print("1. Login")
        print("2. Register a New Account")
        choice = input("Select an option (enter number): ")

        if choice == "1":
            wallet_id = input("Enter Wallet ID: ")
            password = input("Enter Password: ")
            try:
                wallet = WalletSystem.load_from_file(wallet_id)
                if wallet.password==password:
                    print(f"Login successful. Welcome, {wallet.name}!")
                    return wallet
                else:
                    print("Incorrect password, please try again.")
            except FileNotFoundError:
                print("Wallet ID does not exist. Please check or register a new account.")

        elif choice == "2":
            wallet_id = input("Enter a Wallet ID: ")
            if os.path.exists(os.path.join(DATA_FOLDER, f"{wallet_id}.json")):
                print("Wallet ID already exists. Please choose a different ID.")
                continue

            name = input("Enter your name: ")
            email = input("Enter your email: ")
            phone = input("Enter your phone number: ")
            password = input("Set a password: ")
            initial_balance = 0

            wallet = WalletSystem(wallet_id, initial_balance, name, email, phone, password)
            wallet.save_to_file()
            print("Registration successful! Please log in.")
            continue

        else:
            print("Invalid option, please try again.")


def wallet_menu(wallet):
    while True:
        print("\n========== Wallet System Menu ==========")
        print(f"Current Balance: ${wallet.balance:.2f}")
        print(f"Fixed Daily Interest Rate: {DAILY_INTEREST_RATE * 100:.2f}%")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Transfer")
        print("4. Loan/Repay")
        print("5. View/Update Personal Information")
        print("6. View Transaction History")
        print("7. Exit")
        choice = input("Select an option (enter number): ")

        try:
            if choice == "1":
                amount = float(input("Enter deposit amount: "))
                wallet.deposit(amount)
            elif choice == "2":
                amount = float(input("Enter withdrawal amount: "))
                wallet.withdraw(amount)
            elif choice == "3":
                recipient_id = input("Enter recipient Wallet ID: ")
                recipient_filepath = os.path.join(DATA_FOLDER, f"{recipient_id}.json")
                if not os.path.exists(recipient_filepath):
                    print("Invalid Wallet ID.")
                    continue
                amount = float(input("Enter transfer amount: "))
                recipient_wallet = WalletSystem.load_from_file(recipient_id)
                wallet.transfer(recipient_wallet, amount)
            elif choice == "4":
                wallet.loan_or_repay()
            elif choice == "5":
                print("\n====== Personal Information ======")
                print(f"Name: {wallet.name}")
                print(f"Email: {wallet.email}")
                print(f"Phone: {wallet.phone}")
                wallet.update_personal_info()
            elif choice == "6":
                wallet.view_transaction_history()
            elif choice == "7":
                print("Exiting the wallet system.")
                break
            else:
                print("Invalid option, please try again.")
        except ValueError as e:
            print(f"Input error: {e}")
        except Exception as e:
            print(f"Operation failed: {e}")



wallet = login_or_register()
if wallet:
    wallet_menu(wallet)
