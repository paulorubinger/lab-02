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
    """Load consolidated metrics CSV and merge with repository metadata."""
    print("Loading data...")
    
    # Load consolidated metrics
    df_metrics = pd.read_csv(CSV_PATH)
    print(f"  Loaded {len(df_metrics)} repositories from consolidated metrics")
    
    # Load repository metadata
    repos_csv = "data/raw/repositories.csv"
    if os.path.exists(repos_csv):
        df_repos = pd.read_csv(repos_csv)
        print(f"  Loaded {len(df_repos)} repositories from metadata")
        
        # Merge on repository name (extract from consolidated_metrics.csv format: owner_repo)
        # Create a temp key in consolidated_metrics for merging
        df_metrics['owner_repo'] = df_metrics['repository']
        
        # Create a temp key in repos for merging
        df_repos['owner_repo'] = df_repos['owner'] + '_' + df_repos['repository']
        
        # Merge
        df = df_metrics.merge(
            df_repos[['owner_repo', 'stars', 'releases', 'created_at']],
            on='owner_repo',
            how='left'
        )
        
        # Calculate repository age in years
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'])
            # Remove timezone info for comparison
            current_date = pd.Timestamp.now().tz_localize(None)
            df['age_years'] = (df['created_at'].dt.tz_localize(None) - current_date).dt.days / 365.25
            # Age should be positive (invert sign)
            df['age_years'] = -df['age_years']
        
        print(f"  Merged data: {len(df)} repositories with metrics and metadata")
    else:
        print(f"  WARNING: Repository metadata not found at {repos_csv}")
        print(f"  Will analyze only LOC metrics")
        df = df_metrics
    
    print(f"  Columns: {df.columns.tolist()}")
    return df


def calculate_descriptive_stats(df):
    """Calculate descriptive statistics for all metrics."""
    print("\n" + "="*80)
    print("DESCRIPTIVE STATISTICS")
    print("="*80)
    
    all_metrics = {
        'process': ['stars', 'age_years', 'releases', 'loc_avg'],
        'quality': ['cbo_avg', 'dit_avg', 'lcom_star_avg'],
    }
    
    stats_dict = {'process': {}, 'quality': {}}
    
    for group, metrics in all_metrics.items():
        print(f"\n--- {group.upper()} METRICS ---")
        for metric in metrics:
            if metric in df.columns:
                data = df[metric].dropna()
                stats_dict[group][metric] = {
                    'Mean': float(data.mean()),
                    'Median': float(data.median()),
                    'Std Dev': float(data.std()),
                    'Min': float(data.min()),
                    'Max': float(data.max()),
                    'Count': int(data.count())
                }
                
                print(f"\n{metric.upper()}:")
                for stat_name, value in stats_dict[group][metric].items():
                    print(f"  {stat_name:10s}: {value:12.2f}")
    
    return stats_dict


