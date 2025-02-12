import streamlit as st
import pandas as pd
from datetime import datetime
from info import render_title, render_disclaimer, render_faqs
from loan import StudentLoan
from inputs import (
    get_aggregation_period,
    get_salary,
    get_current_loan_balance,
    get_first_repayment_year,
    get_annual_repayment_rate_perc,
    get_lump_sum_payment_today,
    get_annual_salary_growth_rate,
    get_annual_salary_growth_annealing_rate,
    get_annual_interest_rate,
)
from simulate import run_simulation
from utils import (
    get_monthly_repayment_rate,
    plot_summary,
    summarise,
)
from constants import LoanConstants


THIS_YEAR = datetime.now().year


if __name__ == "__main__":

    st.set_page_config(
        layout="wide",
        page_icon="💸",
    )

    render_title()
    render_disclaimer()
    render_faqs()

    left_col, right_col = st.columns(2)

    with left_col:
        salary = get_salary()
        balance = get_current_loan_balance()
        first_repayment_year = get_first_repayment_year(balance)
        annual_repayment_rate_perc = get_annual_repayment_rate_perc()
        monthly_repayment_rate = get_monthly_repayment_rate(annual_repayment_rate_perc)
        lump_sum_payment_today = get_lump_sum_payment_today(balance)

        years_paid = THIS_YEAR - first_repayment_year
        years_left_to_pay = LoanConstants.LOAN_LENGTH_YEARS - years_paid

        with st.expander("Assumptions"):
            annual_salary_growth_rate = get_annual_salary_growth_rate()
            annual_salary_growth_annealing_rate = (
                get_annual_salary_growth_annealing_rate()
            )
            annual_interest_rate = get_annual_interest_rate()  # (constant for now)

        loan = StudentLoan(balance, annual_interest_rate)

        results = run_simulation(
            loan,
            salary,
            monthly_repayment_rate,
            annual_salary_growth_rate,
            annual_salary_growth_annealing_rate,
            first_repayment_year,
            years_left_to_pay,
            LoanConstants.REPAYMENT_THRESHOLD,
            lump_sum_payment_today,
        )

        df = pd.DataFrame(results)

    with right_col:
        groupby = get_aggregation_period()
        summary_df = summarise(df, groupby)

        with st.expander("Summary Table:"):
            st.table(summary_df)

        st.markdown(
            f"**Years left to pay:** {years_left_to_pay} | **Total to be paid:** £{summary_df['total paid to date'].iloc[-1]:,.2f}"
        )

        fig = plot_summary(summary_df)
        st.plotly_chart(fig, config={"displayModeBar": False})
