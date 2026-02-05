import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Union

def setup_style():
    """Sets up the plotting style."""
    sns.set_theme(style="whitegrid")
    plt.rcParams["figure.figsize"] = (12, 7)
    plt.rcParams["font.size"] = 10


def plot_revenue_vs_budget(df: pd.DataFrame, output_path: Union[str, Path]):
    """
    Plots Revenue vs Budget scatter plot with release year coloring.
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Filter out null values
    plot_data = df.dropna(subset=["budget_musd", "revenue_musd"])
    
    scatter = ax.scatter(
        plot_data["budget_musd"], 
        plot_data["revenue_musd"],
        c=plot_data["release_year"],
        s=plot_data["vote_count"] / 10,  # Size based on vote count
        alpha=0.6,
        cmap="viridis"
    )
    
    ax.set_title("Revenue vs Budget Trends", fontsize=14, fontweight="bold")
    ax.set_xlabel("Budget (Million USD)", fontsize=11)
    ax.set_ylabel("Revenue (Million USD)", fontsize=11)
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Release Year")
    
    plt.tight_layout()
    output_file = Path(output_path) / "revenue_vs_budget.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved plot: {output_file}")


def plot_roi_distribution_by_genre(df: pd.DataFrame, output_path: Union[str, Path]):
    """
    Plots ROI distribution by genre.
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Expand genres (pipe-separated) and create long format
    plot_data = df.dropna(subset=["roi", "genres"]).copy()
    plot_data = plot_data[plot_data["roi"] > 0]  # Filter for positive ROI
    plot_data = plot_data[plot_data["roi"] < 20]  # Cap extreme outliers for visualization
    
    # Split genres and explode
    plot_data["genre_list"] = plot_data["genres"].str.split("|")
    plot_data_expanded = plot_data.explode("genre_list")
    plot_data_expanded["genre_list"] = plot_data_expanded["genre_list"].str.strip()
    
    # Filter top genres by count
    top_genres = plot_data_expanded["genre_list"].value_counts().head(8).index
    plot_data_expanded = plot_data_expanded[plot_data_expanded["genre_list"].isin(top_genres)]
    
    sns.boxplot(data=plot_data_expanded, x="genre_list", y="roi", ax=ax, palette="Set2")
    ax.set_title("ROI Distribution by Genre", fontsize=14, fontweight="bold")
    ax.set_xlabel("Genre", fontsize=11)
    ax.set_ylabel("ROI (Revenue / Budget)", fontsize=11)
    ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    output_file = Path(output_path) / "roi_by_genre.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved plot: {output_file}")