def calculate_correlations(df):
    """Calculate Spearman and Pearson correlations for all RQs."""
    print("\n" + "="*80)
    print("CORRELATION ANALYSIS - ALL RESEARCH QUESTIONS")
    print("="*80)
    
    quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_star_avg']
    
    # Define all process metrics (Research Questions) - in order RQ01-RQ04
    process_metrics = {
        'stars': 'RQ01 - Popularidade (Stars) vs Qualidade',
        'age_years': 'RQ02 - Maturidade (Idade em anos) vs Qualidade',
        'releases': 'RQ03 - Atividade (Releases) vs Qualidade',
        'loc_avg': 'RQ04 - Tamanho (LOC) vs Qualidade'
    }
    
    correlations = {}
    
    for process_metric, rq_name in process_metrics.items():
        if process_metric not in df.columns:
            print(f"\n⚠️  {rq_name}")
            print(f"   {process_metric} not available in data")
            continue
            
        print(f"\n{rq_name}")
        print("-" * 80)
        
        for quality_metric in quality_metrics:
            if quality_metric not in df.columns:
                continue
            
            # Remove NaN values
            mask = df[[process_metric, quality_metric]].notna().all(axis=1)
            x = df.loc[mask, process_metric].astype(float)
            y = df.loc[mask, quality_metric].astype(float)
            
            if len(x) > 2:
                # Spearman correlation (for non-linear relationships)
                spearman_r, spearman_p = stats.spearmanr(x, y)
                
                # Pearson correlation (for linear relationships)
                pearson_r, pearson_p = stats.pearsonr(x, y)
                
                key = f"{process_metric} vs {quality_metric}"
                correlations[key] = {
                    'rq_name': rq_name,
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
                    print(f"    *** SIGNIFICANT at alpha=0.05 ***")
                if abs(spearman_r) > 0.7:
                    print(f"    *** STRONG correlation (|r| > 0.7) ***")
                elif abs(spearman_r) > 0.5:
                    print(f"    *** MODERATE correlation (|r| > 0.5) ***")
                elif abs(spearman_r) > 0.3:
                    print(f"    *** WEAK correlation (|r| > 0.3) ***")
    
    return correlations


def create_scatter_plots(df):
    """Create scatter plot subsets for each RQ."""
    print("\n" + "="*80)
    print("GENERATING SCATTER PLOTS FOR ALL RQs")
    print("="*80)
    
    quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_star_avg']
    
    # Process metrics by RQ - in order RQ01-RQ04
    rqs = {
        'stars': ('RQ01 - Popularidade (Stars)', 'Stars'),
        'age_years': ('RQ02 - Maturidade (Anos)', 'Age (years)'),
        'releases': ('RQ03 - Atividade (Releases)', 'Releases'),
        'loc_avg': ('RQ04 - Tamanho (LOC)', 'LOC (Lines of Code)')
    }
    
    for process_metric, (rq_title, metric_label) in rqs.items():
        if process_metric not in df.columns:
            print(f"\n⚠️  Skipping {rq_title} - {process_metric} not available")
            continue
        
        print(f"\nGenerating plots for {rq_title}...")
        
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        fig.suptitle(f'{rq_title} vs Quality Metrics', 
                     fontsize=14, fontweight='bold')
        
        for idx, quality_metric in enumerate(quality_metrics):
            if quality_metric not in df.columns:
                axes[idx].axis('off')
                continue
            
            ax = axes[idx]
            
            # Remove NaN values
            mask = df[[process_metric, quality_metric]].notna().all(axis=1)
            x = df.loc[mask, process_metric].astype(float)
            y = df.loc[mask, quality_metric].astype(float)
            
            # Calculate correlation
            if len(x) > 2:
                spearman_r, spearman_p = stats.spearmanr(x, y)
                
                # Plot scatter
                ax.scatter(x, y, alpha=0.5, s=30)
                
                # Add trend line
                z = np.polyfit(x, y, 1)
                p = np.poly1d(z)
                x_line = np.linspace(x.min(), x.max(), 100)
                ax.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)
                
                # Labels and title
                ax.set_xlabel(metric_label, fontsize=9)
                ax.set_ylabel(quality_metric, fontsize=9)
                
                # Color code by significance
                if spearman_p < 0.05:
                    sig_marker = " [SIG]"
                else:
                    sig_marker = ""
                
                ax.set_title(f'{quality_metric}\nr={spearman_r:.3f}, p={spearman_p:.2e}{sig_marker}',
                            fontsize=10)
                ax.grid(True, alpha=0.3)
            else:
                ax.text(0.5, 0.5, 'Insufficient\ndata', ha='center', va='center')
                ax.axis('off')
        
        plt.tight_layout()
        
        # Safe filename
        safe_metric = process_metric.replace('_', '')
        rq_code = rq_title.split(' ')[0]
        plot_file = os.path.join(FIGURES_DIR, f"scatter_{safe_metric}_{rq_code}.png")
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        print(f"  Saved: {plot_file}")
        plt.close()


def create_distribution_plots(df):
    """Create distribution plots for quality metrics."""
    print("\nGenerating distribution plots...")
    
    quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_star_avg']
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
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
    
    plt.tight_layout()
    plot_file = os.path.join(FIGURES_DIR, "distributions.png")
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"  Saved: {plot_file}")
    plt.close()


def create_correlation_heatmap(df):
    """Create correlation heatmap for all process and quality metrics."""
    print("\nGenerating correlation heatmap...")
    
    # All available metrics
    all_metrics = ['cbo_avg', 'dit_avg', 'lcom_star_avg', 'loc_avg', 'stars', 'age_years', 'releases']
    available_metrics = [m for m in all_metrics if m in df.columns]
    
    if len(available_metrics) < 2:
        print("  Not enough metrics for heatmap")
        return
    
    # Calculate Spearman correlation matrix
    corr_matrix = df[available_metrics].corr(method='spearman')
    
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', 
                center=0, vmin=-1, vmax=1, square=True, ax=ax,
                cbar_kws={"shrink": 0.8})
    
    ax.set_title('Spearman Correlation Matrix - All Process and Quality Metrics', 
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plot_file = os.path.join(FIGURES_DIR, "correlation_heatmap.png")
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"  Saved: {plot_file}")
    plt.close()


