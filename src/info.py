import streamlit as st


def render_title() -> None:
    st.title("Student Loan Balance Forecaster")


def render_disclaimer() -> None:
    st.warning(
        """
        **Important:** This tool is provided for illustrative purposes only. It is not financial advice. 
        The calculations are based on the assumptions and constants provided and are an **estimate**. You should perform your own calculations and seek professional advice before making any financial decisions.
        The author takes no responsibility for any decisions made based on the results of this tool.
        """
    )
    st.write(
        """
        This forecasting tool is based on the UK student loan system for Plan 2 loans (2012-2022) in England. *We don't permanently store any user information entered*. For FAQs, see the sidebar on the left.
        """
    )


def render_faqs() -> None:
    with st.sidebar:
        st.title("FAQs")

        st.header("What is this tool for?")
        st.write(
            """
            I was curious if repaying more than the minimum on my student loan each month (e.g. 12\% over the repayment threshold instead of 9%), or making a lump sum payment now, would save me money in the long run. This tool is intended to (roughly!) model what would happen in each of those cases.
            """
        )

        st.header("Who is this tool for?")
        st.write(
            """
            This tool is for anyone who has already graduated, with a Plan 2 student loan in England, who wants to understand how much they might repay over time.
            """
        )

        st.header("How do I use this tool?")
        st.write(
            """
            Some basic information is required from you to make your forecast. This includes your current salary, how much you owe on your student loan, and when you graduated. None of this information is permanently stored!

            You can then play around with different ways of paying off your loan (such as the proportion of your salary you pay, and making a lump sum payment now) to see how it affects your repayments over time and the total amount that you might repay.

            More advanced assumptions about how your salary might grow over time and the interest rate on your loan can be adjusted under 'Assumptions'.
            """
        )

        st.header("How accurate are these forecasts?")
        st.write(
            """
            These forecasts are based on:
            
            1. A number of simple assumptions regarding the future (which is hard to predict!), like salary growth and interest rates.
            2. The fairly opaque information that the Student Loans Company/UK Government provides about the terms of the loans and how interest and payments are calculated.

            Some useful references for understanding how this tool works:

            - [UK Gov Info on 'Repaying your student loan'](https://www.gov.uk/repaying-your-student-loan)
            - [Student Loan Ts&Cs](https://www.gov.uk/government/publications/student-loans-a-guide-to-terms-and-conditions/student-loans-a-guide-to-terms-and-conditions-2025-to-2026#whats-this-guide-about)
            """
        )

        st.header("These results seem a bit weird to me?")
        st.write(
            """
            The way that student loans work means that the amount you end up paying in total is highly dependent on 3 main things:

            1. Your salary.
            2. The size of your loan over time.
            3. Whether or not you pay off the whole thing before the 30 year term is up.

            For example, if you have a huge salary, you'll pay off the loan quickly and pay less in total. If you never earn over the repayment threshold, you will never pay anything towards the loan. If you have a salary somewhere in the middle, you may end up paying the most because you may pay off the loan exactly at the 30 year mark (this is the worst case scenario).

            For more info, check out [Martin Lewis' video](https://www.moneysavingexpert.com/students/student-loans-decoded/)

            It's also possible that there's a bug! See below for how to report it.
        """
        )

        st.header("How are interest and payments calculated and applied?")
        st.write(
            """
            Interest is calculated daily and applied monthly. Payments are made monthly. The interest rate is fixed.
            """
        )

        st.header("What is the 'Salary Growth Annealing Rate'?")
        st.write(
            """
            This is a fancy way of saying that your salary growth rate will decrease over time. It controls the rate at which your salary will plateau. For example, if you set this to 0.9, then your salary growth rate will decrease by 10\% each year.
            """
        )

        st.header("I have an idea for a new feature or improvement/I've found a bug!")
        st.write(
            """
            Great! This tool is open source. You can find the code on [GitHub](https://github.com/jjacobgreen/student-loan-forecaster). Feel free to open an issue for or a pull request.
            """
        )
