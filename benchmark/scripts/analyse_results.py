import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

sns.set_theme(style="whitegrid", palette="colorblind")


def save_plot(ax, plot_name: str) -> None:
    figure = ax.get_figure()
    figure.savefig(f"plots/{plot_name}.png")
    plt.close(figure)


def print_and_plot_init_duration_by_language(data: pd.DataFrame) -> None:
    cold_starts = data[data["cold_start"] == True]

    print("Cold start times per language - p50, p95, p99")
    print(
        cold_starts.groupby("name")["init_duration_ms"]
        .quantile(q=np.array([0.50, 0.95, 0.99]))
        .unstack()
    )
    print("-" * 10)

    ax = sns.histplot(x="init_duration_ms", hue="name", binwidth=20, data=data)
    ax.set_title("Cold start times by language")
    ax.set_xlabel("Init duration (ms)")
    ax.set_ylabel("Count")
    ax.set_xlim(0)
    sns.despine()
    save_plot(ax, "init_duration_by_language")


def print_and_plot_run_time_by_language(data: pd.DataFrame) -> None:
    print("Execution times per language - p50, p95, p99")
    print(
        data.groupby(["name", "cold_start"])["execution_time_ms"]
        .quantile(q=np.array([0.50, 0.95, 0.99]))
        .unstack()
    )
    print("-" * 10)

    ax = sns.histplot(x="execution_time_ms", hue="name", binwidth=5, data=data)
    ax.set_title("Execution times by language")
    ax.set_xlabel("Execution time (ms)")
    ax.set_ylabel("Count")
    ax.set_xlim(0, 500)
    sns.despine()
    save_plot(ax, "run_time_by_language")


def print_total_cost_by_language(data: pd.DataFrame) -> None:
    # From August 1st 2025 AWS will charge for the INIT phase
    # https://aws.amazon.com/blogs/compute/aws-lambda-standardizes-billing-for-init-phase/
    data["total_time"] = data["execution_time_ms"] + data["init_duration_ms"]
    totals = data.groupby("name")[
        ["init_duration_ms", "execution_time_ms", "total_time"]
    ].sum()
    totals["init_percentage"] = totals["init_duration_ms"] / totals["total_time"]

    print("Total billed time by language")
    print(totals)
    print("-" * 10)


if __name__ == "__main__":
    data = pd.read_csv("../data/parsed_cloudwatch_logs.csv")
    print_and_plot_init_duration_by_language(data=data)
    print_and_plot_run_time_by_language(data=data)
    print_total_cost_by_language(data=data)
