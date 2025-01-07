import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def grow_salary(salary: float, growth_rate: float) -> float:
    return salary * (1 + growth_rate)

def calculate_payment(salary: float, repayment_rate: float, repayment_threshold: float) -> float:
    if salary < repayment_threshold:
        return 0.0
    return max((salary - repayment_threshold) * repayment_rate, 0)

def calculate_interest(current_owed: float, interest_rate: float) -> float:
    return current_owed * interest_rate
    

if __name__ == "__main__":

    # https://www.gov.uk/repaying-your-student-loan/what-you-pay
    # assumes graduated already
    # plan 2 only (2012-2022)
    # interest is calculated daily, and applied monthly
    # payments are usually made monthly
    
    this_year = datetime.now().year
    loan_length_years = 30
    repayment_threshold = 27_295

    salary = st.number_input("What's your current salary?", 27_250, 1_000_000, 86_000)
    owed = st.number_input("How much do you currently owe on your student loan (Plan 2)?", 0, 250_000, 64_000)
    first_repayment_year = st.slider("What year did you graduate?", 2012, 2022, 2020) + 1  # april after graduating
    annual_repayment_rate_perc = st.slider(f"What percentage of your salary over £{repayment_threshold:,d} do you pay towards your student loan?", 9, 30)
    monthly_repayment_rate = (annual_repayment_rate_perc / 100 + 1) ** (1 / 12) - 1
    lump_sum_payment = st.number_input(f"Lump sum payment today?", 0, owed, 0)
    owed -= lump_sum_payment

    with st.expander("Assumptions"):
        # rate at which salary grows each year
        annual_salary_growth_rate_perc = st.slider("Annual Salary Growth Rate (%)", 0, 200, 15)
        annual_salary_growth_rate = annual_salary_growth_rate_perc / 100
        
        # rate at which salary growth decays each year
        annual_salary_growth_annealing_rate_perc = st.slider("Annual Salary Growth Annealing Rate (%)", 0, 100, 90)
        annual_salary_growth_annealing_rate = annual_salary_growth_annealing_rate_perc / 100
        
        # student loan interest rate (constant for now)
        annual_interest_rate_perc = st.slider("Student Loan Interest Rate (%)", 0.1, 10.0, 4.3)
        # student_loan_interest_rate_annual = student_loan_interest_rate_perc / 100
        daily_interest_rate = (annual_interest_rate_perc / 100 + 1) ** (1 / 365.25) - 1
        
        years_paid = this_year - first_repayment_year
        years_left_to_pay = loan_length_years - years_paid

    st.write(f"Years left to pay: {years_left_to_pay}")
    st.write(f"Daily interest rate: {daily_interest_rate}")

    current_salary_growth_rate = annual_salary_growth_rate
    monthly_interest = 0

    date = datetime.today()
    
    all_years = [date]
    all_owed = [owed]
    all_salary = [salary]
    all_interest = [0]
    all_payments = [lump_sum_payment]  # assume haven't paid anything this year
    all_cumulative_paid = [0]  # assume haven't paid anything this year
    
    while True:
        if date.month == 1 and date.day == 1:
            salary = grow_salary(salary, current_salary_growth_rate)
            current_salary_growth_rate *= annual_salary_growth_annealing_rate

        interest = calculate_interest(owed, daily_interest_rate)
        monthly_interest += interest
        owed += interest
        if date.day == 1:
            payment = calculate_payment(salary, monthly_repayment_rate, repayment_threshold)
            owed -= min(payment, owed)
            all_years.append(date)
            all_owed.append(owed)
            all_interest.append(monthly_interest)
            all_payments.append(payment)
            all_salary.append(salary)
            monthly_interest = 0
        if owed <= 0:
            break
        date += timedelta(days=1)
        if date.year - first_repayment_year > 30:
        # if date.month >= 2:
            break

df = pd.DataFrame({
    "date": all_years,
    "owed": all_owed,
    "payment": all_payments,
    "interest": all_interest,
    "salary": all_salary,
})
df["date"] = pd.to_datetime(df["date"])

summary_df = df.groupby(df["date"].dt.year).agg(
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