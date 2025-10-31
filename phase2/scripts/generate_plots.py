"""
Phase 2: Generate Visualizations
Creates plots for classifier comparison, confusion matrices, and defense overlap.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from matplotlib.patches import Circle


class PlotGenerator:
    """Generates visualizations for Phase 2 analysis."""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.phase2_dir = self.script_dir.parent
        self.results_dir = self.phase2_dir / "results"
        self.plots_dir = self.phase2_dir / "plots"
        self.plots_dir.mkdir(parents=True, exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 11
    
    def load_data(self):
        """Load evaluation results."""
        self.metrics = pd.read_csv(self.results_dir / "classifier_metrics.csv")
        self.ablation = pd.read_csv(self.results_dir / "ablation_detailed.csv")
        print(f"✓ Loaded metrics and ablation data")
    
    def plot_classifier_comparison(self):
        """Generate classifier comparison plot."""
        print("\n📊 Generating classifier comparison plot...")
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # TPR comparison
        ax1 = axes[0]
        versions = self.metrics['version'].tolist()
        tpr = self.metrics['tpr'].tolist()
        tpr_low = self.metrics['tpr_ci_low'].tolist()
        tpr_high = self.metrics['tpr_ci_high'].tolist()
        
        x = np.arange(len(versions))
        bars1 = ax1.bar(x, [t*100 for t in tpr], color=['#2ecc71', '#3498db', '#9b59b6'], alpha=0.8)
        
        # Error bars
        yerr_low = [(tpr[i] - tpr_low[i])*100 for i in range(len(versions))]
        yerr_high = [(tpr_high[i] - tpr[i])*100 for i in range(len(versions))]
        ax1.errorbar(x, [t*100 for t in tpr], yerr=[yerr_low, yerr_high], 
                     fmt='none', ecolor='black', capsize=5, alpha=0.6)
        
        ax1.set_xlabel('Classifier Version', fontsize=12, fontweight='bold')
        ax1.set_ylabel('TPR - Detection Rate (%)', fontsize=12, fontweight='bold')
        ax1.set_title('True Positive Rate by Classifier', fontsize=14, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(versions)
        ax1.set_ylim([0, 105])
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for i, bar in enumerate(bars1):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{tpr[i]*100:.1f}%',
                    ha='center', va='bottom', fontweight='bold')
        
        # FAR comparison
        ax2 = axes[1]
        far = self.metrics['far'].tolist()
        far_low = self.metrics['far_ci_low'].tolist()
        far_high = self.metrics['far_ci_high'].tolist()
        
        bars2 = ax2.bar(x, [f*100 for f in far], color=['#2ecc71', '#e74c3c', '#e67e22'], alpha=0.8)
        
        # Error bars
        yerr_low = [(far[i] - far_low[i])*100 for i in range(len(versions))]
        yerr_high = [(far_high[i] - far[i])*100 for i in range(len(versions))]
        ax2.errorbar(x, [f*100 for f in far], yerr=[yerr_low, yerr_high],
                     fmt='none', ecolor='black', capsize=5, alpha=0.6)
        
        ax2.set_xlabel('Classifier Version', fontsize=12, fontweight='bold')
        ax2.set_ylabel('FAR - False Alarm Rate (%)', fontsize=12, fontweight='bold')
        ax2.set_title('False Alarm Rate by Classifier', fontsize=14, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(versions)
        ax2.set_ylim([0, max([f*100 for f in far]) * 1.5 + 0.5])
        ax2.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for i, bar in enumerate(bars2):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{far[i]*100:.2f}%',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        output_file = self.plots_dir / "classifier_comparison.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {output_file}")
        plt.close()
    
    def plot_confusion_matrices(self):
        """Generate confusion matrices for each classifier."""
        print("\n📊 Generating confusion matrices...")
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        
        for idx, version in enumerate(['v1', 'v2', 'v3']):
            ax = axes[idx]
            row = self.metrics[self.metrics['version'] == version].iloc[0]
            
            # Confusion matrix
            cm = np.array([
                [row['tn'], row['fp']],
                [row['fn'], row['tp']]
            ])
            
            # Plot
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                       xticklabels=['Predicted Benign', 'Predicted Attack'],
                       yticklabels=['Actual Benign', 'Actual Attack'],
                       ax=ax, cbar=False, annot_kws={'size': 14, 'weight': 'bold'})
            
            ax.set_title(f'Classifier {version.upper()}\nF1: {row["f1"]:.4f}', 
                        fontsize=12, fontweight='bold')
            ax.set_xlabel('Predicted', fontsize=11, fontweight='bold')
            ax.set_ylabel('Actual', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        output_file = self.plots_dir / "confusion_matrices.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {output_file}")
        plt.close()
    
    def plot_defense_overlap(self):
        """Generate bar chart showing defense overlap."""
        print("\n📊 Generating defense overlap diagram...")
        
        # Count overlaps from ablation data
        attacks = self.ablation[self.ablation['is_attack'] == True]
        
        sig_only = len(attacks[attacks['caught_by_signature'] & ~attacks['caught_by_rules']])
        rules_only = len(attacks[~attacks['caught_by_signature'] & attacks['caught_by_rules']])
        both = len(attacks[attacks['caught_by_signature'] & attacks['caught_by_rules']])
        neither = len(attacks[~attacks['caught_by_signature'] & ~attacks['caught_by_rules']])
        
        total_attacks = len(attacks)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Left plot: Stacked bar chart
        categories = ['All\nAttacks']
        sig_total = sig_only + both
        rules_total = rules_only + both
        
        bars1 = ax1.barh(categories, [sig_total], color='#3498db', alpha=0.8, label='Signature Detection')
        bars2 = ax1.barh(categories, [rules_total], left=[sig_only], color='#e74c3c', alpha=0.8, label='Rules Detection')
        
        ax1.set_xlabel('Number of Attacks Detected', fontsize=12, fontweight='bold')
        ax1.set_title('Defense Coverage (Stacked)', fontsize=14, fontweight='bold')
        ax1.legend(loc='upper right', fontsize=10)
        ax1.set_xlim([0, total_attacks * 1.1])
        
        # Add value labels
        ax1.text(sig_total/2, 0, f'{sig_total}\n({sig_total/total_attacks*100:.0f}%)', 
                ha='center', va='center', fontweight='bold', fontsize=11, color='white')
        if rules_only > 0:
            ax1.text(sig_only + rules_total/2, 0, f'{rules_total}\n({rules_total/total_attacks*100:.0f}%)',
                    ha='center', va='center', fontweight='bold', fontsize=11, color='white')
        
        # Right plot: Overlap breakdown
        categories = ['Signature\nOnly', 'Rules\nOnly', 'Both', 'Neither']
        counts = [sig_only, rules_only, both, neither]
        colors = ['#3498db', '#e74c3c', '#9b59b6', '#95a5a6']
        
        bars = ax2.bar(categories, counts, color=colors, alpha=0.8)
        
        ax2.set_ylabel('Number of Attacks', fontsize=12, fontweight='bold')
        ax2.set_title('Overlap Breakdown', fontsize=14, fontweight='bold')
        ax2.set_ylim([0, max(counts) * 1.2])
        
        # Add value labels and percentages
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{count}\n({count/total_attacks*100:.0f}%)',
                    ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        # Add summary text
        coverage_sig = sig_total / total_attacks * 100
        coverage_rules = rules_total / total_attacks * 100
        coverage_combined = (sig_only + rules_only + both) / total_attacks * 100
        
        summary_text = f"""Total Attacks: {total_attacks}

