
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style to match Pandas
sns.set_theme(style="whitegrid")

def plot_charts(pdf_rev_bud, pdf_roi_genre, pdf_pop_rating, pdf_yearly_revenue, pdf_franchise_standalone):
    """
    Wrapper function to generate all charts.
    """
    plot_revenue_vs_budget(pdf_rev_bud)
    plot_roi_by_genre(pdf_roi_genre)
    plot_popularity_vs_rating(pdf_pop_rating)
    plot_yearly_trend(pdf_yearly_revenue)
    plot_franchise_vs_standalone(pdf_franchise_standalone)


def plot_revenue_vs_budget(pdf_revenue_budget):
    """
    Generates and saves Revenue vs Budget Over Years chart (Grouped Bar).
    Data is expected to be aggregated by year.
    """
    output_dir = "plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not pdf_revenue_budget.empty:
        # Melt data for grouped bar chart
        # pdf_revenue_budget has columns: year, revenue_musd, budget_musd
        pdf_melted = pdf_revenue_budget.melt(id_vars='year', value_vars=['Total Revenue', 'Total Budget'], 
                                             var_name='Type', value_name='Amount')
        
        # Renaissance mapping for legend to match Pandas "Revenue" and "Budget"
        pdf_melted['Type'] = pdf_melted['Type'].replace({'Total Revenue': 'Revenue', 'Total Budget': 'Budget'})
        
        plt.figure(figsize=(12, 6))
        ax = sns.barplot(data=pdf_melted, x='year', y='Amount', hue='Type', palette=['#eb5d19', 'darkgray'])
        
        for container in ax.containers:
            ax.bar_label(container, fmt='%.1f', padding=3, rotation=0, fontsize=9)
            
        plt.title('Revenue vs Budget Over Years', fontsize=30, pad=20)
        plt.xlabel('Year')
        plt.ylabel('Amount (Million USD)')
        plt.legend(title='Type')
        # plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/revenue_vs_budget.png")
        plt.close()
        print(f"Saved {output_dir}/revenue_vs_budget.png")

def plot_roi_by_genre(pdf_roi_genre):
    """
    Generates and saves Average ROI by Genre chart.
    """
    output_dir = "plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not pdf_roi_genre.empty:
        plt.figure(figsize=(12, 6))
        # Using seaborn barplot for consistent coloring
        ax = sns.barplot(x=pdf_roi_genre['mean_roi'], 
                        y=pdf_roi_genre['genres'], color='#eb5d19',
                orientation='horizontal')

        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f', padding=3, rotation=0, fontsize=9)

        plt.title('Total ROI by Genre', fontsize=30, pad=20)
        plt.xlabel('Mean ROI') # Label changed to reflect what is actually calculated (Mean vs Total in title)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/roi_by_genre.png")
        plt.close()
        print(f"Saved {output_dir}/roi_by_genre.png")

def plot_popularity_vs_rating(pdf_popularity_rating):
    """
    Generates and saves Popularity vs Rating chart.
    """
    output_dir = "plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not pdf_popularity_rating.empty:
        plt.figure(figsize=(10, 6))
        # Pandas uses scatterplot with s=100
        sns.scatterplot(data=pdf_popularity_rating, x='vote_average', y='popularity', s=100, color='#eb5d19')
        plt.title('Popularity vs Vote Average', fontsize=30, pad=20)
        plt.xlabel('Vote Average')
        plt.ylabel('Popularity')
        # plt.grid(True) # Pandas didn't explicitly enable grid in provided snippet, but set style whitegrid
        plt.tight_layout()
        plt.savefig(f"{output_dir}/popularity_vs_rating.png")
        plt.close()
        print(f"Saved {output_dir}/popularity_vs_rating.png")

def plot_yearly_trend(pdf_yearly_revenue):
    """
    Generates and saves Yearly Trend in Box Office Revenue chart.
    """
    output_dir = "plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not pdf_yearly_revenue.empty:
        plt.figure(figsize=(12, 6))
        # Pandas uses lineplot
        sns.lineplot(data=pdf_yearly_revenue, x='year', y='total_revenue', marker='o', label='Total Revenue', color='#eb5d19')
        plt.title('Total Revenue by Release Year', fontsize=30, pad=20)
        plt.xlabel('Year')
        plt.ylabel('Total Revenue (Million USD)')
        plt.grid(False) # Matching Pandas snippet
        plt.tight_layout()
        plt.savefig(f"{output_dir}/yearly_trend.png")
        plt.close()
        print(f"Saved {output_dir}/yearly_trend.png")

def plot_franchise_vs_standalone(pdf_franchise_standalone):
    """
    Generates and saves Comparison of Franchise vs Standalone Movies chart.
    """
    output_dir = "plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not pdf_franchise_standalone.empty:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        plt.suptitle('Franchise vs Standalone Movies', fontsize=24, y=1.02)
        
        # Mean Revenue
        # Check column names from spark agg: mean_revenue, median_roi, etc.
        # kpi_calculations.py stats: mean_revenue, mean_budget, mean_popularity, mean_rating, median_roi
        
        sns.barplot(data=pdf_franchise_standalone, x='is_franchise', y='mean_revenue', ax=axes[0], errorbar=None, color='#eb5d19')
        axes[0].set_title('Mean Revenue: Franchise vs Standalone', fontsize=20, pad=20)
        axes[0].set_ylabel('Mean Revenue (Millions)')
        for container in axes[0].containers:
            axes[0].bar_label(container, fmt='%.1f', padding=3)

        # Median ROI
        sns.barplot(data=pdf_franchise_standalone, x='is_franchise', y='median_roi', ax=axes[1], errorbar=None, color='#eb5d19')
        axes[1].set_title('Median ROI: Franchise vs Standalone', fontsize=20, pad=20)
        for container in axes[1].containers:
            axes[1].bar_label(container, fmt='%.2f', padding=3)

        plt.tight_layout()
        plt.savefig(f"{output_dir}/franchise_vs_standalone.png")
        plt.close()
        print(f"Saved {output_dir}/franchise_vs_standalone.png")
