import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

sns.set_theme(style="whitegrid", palette="colorblind")


def save_plot(ax, plot_name: str) -> None:
    figure = ax.get_figure()
    figure.set_size_inches(8, 4.5)
    figure.savefig(f"plots/{plot_name}.svg")
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
    sns.move_legend(ax, "upper right")
    sns.despine()
    save_plot(ax, "init_duration_by_language")


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


def plot_run_time_quantiles_by_language(data: pd.DataFrame) -> None:
    quantiles = data.groupby("name")["execution_time_ms"].quantile(
        q=np.array([0.50, 0.95, 0.99])
    )
    quantiles = quantiles.reset_index()
    quantiles.columns = ["name", "quantile", "value"]
    quantiles["quantile"] = quantiles["quantile"].astype(str)
    print("Execution time quantiles by language")
    print(quantiles)
    print("-" * 10)

    ax = sns.barplot(data=quantiles, x="name", y="value", hue="quantile")
    ax.set_title("Execution times by language")
    ax.set_xlabel("Language")
    ax.set_ylabel("Execution time (ms)")
    ax.set_ylim(0, 2000)
    ax.legend(title="Quantile")
    sns.despine()
    save_plot(ax, "run_time_quantiles_by_language")


if __name__ == "__main__":
    data = pd.read_csv("../data/parsed_cloudwatch_logs.csv").fillna(0)
    print_and_plot_init_duration_by_language(data=data)
    print_total_cost_by_language(data=data)
    plot_run_time_quantiles_by_language(data=data)
