from constants import LoanConstants, SalaryConstants
import streamlit as st


def get_salary() -> float:
    return st.number_input(
        "What's your current salary?",
        SalaryConstants.MIN_SALARY,
        SalaryConstants.MAX_SALARY,
        SalaryConstants.DEFAULT_SALARY,
    )


def get_current_loan_balance() -> float:
    return st.number_input(
        "How much do you currently owe on your student loan (Plan 2)?",
        LoanConstants.MIN_OWABLE,
        LoanConstants.MAX_OWABLE,
        LoanConstants.DEFAULT_OWABLE,
    )


def get_first_repayment_year(owed: float) -> float:
    return (
        st.slider(
            "What year did you graduate?",
            LoanConstants.EARLIEST_GRADUATION_YEAR,
            LoanConstants.LATEST_GRADUATION_YEAR,
            LoanConstants.DEFAULT_GRADUATION_YEAR,
        )
        + 1
    )  # april after graduating


def get_annual_repayment_rate_perc() -> float:
    return st.slider(
        f"What percentage of your salary over £{LoanConstants.REPAYMENT_THRESHOLD:,d} do you pay towards your student loan?",
        LoanConstants.MIN_REPAYMENT_PERCENTAGE_OVER_THRESHOLD,
        LoanConstants.MAX_REPAYMENT_PERCENTAGE_OVER_THRESHOLD,
        LoanConstants.DEFAULT_REPAYMENT_PERCENTAGE_OVER_THRESHOLD,
    )


def get_lump_sum_payment_today(balance: float) -> float:
    return st.number_input(
        "Make a lump sum payment today?",
        LoanConstants.MIN_LUMP_SUM_PAYMENT_TODAY,
        balance,
        LoanConstants.DEFAULT_LUMP_SUM_PAYMENT_TODAY,
    )


def get_annual_salary_growth_rate():
    """Get the annual salary growth rate as a fraction."""
    annual_salary_growth_rate_perc = st.slider(
        "Annual Salary Growth Rate (%)",
        SalaryConstants.MIN_GROWTH_RATE_PERC,
        SalaryConstants.MAX_GROWTH_RATE_PERC,
        SalaryConstants.DEFAULT_GROWTH_RATE_PERC,
    )
    return annual_salary_growth_rate_perc / 100


def get_annual_salary_growth_annealing_rate():
    """Get the annual salary growth annealing rate as a fraction."""
    # rate at which salary growth decays each year
    annual_salary_growth_annealing_rate_perc = st.slider(
        "Annual Salary Growth Annealing Rate (%)",
        SalaryConstants.MIN_GROWTH_ANNEALING_RATE_PERC,
        SalaryConstants.MAX_GROWTH_ANNEALING_RATE_PERC,
        SalaryConstants.DEFAULT_GROWTH_ANNEALING_RATE_PERC,
    )
    return annual_salary_growth_annealing_rate_perc / 100


def get_annual_interest_rate():
    """Get the annual loan interest rate as a fraction."""
    annual_interest_rate_perc = st.slider(
        "Student Loan Interest Rate (%)",
        LoanConstants.MIN_INTEREST_RATE_PERC,
        LoanConstants.MAX_INTEREST_RATE_PERC,
        LoanConstants.DEFAULT_INTEREST_RATE_PERC,
    )
    return annual_interest_rate_perc / 100


def get_aggregation_period():
    return st.radio("Aggregate results by", ["Year", "Month"], horizontal=True)