Coverage:
• Signature: {coverage_sig:.1f}%
• Rules: {coverage_rules:.1f}%  
• Combined: {coverage_combined:.1f}%

Overlap: {both} ({both/total_attacks*100:.0f}%)
"""
        fig.text(0.5, 0.02, summary_text, ha='center', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout(rect=[0, 0.15, 1, 1])
        output_file = self.plots_dir / "defense_overlap.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {output_file}")
        plt.close()
    
    def plot_performance_progression(self):
        """Generate line plot showing TPR/FAR progression across versions."""
        print("\n📊 Generating performance progression plot...")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        versions = self.metrics['version'].tolist()
        tpr = [t*100 for t in self.metrics['tpr'].tolist()]
        far = [f*100 for f in self.metrics['far'].tolist()]
        
        x = np.arange(len(versions))
        
        # Plot lines
        line1 = ax.plot(x, tpr, 'o-', linewidth=2, markersize=10, 
                       color='#2ecc71', label='TPR (Detection Rate)')
        line2 = ax.plot(x, far, 's-', linewidth=2, markersize=10,
                       color='#e74c3c', label='FAR (False Alarm Rate)')
        
        ax.set_xlabel('Classifier Version', fontsize=12, fontweight='bold')
        ax.set_ylabel('Rate (%)', fontsize=12, fontweight='bold')
        ax.set_title('Performance Progression: TPR vs FAR', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(versions)
        ax.legend(fontsize=11, loc='best')
        ax.grid(True, alpha=0.3)
        ax.set_ylim([-5, 105])
        
        # Add value labels
        for i, (t, f) in enumerate(zip(tpr, far)):
            ax.text(i, t + 2, f'{t:.1f}%', ha='center', fontweight='bold', color='#2ecc71')
            ax.text(i, f + 2, f'{f:.2f}%', ha='center', fontweight='bold', color='#e74c3c')
        
        plt.tight_layout()
        output_file = self.plots_dir / "performance_progression.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {output_file}")
        plt.close()
    
    def generate_all_plots(self):
        """Generate all visualizations."""
        print("\n" + "="*70)
        print("GENERATING PHASE 2 VISUALIZATIONS")
        print("="*70)
        
        self.load_data()
        self.plot_classifier_comparison()
        self.plot_confusion_matrices()
        self.plot_defense_overlap()
        self.plot_performance_progression()
        
        print("\n✅ All plots generated successfully!")
        print(f"\nPlots saved to: {self.plots_dir}")


def main():
    """Generate all plots."""
    generator = PlotGenerator()
    generator.generate_all_plots()


if __name__ == "__main__":
    main()
