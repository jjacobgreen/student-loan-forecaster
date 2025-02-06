from calendar import monthrange
import streamlit as st
import pandas as pd
from datetime import datetime
from utils import StudentLoan
from constants import LoanConstants, SalaryConstants


def grow_salary(salary: float, growth_rate: float) -> float:
    return salary * (1 + growth_rate)


def calculate_payment(
    salary: float,
    repayment_rate: float,
    REPAYMENT_THRESHOLD: float,
    balance: float,
) -> float:
    if salary < REPAYMENT_THRESHOLD:
        return 0.0
    return min((salary - REPAYMENT_THRESHOLD) * repayment_rate, balance)


if __name__ == "__main__":
    # https://www.gov.uk/repaying-your-student-loan/what-you-pay
    # assumes graduated already
    # plan 2 only (2012-2022)
    # interest is calculated daily, and applied monthly
    # payments are usually made monthly

    THIS_YEAR = datetime.now().year

    salary = st.number_input(
        "What's your current salary?",
        SalaryConstants.MIN_SALARY,
        SalaryConstants.MAX_SALARY,
        SalaryConstants.DEFAULT_SALARY,
    )
    owed = st.number_input(
        "How much do you currently owe on your student loan (Plan 2)?",
        LoanConstants.MIN_OWABLE,
        LoanConstants.MAX_OWABLE,
        LoanConstants.DEFAULT_OWABLE,
    )
    first_repayment_year = (
        st.slider(
            "What year did you graduate?",
            LoanConstants.EARLIEST_GRADUATION_YEAR,
            LoanConstants.LATEST_GRADUATION_YEAR,
            LoanConstants.DEFAULT_GRADUATION_YEAR,
        )
        + 1
    )  # april after graduating
    annual_repayment_rate_perc = st.slider(
        f"What percentage of your salary over £{LoanConstants.REPAYMENT_THRESHOLD:,d} do you pay towards your student loan?",
        9,
        30,
    )
    monthly_repayment_rate = (annual_repayment_rate_perc / 100 + 1) ** (
        1 / 12
    ) - 1
    lump_sum_payment = st.number_input("Lump sum payment today?", 0, owed, 0)
    owed -= lump_sum_payment

    with st.expander("Assumptions"):
        # rate at which salary grows each year
        annual_salary_growth_rate_perc = st.slider(
            "Annual Salary Growth Rate (%)",
            SalaryConstants.MIN_GROWTH_RATE_PERC,
            SalaryConstants.MAX_GROWTH_RATE_PERC,
            SalaryConstants.DEFAULT_GROWTH_RATE_PERC,
        )
        annual_salary_growth_rate = annual_salary_growth_rate_perc / 100

        # rate at which salary growth decays each year
        annual_salary_growth_annealing_rate_perc = st.slider(
            "Annual Salary Growth Annealing Rate (%)",
            SalaryConstants.MIN_GROWTH_ANNEALING_RATE_PERC,
            SalaryConstants.MAX_GROWTH_ANNEALING_RATE_PERC,
            SalaryConstants.DEFAULT_GROWTH_ANNEALING_RATE_PERC,
        )
        annual_salary_growth_annealing_rate = (
            annual_salary_growth_annealing_rate_perc / 100
        )

        # student loan interest rate (constant for now)
        annual_interest_rate_perc = st.slider(
            "Student Loan Interest Rate (%)",
            LoanConstants.MIN_INTEREST_RATE_PERC,
            LoanConstants.MAX_INTEREST_RATE_PERC,
            LoanConstants.DEFAULT_INTEREST_RATE_PERC,
        )
        annual_interest_rate = annual_interest_rate_perc / 100

        years_paid = THIS_YEAR - first_repayment_year
        years_left_to_pay = LoanConstants.LOAN_LENGTH_YEARS - years_paid

    st.write(f"Years left to pay: {years_left_to_pay}")

    current_salary_growth_rate = annual_salary_growth_rate
    monthly_interest = 0

    date = datetime.today()
    year = date.year

    dates = [date]
    balances = [owed]
    salaries = [salary]
    interests = [0]
    # payments = [lump_sum_payment]  # assume haven't paid anything this year
    payments = [0]  # assume haven't paid anything this year

    loan = StudentLoan(owed, annual_interest_rate)

    while (
        year <= first_repayment_year + LoanConstants.LOAN_LENGTH_YEARS
    ) and loan.unpaid:
        for month in range(date.month, 13):
            date = datetime(year, month, monthrange(year, month)[1])
            dates.append(date)

            # pessimistic assumption: interest is added before payment
            monthly_interest = loan.add_monthly_interest(month, year)
            interests.append(monthly_interest)

            salaries.append(salary)
            payment = calculate_payment(
                salary,
                monthly_repayment_rate,
                LoanConstants.REPAYMENT_THRESHOLD,
                loan.balance,
            )
            loan.pay(payment)

            payments.append(payment)
            balances.append(loan.balance)

            if not loan.unpaid:
                break

        salary = grow_salary(salary, current_salary_growth_rate)
        current_salary_growth_rate = max(
            current_salary_growth_rate * annual_salary_growth_annealing_rate, 0
        )
        year += 1

    df = pd.DataFrame(
        {
            "date": pd.to_datetime(dates),
            "owed": balances,
            "payment": payments,
            "interest": interests,
            "salary": salaries,
        }
    )

    groupby = st.radio("Aggregate by", ["Year", "Month"], horizontal=True)
    groupby = (
        df["date"].dt.year
        if groupby == "Year"
        else df["date"].dt.to_period("M")
    )

    summary_df = df.groupby(groupby).agg(
        {
            "owed": "last",
            "payment": "sum",
            "interest": "sum",
            "salary": "last",
        }
    )
    summary_df["paid"] = summary_df["payment"].cumsum()
    st.table(summary_df)
# fig = go.Figure(
#     data=[
#         go.Candlestick(
#             x=pd.to_datetime(df["year"]),
#             open=df["owed"],
#             high=df["owed"],
#             low=df["owed"] - df["payment"],
#             close=df["owed"] - df["payment"],
#         )
#     ]
# )

# st.plotly_chart(fig)