def generate_hypothesis_test_summary(df, correlations):
    """Generate summary of hypothesis tests grouped by RQ."""
    print("\n" + "="*80)
    print("HYPOTHESIS TEST SUMMARY - BY RESEARCH QUESTION")
    print("="*80)
    
    # Bonferroni correction: 4 RQs × 5 quality metrics = 20 tests
    alpha = 0.05
    n_tests = len(correlations)
    alpha_corrected = alpha / n_tests
    
    print(f"\nAlpha level: {alpha}")
    print(f"Number of tests: {n_tests}")
    print(f"Bonferroni-corrected alpha: {alpha_corrected:.6f}")
    
    # Group by RQ
    rqs_dict = {}
    for test_name, results in correlations.items():
        rq_name = results.get('rq_name', 'Unknown')
        if rq_name not in rqs_dict:
            rqs_dict[rq_name] = []
        rqs_dict[rq_name].append((test_name, results))
    
    # Print results by RQ
    rq_order = [
        'RQ01 - Popularidade (Stars) vs Qualidade',
        'RQ02 - Maturidade (Idade em anos) vs Qualidade',
        'RQ03 - Atividade (Releases) vs Qualidade',
        'RQ04 - Tamanho (LOC) vs Qualidade'
    ]
    
    total_significant = 0
    for rq_name in rq_order:
        if rq_name not in rqs_dict:
            continue
            
        print(f"\n{rq_name}")
        print("-" * 80)
        
        rq_significant = 0
        for test_name, results in sorted(rqs_dict[rq_name]):
            # Extract quality metric from test name
            quality_metric = test_name.split(' vs ')[1]
            
            sig_marker = ""
            if results['spearman_p'] < alpha_corrected:
                sig_marker = " [SIG] SIGNIFICANT"
                rq_significant += 1
                total_significant += 1
            
            print(f"  {quality_metric:12s}: r={results['spearman_r']:7.4f}, p={results['spearman_p']:.2e}{sig_marker}")
        
        print(f"  -> {rq_significant} significant results in {rq_name}")
    
    print(f"\n{'='*80}")
    print(f"TOTAL: {total_significant}/{n_tests} tests significant at Bonferroni-corrected alpha={alpha_corrected:.6f}")


def generate_report_section(df, correlations, stats_dict):
    """Generate summary section for the report."""
    report = []
    report.append("\n" + "="*80)
    report.append("ANALYSIS RESULTS - TO BE INSERTED IN RELATORIO_FINAL.md")
    report.append("="*80)
    
    n = len(df)
    report.append(f"\n## 9.1 Estatísticas Descritivas\n")
    report.append(f"**Métricas de Processo (n = {n}):**\n")
    report.append("| Métrica | Média | Mediana | Desvio Padrão | Min | Max |")
    report.append("|---------|-------|---------|---------------|-----|-----|")
    
    process_labels = {
        'stars': 'Stars',
        'age_years': 'Idade (anos)',
        'releases': 'Releases',
        'loc_avg': 'LOC_avg',
    }
    for metric, label in process_labels.items():
        s = stats_dict.get('process', {}).get(metric)
        if s:
            report.append(f"| {label} | {s['Mean']:.2f} | {s['Median']:.2f} | {s['Std Dev']:.2f} | {s['Min']:.2f} | {s['Max']:.2f} |")
    
    report.append(f"\n**Métricas de Qualidade (n = {n}):**\n")
    report.append("| Métrica | Média | Mediana | Desvio Padrão | Min | Max |")
    report.append("|---------|-------|---------|---------------|-----|-----|")
    
    quality_labels = {
        'cbo_avg': 'CBO_avg',
        'dit_avg': 'DIT_avg',
        'lcom_star_avg': 'LCOM*_avg',
    }
    for metric, label in quality_labels.items():
        s = stats_dict.get('quality', {}).get(metric)
        if s:
            report.append(f"| {label} | {s['Mean']:.2f} | {s['Median']:.2f} | {s['Std Dev']:.2f} | {s['Min']:.2f} | {s['Max']:.2f} |")
    
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
    print(f"\n[OK] Report section saved: {report_file}")
    
    # Save descriptive stats to JSON
    stats_json = os.path.join(REPORTS_DIR, "descriptive_stats.json")
    with open(stats_json, 'w', encoding='utf-8') as f:
        json.dump(stats_dict, f, indent=2, ensure_ascii=False)
    print(f"[OK] Descriptive stats saved: {stats_json}")
    
    # Save detailed correlations to JSON
    correlations_json = os.path.join(REPORTS_DIR, "correlations_detailed.json")
    with open(correlations_json, 'w', encoding='utf-8') as f:
        # Convert numpy types for JSON serialization
        corr_json = {}
        for k, v in correlations.items():
            corr_json[k] = {key: float(val) if key != 'rq_name' else val 
                           for key, val in v.items()}
        json.dump(corr_json, f, indent=2)
    print(f"[OK] Detailed correlations saved: {correlations_json}")
    
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
