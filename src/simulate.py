from calendar import monthrange
from datetime import datetime
from dateutil.relativedelta import relativedelta
from loan import StudentLoan
from utils import calculate_payment, grow_salary


def run_simulation(
    loan: StudentLoan,
    salary: float,
    monthly_repayment_rate: float,
    annual_salary_growth_rate: float,
    annual_salary_growth_annealing_rate: float,
    first_repayment_year: int,
    loan_length_years: int,
    repayment_threshold: float,
    lump_sum_payment_today: float,
) -> dict[str, list]:
    date = datetime.today()

    dates = [datetime.today()]
    interests = [0]
    salaries = [salary]
    payments = [lump_sum_payment_today]
    balances = [loan.pay(lump_sum_payment_today).balance]

    while (date.year <= first_repayment_year + loan_length_years) and not loan.settled:
        _, num_days_in_month = monthrange(date.year, date.month)
        date = date.replace(day=num_days_in_month)

        year = date.year
        month = date.month

        # pessimistic assumption: interest is added before payment
        monthly_interest = loan.add_monthly_interest(month, year)
        payment = calculate_payment(
            salary,
            monthly_repayment_rate,
            repayment_threshold,
            loan.balance,
        )
        loan.pay(payment)

        dates.append(date)
        interests.append(monthly_interest)
        salaries.append(salary)
        payments.append(payment)
        balances.append(loan.balance)

        if loan.settled:
            break

        if date.month == 12:
            salary = grow_salary(salary, annual_salary_growth_rate)
            annual_salary_growth_rate = max(
                annual_salary_growth_rate * annual_salary_growth_annealing_rate, 0
            )

        date += relativedelta(months=1)

    return {
        "date": dates,
        "interest": interests,
        "salary": salaries,
        "payment": payments,
        "balance": balances,
    }
