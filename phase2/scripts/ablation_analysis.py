"""
Phase 2: Ablation Study - Defense Complementarity Analysis
Analyzes signature-only, rules-only, and combined defenses.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from scipy import stats


def wilson_ci(successes: int, trials: int, confidence: float = 0.95) -> Tuple[float, float, float]:
    """Calculate Wilson score confidence interval for binomial proportion."""
    if trials == 0:
        return 0.0, 0.0, 0.0
    
    p = successes / trials
    z = stats.norm.ppf((1 + confidence) / 2)
    
    denominator = 1 + z**2 / trials
    center = (p + z**2 / (2 * trials)) / denominator
    margin = z * np.sqrt((p * (1 - p) + z**2 / (4 * trials)) / trials) / denominator
    
    lower = max(0.0, center - margin)
    upper = min(1.0, center + margin)
    
    return p, lower, upper


class AblationAnalyzer:
    """Performs ablation study on defense mechanisms."""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.phase2_dir = self.script_dir.parent
        self.phase1_dir = self.phase2_dir.parent / "phase1"
        
        self.results_file = self.phase1_dir / "data" / "partA_results.json"
        self.v3_detections_file = self.phase2_dir / "results" / "detections_v3.csv"
        
        self.data = None
        self.v3_detections = None
    
    def load_data(self):
        """Load Phase 1 results and v3 detections."""
        # Load Phase 1 results
        with open(self.results_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        
        # Load v3 detections
        self.v3_detections = pd.read_csv(self.v3_detections_file)
        
        print(f"✓ Loaded {len(self.data)} Phase 1 samples")
        print(f"✓ Loaded {len(self.v3_detections)} v3 detections")
    
    def perform_ablation(self) -> pd.DataFrame:
        """Perform ablation study on different defense combinations."""
        print("\n" + "="*70)
        print("ABLATION STUDY: DEFENSE COMPLEMENTARITY ANALYSIS")
        print("="*70)
        
        results = []
        
        # For each sample, determine what caught it
        for idx, sample in enumerate(self.data):
            is_injected = sample.get("is_injected", False)
            injection_success = sample.get("injection_success", False)
            success_token = sample.get("success_token", "")
            response = sample.get("response", "")
            evasion_type = sample.get("evasion_type", "")
            
            # Ground truth: successful attack
            is_attack = is_injected and injection_success
            
            # Signature detection: Check for success token in response
            caught_by_signature = False
            if success_token:
                caught_by_signature = success_token.lower() in response.lower()
            
            # Rules detection: Check v3 classifier result
            v3_row = self.v3_detections.iloc[idx]
            caught_by_rules = v3_row['detected']
            
            # Combined: Either signature or rules
            caught_by_combined = caught_by_signature or caught_by_rules
            
            results.append({
                'is_attack': is_attack,
                'evasion_type': evasion_type if is_attack else 'benign',
                'caught_by_signature': caught_by_signature,
                'caught_by_rules': caught_by_rules,
                'caught_by_combined': caught_by_combined,
            })
        
        df = pd.DataFrame(results)
        
        # Compute metrics for each defense configuration
        self._compute_defense_metrics(df)
        
        # Analyze complementarity
        self._analyze_complementarity(df)
        
        # Save results
        self._save_results(df)
        
        return df
    
    def _compute_defense_metrics(self, df: pd.DataFrame):
        """Compute metrics for each defense configuration."""
        print("\n📊 DEFENSE PERFORMANCE METRICS")
        print("-" * 70)
        
        attacks = df[df['is_attack'] == True]
        benign = df[df['is_attack'] == False]
        
        total_attacks = len(attacks)
        total_benign = len(benign)
        
        configs = {
            'Signature-Only': 'caught_by_signature',
            'Rules-Only (v3)': 'caught_by_rules',
            'Combined (Sig+Rules)': 'caught_by_combined',
        }
        
        metrics_list = []
        
        for config_name, column in configs.items():
            # True positives: attacks caught
            tp = attacks[column].sum()
            # False positives: benign samples flagged
            fp = benign[column].sum()
            # True negatives: benign samples not flagged
            tn = total_benign - fp
            # False negatives: attacks missed
            fn = total_attacks - tp
            
            # Metrics
            tpr = tp / total_attacks if total_attacks > 0 else 0.0
            far = fp / total_benign if total_benign > 0 else 0.0
            accuracy = (tp + tn) / len(df)
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            f1 = 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) > 0 else 0.0
            
            # Wilson CIs
            tpr_point, tpr_low, tpr_high = wilson_ci(tp, total_attacks)
            far_point, far_low, far_high = wilson_ci(fp, total_benign)
            
            metrics = {
                'defense': config_name,
                'tp': tp,
                'fp': fp,
                'tn': tn,
                'fn': fn,
                'tpr': tpr,
                'tpr_ci_low': tpr_low,
                'tpr_ci_high': tpr_high,
                'far': far,
                'far_ci_low': far_low,
                'far_ci_high': far_high,
                'accuracy': accuracy,
                'precision': precision,
                'f1': f1,
            }
            
            metrics_list.append(metrics)
            
            print(f"\n{config_name}:")
            print(f"  TP: {tp}, FP: {fp}, TN: {tn}, FN: {fn}")
            print(f"  TPR: {tpr:.2%} (95% CI: [{tpr_low:.2%}, {tpr_high:.2%}])")
            print(f"  FAR: {far:.2%} (95% CI: [{far_low:.2%}, {far_high:.2%}])")
            print(f"  Accuracy: {accuracy:.2%}")
            print(f"  Precision: {precision:.2%}")
            print(f"  F1: {f1:.4f}")
        
        return pd.DataFrame(metrics_list)
    
    def _analyze_complementarity(self, df: pd.DataFrame):
        """Analyze complementarity between defenses."""
        print("\n" + "="*70)
        print("COMPLEMENTARITY ANALYSIS")
        print("="*70)
        
        attacks = df[df['is_attack'] == True]
        
        # Count overlaps
        sig_only = attacks[attacks['caught_by_signature'] & ~attacks['caught_by_rules']]
        rules_only = attacks[~attacks['caught_by_signature'] & attacks['caught_by_rules']]
        both = attacks[attacks['caught_by_signature'] & attacks['caught_by_rules']]
        neither = attacks[~attacks['caught_by_signature'] & ~attacks['caught_by_rules']]
        
        print(f"\n📊 Attack Coverage (Total: {len(attacks)} attacks)")
        print(f"  Caught by BOTH: {len(both)} ({len(both)/len(attacks):.1%})")
        print(f"  Caught by Signature ONLY: {len(sig_only)} ({len(sig_only)/len(attacks):.1%})")
        print(f"  Caught by Rules ONLY: {len(rules_only)} ({len(rules_only)/len(attacks):.1%})")
        print(f"  Missed by BOTH: {len(neither)} ({len(neither)/len(attacks):.1%})")
        
        # Synergy analysis
        sig_coverage = (len(sig_only) + len(both)) / len(attacks)
        rules_coverage = (len(rules_only) + len(both)) / len(attacks)
        combined_coverage = (len(sig_only) + len(rules_only) + len(both)) / len(attacks)
        
        print(f"\n📈 Coverage Analysis:")
        print(f"  Signature coverage: {sig_coverage:.1%}")
        print(f"  Rules coverage: {rules_coverage:.1%}")
        print(f"  Combined coverage: {combined_coverage:.1%}")
        
        if combined_coverage > max(sig_coverage, rules_coverage):
            improvement = combined_coverage - max(sig_coverage, rules_coverage)
            print(f"  ✅ Synergy: +{improvement:.1%} additional coverage from combination")
        else:
            print(f"  ⚠️ No synergy: Combined doesn't exceed individual defenses")
        
        # Analyze what each defense uniquely catches
        print(f"\n🎯 Unique Contributions:")
        if len(sig_only) > 0:
            print(f"  Signature catches {len(sig_only)} attacks that rules miss")
            sig_types = sig_only['evasion_type'].value_counts()
            print(f"    Evasion types: {dict(sig_types)}")
        
        if len(rules_only) > 0:
            print(f"  Rules catch {len(rules_only)} attacks that signature misses")
            rules_types = rules_only['evasion_type'].value_counts()
            print(f"    Evasion types: {dict(rules_types)}")
        
        if len(neither) > 0:
            print(f"\n⚠️ Attacks missed by both defenses: {len(neither)}")
            neither_types = neither['evasion_type'].value_counts()
            print(f"    Evasion types: {dict(neither_types)}")
    
    def _save_results(self, df: pd.DataFrame):
        """Save ablation results."""
        results_dir = self.phase2_dir / "results"
        
        # Save detailed results
        output_file = results_dir / "ablation_detailed.csv"
        df.to_csv(output_file, index=False)
        print(f"\n✓ Saved detailed results to {output_file}")
        
        # Save summary metrics
        attacks = df[df['is_attack'] == True]
        benign = df[df['is_attack'] == False]
        
        summary = {
            'total_samples': len(df),
            'total_attacks': len(attacks),
            'total_benign': len(benign),
            'signature_tp': attacks['caught_by_signature'].sum(),
            'signature_fp': benign['caught_by_signature'].sum(),
            'rules_tp': attacks['caught_by_rules'].sum(),
            'rules_fp': benign['caught_by_rules'].sum(),
            'combined_tp': attacks['caught_by_combined'].sum(),
            'combined_fp': benign['caught_by_combined'].sum(),
        }
        
        summary_df = pd.DataFrame([summary])
        summary_file = results_dir / "ablation_summary.csv"
        summary_df.to_csv(summary_file, index=False)
        print(f"✓ Saved summary to {summary_file}")


def main():
    """Run ablation analysis."""
    analyzer = AblationAnalyzer()
    analyzer.load_data()
    df = analyzer.perform_ablation()
    
    print("\n✅ Ablation analysis complete!")


if __name__ == "__main__":
    main()