def plot_popularity_vs_rating(df: pd.DataFrame, output_path: Union[str, Path]):
    """
    Plots Popularity vs Rating scatter plot.
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))
    
    plot_data = df.dropna(subset=["popularity", "vote_average"])
    
    scatter = ax.scatter(
        plot_data["vote_average"],
        plot_data["popularity"],
        c=plot_data["revenue_musd"],
        s=100,
        alpha=0.6,
        cmap="plasma"
    )
    
    ax.set_title("Popularity vs Critical Rating", fontsize=14, fontweight="bold")
    ax.set_xlabel("Average Rating (out of 10)", fontsize=11)
    ax.set_ylabel("Popularity Score", fontsize=11)
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Revenue (Million USD)")
    
    plt.tight_layout()
    output_file = Path(output_path) / "popularity_vs_rating.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved plot: {output_file}")


def plot_yearly_box_office_trends(df: pd.DataFrame, output_path: Union[str, Path]):
    """
    Plots average Revenue, Budget, and Profit by Year.
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(14, 7))
    
    plot_data = df.dropna(subset=["release_year", "revenue_musd", "budget_musd"])
    yearly = plot_data.groupby("release_year")[["revenue_musd", "budget_musd"]].mean().reset_index()
    yearly["profit_musd"] = yearly["revenue_musd"] - yearly["budget_musd"]
    
    ax.plot(yearly["release_year"], yearly["revenue_musd"], marker="o", linewidth=2.5, label="Avg Revenue", color="green")
    ax.plot(yearly["release_year"], yearly["budget_musd"], marker="s", linewidth=2.5, label="Avg Budget", color="red")
    ax.plot(yearly["release_year"], yearly["profit_musd"], marker="^", linewidth=2.5, label="Avg Profit", color="blue")
    
    ax.set_title("Yearly Box Office Trends", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year", fontsize=11)
    ax.set_ylabel("Amount (Million USD)", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_file = Path(output_path) / "yearly_trends.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved plot: {output_file}")


def plot_franchise_vs_standalone(df: pd.DataFrame, output_path: Union[str, Path]):
    """
    Compares Franchise vs Standalone movie performance.
    """
    setup_style()
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Classify franchise vs standalone
    plot_data = df.copy()
    plot_data["movie_type"] = plot_data["belongs_to_collection"].apply(
        lambda x: "Franchise" if pd.notna(x) else "Standalone"
    )
    
    # Remove NaN for calculations
    plot_data_clean = plot_data.dropna(subset=["revenue_musd", "budget_musd", "vote_average"])
    
    # 1. Revenue Comparison
    ax = axes[0, 0]
    revenue_data = [
        plot_data_clean[plot_data_clean["movie_type"] == "Franchise"]["revenue_musd"],
        plot_data_clean[plot_data_clean["movie_type"] == "Standalone"]["revenue_musd"]
    ]
    bp1 = ax.boxplot(revenue_data, labels=["Franchise", "Standalone"], patch_artist=True)
    for patch, color in zip(bp1['boxes'], ['lightblue', 'lightcoral']):
        patch.set_facecolor(color)
    ax.set_title("Revenue Comparison", fontsize=12, fontweight="bold")
    ax.set_ylabel("Revenue (Million USD)")
    ax.grid(True, alpha=0.3, axis='y')
    
    # 2. Budget Comparison
    ax = axes[0, 1]
    budget_data = [
        plot_data_clean[plot_data_clean["movie_type"] == "Franchise"]["budget_musd"],
        plot_data_clean[plot_data_clean["movie_type"] == "Standalone"]["budget_musd"]
    ]
    bp2 = ax.boxplot(budget_data, labels=["Franchise", "Standalone"], patch_artist=True)
    for patch, color in zip(bp2['boxes'], ['lightblue', 'lightcoral']):
        patch.set_facecolor(color)
    ax.set_title("Budget Comparison", fontsize=12, fontweight="bold")
    ax.set_ylabel("Budget (Million USD)")
    ax.grid(True, alpha=0.3, axis='y')
    
    # 3. Rating Comparison
    ax = axes[1, 0]
    rating_data = [
        plot_data_clean[plot_data_clean["movie_type"] == "Franchise"]["vote_average"],
        plot_data_clean[plot_data_clean["movie_type"] == "Standalone"]["vote_average"]
    ]
    bp3 = ax.boxplot(rating_data, labels=["Franchise", "Standalone"], patch_artist=True)
    for patch, color in zip(bp3['boxes'], ['lightblue', 'lightcoral']):
        patch.set_facecolor(color)
    ax.set_title("Rating Comparison", fontsize=12, fontweight="bold")
    ax.set_ylabel("Average Rating (out of 10)")
    ax.grid(True, alpha=0.3, axis='y')
    
    # 4. Count and Popularity
    ax = axes[1, 1]
    type_counts = plot_data["movie_type"].value_counts()
    colors = ['lightblue', 'lightcoral']
    ax.bar(type_counts.index, type_counts.values, color=colors)
    ax.set_title("Movie Count by Type", fontsize=12, fontweight="bold")
    ax.set_ylabel("Count")
    for i, v in enumerate(type_counts.values):
        ax.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
    
    plt.suptitle("Franchise vs Standalone Movie Performance", fontsize=14, fontweight="bold", y=1.00)
    plt.tight_layout()
    output_file = Path(output_path) / "franchise_vs_standalone.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved plot: {output_file}")


def plot_rating_distribution(df: pd.DataFrame, output_path: Union[str, Path]):
    """
    Plots the distribution of movie ratings.
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))
    
    plot_data = df.dropna(subset=["vote_average"])
    
    ax.hist(plot_data["vote_average"], bins=40, color="steelblue", edgecolor="black", alpha=0.7)
    ax.axvline(plot_data["vote_average"].mean(), color="red", linestyle="--", linewidth=2.5, label=f"Mean: {plot_data['vote_average'].mean():.2f}")
    ax.axvline(plot_data["vote_average"].median(), color="green", linestyle="--", linewidth=2.5, label=f"Median: {plot_data['vote_average'].median():.2f}")
    
    ax.set_title("Distribution of Movie Ratings", fontsize=14, fontweight="bold")
    ax.set_xlabel("Average Rating (out of 10)", fontsize=11)
    ax.set_ylabel("Count", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    output_file = Path(output_path) / "rating_distribution.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved plot: {output_file}")


def plot_top_directors(df: pd.DataFrame, output_path: Union[str, Path], top_n: int = 10):
    """
    Plots top directors by total revenue.
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))
    
    plot_data = df.dropna(subset=["director", "revenue_musd"])
    plot_data = plot_data[plot_data["director"] != "Unknown"]
    
    director_revenue = plot_data.groupby("director")["revenue_musd"].agg(["sum", "count"]).sort_values("sum", ascending=False).head(top_n)
    
    bars = ax.barh(range(len(director_revenue)), director_revenue["sum"], color="teal", alpha=0.7)
    ax.set_yticks(range(len(director_revenue)))
    ax.set_yticklabels(director_revenue.index)
    ax.set_title(f"Top {top_n} Directors by Total Revenue", fontsize=14, fontweight="bold")
    ax.set_xlabel("Total Revenue (Million USD)", fontsize=11)
    ax.invert_yaxis()
    
    # Add count labels
    for i, (idx, row) in enumerate(director_revenue.iterrows()):
        ax.text(row["sum"] + 5, i, f"{int(row['count'])} movies", va='center', fontsize=9)
    
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    output_file = Path(output_path) / "top_directors.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved plot: {output_file}")


