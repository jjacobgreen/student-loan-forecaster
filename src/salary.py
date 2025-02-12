from calendar import monthrange


class StudentLoan:
    def __init__(self, balance: float, annual_interest_rate: float):
        if not 0 < annual_interest_rate < 1:
            raise ValueError("Interest rate must be between 0 and 1")
        if balance < 0:
            raise ValueError("Initial alance must be positive")

        self.balance = balance
        self.annual_interest_rate = annual_interest_rate
        self.daily_interest_rate = (annual_interest_rate + 1) ** (1 / 365.25) - 1

    def add_monthly_interest(self, month: int, year: int) -> float:
        _, num_days_in_month = monthrange(year, month)
        monthly_interest = sum(
            self.calculate_daily_interest() for _ in range(num_days_in_month)
        )
        self.balance += monthly_interest
        return monthly_interest

    def calculate_daily_interest(self) -> float:
        interest = self.balance * self.daily_interest_rate
        return interest

    def pay(self, amount: float):
        if amount < 0:
            raise ValueError("Payment amount must be positive")
        self.balance -= amount

    @property
    def unpaid(self) -> float:
        return self.balance > 0
