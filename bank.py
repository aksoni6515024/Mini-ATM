import json


class SavingsAccount(object):
    '''This class represents a Savings account
    with the owner's name, PIN, and balance.'''
    RATE = 0.02
    def __init__(self, name, pin, balance = 0.0):
        self._name = name
        self._pin = pin
        self._balance = balance
    def __str__(self):
        result =  'Name:    ' + self._name + '\n' 
        result += 'PIN:     ' + self._pin + '\n' 
        result += 'Balance: ' + str(self._balance)
        return result
    def getBalance(self):
        return self._balance
    def getName(self):
        return self._name
    def getPin(self):
        return self._pin
    def deposit(self, amount):
        '''Deposits the given amount and returns the
        new balance.'''
        self._balance += amount
        return self._balance
    def withdraw(self, amount):
        '''Withdraws the given amount.
        Returns None if successful, or an
        error message if unsuccessful.'''
        if amount < 0:
            return 'Amount must be >= 0'
        elif self._balance < amount:
            return 'Insufficient funds'
        else:
            self._balance -= amount
            return None
    def computeInterest(self):
        '''Computes, deposits, and returns the interest.'''
        interest = self._balance * SavingsAccount.RATE
        self.deposit(interest)
        return interest

class Bank(object):
    
    def __init__(self, filename = None):
        self._accounts = {}
        self._filename = filename
        if filename is not None:
            try:
                with open(filename, 'r') as file:
                    accounts = json.load(file)
            except FileNotFoundError:
                return
            for account in accounts:
                self.add(SavingsAccount(account['name'],
                                        account['pin'],
                                        account['balance']))

    def __str__(self):
        '''Return the string rep of the entire bank.'''
        return '\n'.join(map(str, self._accounts.values()))
    
    def add(self, account): 
        '''Inserts an account using its PIN as a key.'''
        self._accounts[account.getPin()] = account

    def remove(self, pin):
        return self._accounts.pop(pin, None)
    
    def get(self, pin):
        return self._accounts.get(pin, None)
    
    def computeInterest(self):
        '''Computes interest for each account and 
        returns the total.'''
        total = 0.0
        for account in self._accounts.values():
            total += account.computeInterest()
        return total

    def save(self, filename = None):
        '''Saves the accounts to a JSON data file.'''
        if filename is not None:
            self._filename = filename
        if self._filename is None:
            raise ValueError('A filename is required to save the bank')
        accounts = [
            {
                'name': account.getName(),
                'pin': account.getPin(),
                'balance': account.getBalance()
            }
            for account in self._accounts.values()
        ]
        with open(self._filename, 'w') as file:
            json.dump(accounts, file, indent=2)