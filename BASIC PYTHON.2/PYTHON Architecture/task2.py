# Create a class BankAccount with a private attribute __balance. Write a getter and setter for it using Python's @property and @balance.setter decorators. The setter should raise a ValueError if someone tries to set a negative balance
class BankAccount:
    def __init__(self, initial_balance: float = 0.0):
       self.balance = initial_balance

    @property
    def balance(self) -> float:
        """Getter for the private balance attribute."""
        return self.__balance

    @balance.setter
    def balance(self, amount: float) -> None:
        """Setter for balance with negative value check."""
        if amount < 0:
            raise ValueError("Balance cannot be negative.")
        self.__balance = amount