#!/usr/bin/env python3
"""
Analysis script for correlations between process metrics and quality metrics.
Generates statistics, tests hypotheses, and creates visualizations.
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime

# Configuration
CSV_PATH = "data/processed/consolidated_metrics.csv"
LOG_PATTERN = "logs/processing_*.json"
REPORTS_DIR = "reports"
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")

os.makedirs(FIGURES_DIR, exist_ok=True)

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def load_data():
    """Load consolidated metrics CSV."""
    print("Loading data...")
    df = pd.read_csv(CSV_PATH)
    print(f"  Loaded {len(df)} repositories")
    print(f"  Columns: {df.columns.tolist()}")
    return df


def calculate_descriptive_stats(df):
    """Calculate descriptive statistics for all metrics."""
    print("\n" + "="*80)
    print("DESCRIPTIVE STATISTICS")
    print("="*80)
    
    # Process metrics
    process_metrics = ['cbo_avg', 'dit_avg', 'lcom_avg', 'wmc_avg', 'rfc_avg', 'loc_avg']
    
    stats_dict = {}
    for metric in process_metrics:
        if metric in df.columns:
            stats_dict[metric] = {
                'Mean': df[metric].mean(),
                'Median': df[metric].median(),
                'Std Dev': df[metric].std(),
                'Min': df[metric].min(),
                'Max': df[metric].max(),
                'Count': df[metric].count()
            }
            
            print(f"\n{metric.upper()}:")
            for stat_name, value in stats_dict[metric].items():
                print(f"  {stat_name:10s}: {value:12.2f}")
    
    return stats_dict


def calculate_correlations(df):
    """Calculate Spearman and Pearson correlations."""
    print("\n" + "="*80)
    print("CORRELATION ANALYSIS")
    print("="*80)
    
    quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_avg', 'wmc_avg', 'rfc_avg']
    process_metrics = ['loc_avg']  # LOC is the main process metric we have
    
    correlations = {}
    
    for process_metric in process_metrics:
        if process_metric in df.columns:
            print(f"\n{process_metric.upper()} (Process Metric)")
            print("-" * 80)
            
            for quality_metric in quality_metrics:
                if quality_metric in df.columns:
                    # Remove NaN values
                    mask = df[[process_metric, quality_metric]].notna().all(axis=1)
                    x = df.loc[mask, process_metric]
                    y = df.loc[mask, quality_metric]
                    
                    if len(x) > 2:
                        # Spearman correlation (for non-linear relationships)
                        spearman_r, spearman_p = stats.spearmanr(x, y)
                        
                        # Pearson correlation (for linear relationships)
                        pearson_r, pearson_p = stats.pearsonr(x, y)
                        
                        key = f"{process_metric} vs {quality_metric}"
                        correlations[key] = {
                            'spearman_r': spearman_r,
                            'spearman_p': spearman_p,
                            'pearson_r': pearson_r,
                            'pearson_p': pearson_p,
                            'n': len(x)
                        }
                        
                        print(f"\n  {quality_metric}:")
                        print(f"    Spearman: r={spearman_r:7.4f}, p-value={spearman_p:.2e} (n={len(x)})")
                        print(f"    Pearson:  r={pearson_r:7.4f}, p-value={pearson_p:.2e}")
                        
                        # Interpretation
                        if spearman_p < 0.05:
                            print(f"    *** SIGNIFICANT at α=0.05 ***")
                        if abs(spearman_r) > 0.7:
                            print(f"    *** STRONG correlation ***")
                        elif abs(spearman_r) > 0.5:
                            print(f"    *** MODERATE correlation ***")
    
    return correlations


def create_scatter_plots(df):
    """Create scatter plots for LOC vs quality metrics."""
    print("\n" + "="*80)
    print("GENERATING SCATTER PLOTS")
    print("="*80)
    
    quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_avg', 'wmc_avg', 'rfc_avg']
    process_metric = 'loc_avg'
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle(f'Correlations: {process_metric.upper()} vs Quality Metrics', 
                 fontsize=16, fontweight='bold')
    
    axes = axes.flatten()
    
    for idx, quality_metric in enumerate(quality_metrics):
        if quality_metric in df.columns:
            ax = axes[idx]
            
            # Remove outliers for better visualization
            mask = df[[process_metric, quality_metric]].notna().all(axis=1)
            x = df.loc[mask, process_metric]
            y = df.loc[mask, quality_metric]
            
            # Calculate correlation
            spearman_r, spearman_p = stats.spearmanr(x, y)
            
            # Plot scatter
            ax.scatter(x, y, alpha=0.5, s=30)
            
            # Add trend line
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            x_line = np.linspace(x.min(), x.max(), 100)
            ax.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)
            
            # Labels and title
            ax.set_xlabel(process_metric, fontsize=10)
            ax.set_ylabel(quality_metric, fontsize=10)
            ax.set_title(f'{quality_metric}\nSpearman r={spearman_r:.3f}, p={spearman_p:.2e}',
                        fontsize=11)
            ax.grid(True, alpha=0.3)
    
    # Remove empty subplot
    fig.delaxes(axes[5])
    
    plt.tight_layout()
    plot_file = os.path.join(FIGURES_DIR, "correlations_scatter.png")
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"  Saved: {plot_file}")
    plt.close()


def create_distribution_plots(df):
    """Create distribution plots for quality metrics."""
    print("\nGenerating distribution plots...")
    
    quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_avg', 'wmc_avg', 'rfc_avg']
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 8))
    fig.suptitle('Distribution of Quality Metrics Across Repositories', 
                 fontsize=16, fontweight='bold')
    
    axes = axes.flatten()
    
    for idx, metric in enumerate(quality_metrics):
        if metric in df.columns:
            ax = axes[idx]
            data = df[metric].dropna()
            
            ax.hist(data, bins=50, alpha=0.7, edgecolor='black')
            ax.axvline(data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {data.mean():.2f}')
            ax.axvline(data.median(), color='green', linestyle='--', linewidth=2, label=f'Median: {data.median():.2f}')
            
            ax.set_xlabel('Value')
            ax.set_ylabel('Frequency')
            ax.set_title(f'{metric.upper()}')
            ax.legend()
            ax.grid(True, alpha=0.3)
    
    # Remove empty subplot
    fig.delaxes(axes[5])
    
    plt.tight_layout()
    plot_file = os.path.join(FIGURES_DIR, "distributions.png")
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"  Saved: {plot_file}")
    plt.close()


def create_correlation_heatmap(df):
    """Create correlation heatmap."""
    print("\nGenerating correlation heatmap...")
    
    metrics = ['cbo_avg', 'dit_avg', 'lcom_avg', 'wmc_avg', 'rfc_avg', 'loc_avg']
    available_metrics = [m for m in metrics if m in df.columns]
    
    # Calculate Spearman correlation matrix
    corr_matrix = df[available_metrics].corr(method='spearman')
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', 
                center=0, vmin=-1, vmax=1, square=True, ax=ax,
                cbar_kws={"shrink": 0.8})
    
    ax.set_title('Spearman Correlation Matrix - Quality and Process Metrics', 
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plot_file = os.path.join(FIGURES_DIR, "correlation_heatmap.png")
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"  Saved: {plot_file}")
    plt.close()


def generate_hypothesis_test_summary(df, correlations):
    """Generate summary of hypothesis tests."""
    print("\n" + "="*80)
    print("HYPOTHESIS TEST SUMMARY")
    print("="*80)
    
    # Bonferroni correction
    alpha = 0.05
    n_tests = len(correlations)
    alpha_corrected = alpha / n_tests
    
    print(f"\nAlpha level: {alpha}")
    print(f"Number of tests: {n_tests}")
    print(f"Bonferroni-corrected alpha: {alpha_corrected:.6f}")
    
    significant = 0
    for test_name, results in correlations.items():
        if results['spearman_p'] < alpha_corrected:
            significant += 1
            print(f"\n✓ SIGNIFICANT: {test_name}")
            print(f"  Spearman r = {results['spearman_r']:.4f}, p = {results['spearman_p']:.2e}")
    
    print(f"\n{significant}/{n_tests} tests significant at Bonferroni-corrected α={alpha_corrected:.6f}")


def generate_report_section(df, correlations, stats_dict):
    """Generate summary section for the report."""
    report = []
    report.append("\n" + "="*80)
    report.append("ANALYSIS RESULTS - TO BE INSERTED IN RELATORIO_FINAL.md")
    report.append("="*80)
    
    # Descriptive Statistics
    report.append("\n## 10.1 Estatísticas Descritivas\n")
    report.append("**Métricas de Qualidade:**\n")
    report.append("| Métrica | Média | Mediana | Desvio Padrão | Min | Max |")
    report.append("|---------|-------|---------|---------------|-----|-----|")
    
    for metric in ['cbo_avg', 'dit_avg', 'lcom_avg', 'wmc_avg', 'rfc_avg']:
        if metric in df.columns:
            data = df[metric].dropna()
            report.append(f"| {metric} | {data.mean():.2f} | {data.median():.2f} | {data.std():.2f} | {data.min():.2f} | {data.max():.2f} |")
    
    # Summary statistics
    report.append("\n## Key Findings\n")
    report.append("- Total repositories analyzed: {}".format(len(df)))
    report.append("- Mean LOC per repository: {:.0f}".format(df['loc_avg'].mean() if 'loc_avg' in df.columns else 0))
    report.append("- Average CBO: {:.2f}".format(df['cbo_avg'].mean() if 'cbo_avg' in df.columns else 0))
    report.append("- Average DIT: {:.2f}".format(df['dit_avg'].mean() if 'dit_avg' in df.columns else 0))
    report.append("- Average LCOM: {:.2f}".format(df['lcom_avg'].mean() if 'lcom_avg' in df.columns else 0))
    
    return "\n".join(report)


def main():
    """Main analysis pipeline."""
    print("\n" + "="*80)
    print("LAB-02: QUALITY METRICS ANALYSIS")
    print("="*80)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if data file exists
    if not os.path.exists(CSV_PATH):
        print(f"\nERROR: Data file not found: {CSV_PATH}")
        print("Please run: python src/main.py")
        return
    
    # Load data
    df = load_data()
    
    # Descriptive statistics
    stats_dict = calculate_descriptive_stats(df)
    
    # Correlations
    correlations = calculate_correlations(df)
    
    # Create visualizations
    create_scatter_plots(df)
    create_distribution_plots(df)
    create_correlation_heatmap(df)
    
    # Hypothesis tests
    generate_hypothesis_test_summary(df, correlations)
    
    # Generate report section
    report_section = generate_report_section(df, correlations, stats_dict)
    report_file = os.path.join(REPORTS_DIR, "analysis_results.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_section)
    print(f"\n✓ Report section saved: {report_file}")
    
    # Save detailed correlations to JSON
    correlations_json = os.path.join(REPORTS_DIR, "correlations_detailed.json")
    with open(correlations_json, 'w', encoding='utf-8') as f:
        # Convert numpy types for JSON serialization
        corr_json = {}
        for k, v in correlations.items():
            corr_json[k] = {key: float(val) for key, val in v.items()}
        json.dump(corr_json, f, indent=2)
    print(f"✓ Detailed correlations saved: {correlations_json}")
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print(f"  - {os.path.join(FIGURES_DIR, 'correlations_scatter.png')}")
    print(f"  - {os.path.join(FIGURES_DIR, 'distributions.png')}")
    print(f"  - {os.path.join(FIGURES_DIR, 'correlation_heatmap.png')}")
    print(f"  - {report_file}")
    print(f"  - {correlations_json}")
    print("\nNext steps:")
    print("  1. Review generated figures in reports/figures/")
    print("  2. Copy analysis results from reports/analysis_results.txt")
    print("  3. Paste into RELATORIO_FINAL.md section 10")
    print("  4. Add interpretation and discussion in section 11")
    print("\n")


if __name__ == "__main__":
    main()