def plot_genre_performance(df: pd.DataFrame, output_path: Union[str, Path]):
    """
    Plots average rating, revenue, and popularity by genre.
    """
    setup_style()
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    
    plot_data = df.dropna(subset=["genres", "vote_average", "revenue_musd", "popularity"]).copy()
    
    # Expand genres
    plot_data["genre_list"] = plot_data["genres"].str.split("|")
    plot_data_expanded = plot_data.explode("genre_list")
    plot_data_expanded["genre_list"] = plot_data_expanded["genre_list"].str.strip()
    
    # Get top genres
    top_genres = plot_data_expanded["genre_list"].value_counts().head(10).index
    genre_filtered = plot_data_expanded[plot_data_expanded["genre_list"].isin(top_genres)]
    
    # 1. Average Rating by Genre
    genre_rating = genre_filtered.groupby("genre_list")["vote_average"].mean().sort_values(ascending=False)
    axes[0].barh(range(len(genre_rating)), genre_rating.values, color="steelblue")
    axes[0].set_yticks(range(len(genre_rating)))
    axes[0].set_yticklabels(genre_rating.index)
    axes[0].set_xlabel("Average Rating")
    axes[0].set_title("Avg Rating by Genre", fontweight="bold")
    axes[0].invert_yaxis()
    axes[0].grid(True, alpha=0.3, axis='x')
    
    # 2. Average Revenue by Genre
    genre_revenue = genre_filtered.groupby("genre_list")["revenue_musd"].mean().sort_values(ascending=False)
    axes[1].barh(range(len(genre_revenue)), genre_revenue.values, color="teal")
    axes[1].set_yticks(range(len(genre_revenue)))
    axes[1].set_yticklabels(genre_revenue.index)
    axes[1].set_xlabel("Average Revenue (Million USD)")
    axes[1].set_title("Avg Revenue by Genre", fontweight="bold")
    axes[1].invert_yaxis()
    axes[1].grid(True, alpha=0.3, axis='x')
    
    # 3. Count of Movies by Genre
    genre_count = genre_filtered["genre_list"].value_counts().sort_values(ascending=False)
    axes[2].barh(range(len(genre_count)), genre_count.values, color="coral")
    axes[2].set_yticks(range(len(genre_count)))
    axes[2].set_yticklabels(genre_count.index)
    axes[2].set_xlabel("Number of Movies")
    axes[2].set_title("Movie Count by Genre", fontweight="bold")
    axes[2].invert_yaxis()
    axes[2].grid(True, alpha=0.3, axis='x')
    
    plt.suptitle("Genre Performance Analysis", fontsize=14, fontweight="bold")
    plt.tight_layout()
    output_file = Path(output_path) / "genre_performance.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved plot: {output_file}")


def create_all_visualizations(df: pd.DataFrame, output_dir: Union[str, Path]):
    """
    Creates all visualizations at once.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60)
    
    print("\n1. Creating Revenue vs Budget plot...")
    plot_revenue_vs_budget(df, output_path)
    
    print("2. Creating ROI by Genre plot...")
    plot_roi_distribution_by_genre(df, output_path)
    
    print("3. Creating Popularity vs Rating plot...")
    plot_popularity_vs_rating(df, output_path)
    
    print("4. Creating Yearly Trends plot...")
    plot_yearly_box_office_trends(df, output_path)
    
    print("5. Creating Franchise vs Standalone plot...")
    plot_franchise_vs_standalone(df, output_path)
    
    print("6. Creating Rating Distribution plot...")
    plot_rating_distribution(df, output_path)
    
    print("7. Creating Top Directors plot...")
    plot_top_directors(df, output_path)
    
    print("8. Creating Genre Performance plot...")
    plot_genre_performance(df, output_path)
    
    print("\n" + "="*60)
    print(f"All visualizations saved to: {output_path}")
    print("="*60 + "\n")
