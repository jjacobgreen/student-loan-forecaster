import pandas as pd
import plotly.graph_objects as go


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


def get_monthly_repayment_rate(annual_repayment_rate_perc: float) -> float:
    """Convert annual repayment rate (%) to monthly repayment rate (fraction)."""
    return (annual_repayment_rate_perc / 100 + 1) ** (1 / 12) - 1


def summarise(results_df: pd.DataFrame, groupby: str) -> pd.DataFrame:
    groupby = (
        results_df["date"].dt.year
        if groupby == "Year"
        else results_df["date"].dt.to_period("M")
    )

    summary_df = results_df.groupby(groupby).agg(
        {
            "balance": "last",
            "payment": "sum",
            "interest": "sum",
            "salary": "first",
        }
    )
    summary_df["total paid to date"] = summary_df["payment"].cumsum()
    return summary_df


def plot_summary(summary_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    date = (
        summary_df.index.to_timestamp()
        if isinstance(summary_df.index, pd.PeriodIndex)
        else summary_df.index
    )
    start = summary_df["balance"] + summary_df["payment"] - summary_df["interest"]
    end = summary_df["balance"]
    diff = end - start

    bar_hovertemplate = """
        <b>Date:</b> %{x}<br>
        <b>Starting Balance:</b> £%{base:,.2f}<br>
        <b>Ending Balance:</b> £%{y:,.2f}
        <extra></extra>
    """

    line_hovertemplate = """
        <b>Total Paid to Date:</b> £%{y:,.2f}
        <extra></extra>
    """

    fig = go.Figure(
        go.Bar(
            x=date,
            y=diff,
            base=start,
            marker_color=diff.map(lambda x: "red" if x > 0 else "green"),
            hovertemplate=bar_hovertemplate,
            customdata=diff,
            name="Change in Balance",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=date,
            y=summary_df["total paid to date"],
            mode="lines",
            line=dict(color="blue", width=2),
            name="Total Paid to Date",
            hovertemplate=line_hovertemplate,
        )
    )

    fig.update_layout(
        title="Loan Balance Over Time",
        xaxis_title="Year",
        yaxis_title="Balance",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
    )
    return fig


def get_loan_outcome(results_df: pd.DataFrame) -> tuple[str, str, float]:
    pay_off_date = results_df["date"].iloc[-1]
    total_paid_to_date = results_df["payment"].sum()
    paid_off = results_df["balance"].iloc[-1] <= 0
    
    return pay_off_date, "paid" if paid_off else "written", total_paid_to_date