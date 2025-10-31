"""
Phase 2: Test Classifiers on Attacks WITHOUT Success Tokens
Evaluates pattern-based detection when token detection isn't available.
"""

import json
import pandas as pd
from pathlib import Path
from prompt_injection_classifier import get_classifier
from scipy import stats
import numpy as np


def wilson_ci(successes: int, trials: int, confidence: float = 0.95):
    """Calculate Wilson score confidence interval."""
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


class TokenlessAttackEvaluator:
    """Tests classifiers on attacks without success tokens."""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.phase2_dir = self.script_dir.parent
        self.phase1_dir = self.phase2_dir.parent / "phase1"
        self.results_file = self.phase1_dir / "data" / "partA_results.json"
        
        self.data = None
    
    def load_data(self):
        """Load Phase 1 results."""
        with open(self.results_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        print(f"✓ Loaded {len(self.data)} Phase 1 samples")
    
    def analyze_failed_attacks(self):
        """Analyze attacks that failed (no success token in response)."""
        print("\n" + "="*70)
        print("ANALYSIS: ATTACKS WITHOUT SUCCESS TOKENS")
        print("="*70)
        
        # Filter for injected queries that failed
        failed_attacks = [s for s in self.data 
                         if s.get('is_injected', False) and not s.get('injection_success', False)]
        
        # Filter for successful attacks (baseline)
        successful_attacks = [s for s in self.data
                             if s.get('is_injected', False) and s.get('injection_success', False)]
        
        # Filter for benign queries
        benign = [s for s in self.data if not s.get('is_injected', False)]
        
        print(f"\n📊 Dataset Breakdown:")
        print(f"  Successful attacks (with tokens): {len(successful_attacks)}")
        print(f"  Failed attacks (without tokens): {len(failed_attacks)}")
        print(f"  Benign queries: {len(benign)}")
        
        return failed_attacks, successful_attacks, benign
    
    def evaluate_on_failed_attacks(self, failed_attacks, benign):
        """Evaluate classifiers on failed attacks (attacks without tokens)."""
        print("\n" + "="*70)
        print("EVALUATION: PATTERN-BASED DETECTION (NO TOKENS)")
        print("="*70)
        
        results = {}
        
        for version in ['v1', 'v2', 'v3']:
            print(f"\n📊 Evaluating Classifier {version}...")
            
            classifier = get_classifier(version)
            
            # Test on failed attacks
            tp = 0  # Attacks correctly detected
            fn = 0  # Attacks missed
            
            for attack in failed_attacks:
                response = attack.get('response', '')
                result = classifier.classify(response)
                
                # Since these are actual attack attempts, detection is good
                if result.is_attack:
                    tp += 1
                else:
                    fn += 1
            
            # Test on benign
            fp = 0
            tn = 0
            
            for sample in benign:
                response = sample.get('response', '')
                result = classifier.classify(response)
                
                if result.is_attack:
                    fp += 1
                else:
                    tn += 1
            
            # Calculate metrics
            total_attacks = len(failed_attacks)
            total_benign = len(benign)
            
            tpr = tp / total_attacks if total_attacks > 0 else 0.0
            far = fp / total_benign if total_benign > 0 else 0.0
            accuracy = (tp + tn) / (total_attacks + total_benign)
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            f1 = 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) > 0 else 0.0
            
            # Wilson CIs
            tpr_point, tpr_low, tpr_high = wilson_ci(tp, total_attacks)
            far_point, far_low, far_high = wilson_ci(fp, total_benign)
            
            results[version] = {
                'version': version,
                'tp': tp,
                'fp': fp,
                'tn': tn,
                'fn': fn,
                'total_attacks': total_attacks,
                'total_benign': total_benign,
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
            
            print(f"  TP: {tp}, FP: {fp}, TN: {tn}, FN: {fn}")
            print(f"  TPR: {tpr:.2%} (95% CI: [{tpr_low:.2%}, {tpr_high:.2%}])")
            print(f"  FAR: {far:.2%} (95% CI: [{far_low:.2%}, {far_high:.2%}])")
            print(f"  Accuracy: {accuracy:.2%}")
            print(f"  Precision: {precision:.2%}")
            print(f"  F1: {f1:.4f}")
        
        return results
    
    def analyze_by_evasion_type(self, failed_attacks):
        """Analyze detection by evasion type for failed attacks."""
        print("\n" + "="*70)
        print("DETECTION BY EVASION TYPE (Failed Attacks)")
        print("="*70)
        
        # Group by evasion type
        evasion_types = {}
        for attack in failed_attacks:
            ev_type = attack.get('evasion_type', 'unknown')
            if ev_type not in evasion_types:
                evasion_types[ev_type] = []
            evasion_types[ev_type].append(attack)
        
        print(f"\nEvasion Types in Failed Attacks:")
        for ev_type, attacks in evasion_types.items():
            print(f"  {ev_type}: {len(attacks)} samples")
        
        # Test v3 on each evasion type
        classifier_v3 = get_classifier('v3')
        
        print(f"\nv3 Detection Rate by Evasion Type:")
        for ev_type, attacks in sorted(evasion_types.items()):
            detected = 0
            for attack in attacks:
                response = attack.get('response', '')
                result = classifier_v3.classify(response)
                if result.is_attack:
                    detected += 1
            
            detection_rate = detected / len(attacks) if len(attacks) > 0 else 0.0
            print(f"  {ev_type}: {detection_rate:.1%} ({detected}/{len(attacks)})")
    
    def compare_with_successful_attacks(self, failed_attacks, successful_attacks):
        """Compare detection rates on failed vs successful attacks."""
        print("\n" + "="*70)
        print("COMPARISON: Failed vs Successful Attacks")
        print("="*70)
        
        classifier_v3 = get_classifier('v3')
        
        # Detection on failed attacks
        failed_detected = 0
        for attack in failed_attacks:
            response = attack.get('response', '')
            result = classifier_v3.classify(response)
            if result.is_attack:
                failed_detected += 1
        
        # Detection on successful attacks
        success_detected = 0
        for attack in successful_attacks:
            response = attack.get('response', '')
            result = classifier_v3.classify(response)
            if result.is_attack:
                success_detected += 1
        
        failed_rate = failed_detected / len(failed_attacks) if len(failed_attacks) > 0 else 0.0
        success_rate = success_detected / len(successful_attacks) if len(successful_attacks) > 0 else 0.0
        
        print(f"\nv3 Detection Rates:")
        print(f"  Failed attacks (no tokens): {failed_rate:.1%} ({failed_detected}/{len(failed_attacks)})")
        print(f"  Successful attacks (with tokens): {success_rate:.1%} ({success_detected}/{len(successful_attacks)})")
        
        print(f"\n⚠️ Key Insight:")
        if failed_rate < success_rate:
            diff = success_rate - failed_rate
            print(f"  Pattern detection drops by {diff:.1%} when success tokens aren't present!")
            print(f"  This reveals the limits of pattern-based detection.")
        else:
            print(f"  Pattern detection performs similarly with and without tokens.")
    
    def save_results(self, results):
        """Save evaluation results."""
        results_dir = self.phase2_dir / "results"
        
        # Save metrics
        df = pd.DataFrame(list(results.values()))
        output_file = results_dir / "tokenless_evaluation.csv"
        df.to_csv(output_file, index=False)
        print(f"\n✓ Saved results to {output_file}")
    
    def run_evaluation(self):
        """Run complete evaluation."""
        self.load_data()
        
        # Analyze dataset
        failed_attacks, successful_attacks, benign = self.analyze_failed_attacks()
        
        # Evaluate on failed attacks
        results = self.evaluate_on_failed_attacks(failed_attacks, benign)
        
        # Analyze by evasion type
        self.analyze_by_evasion_type(failed_attacks)
        
        # Compare with successful attacks
        self.compare_with_successful_attacks(failed_attacks, successful_attacks)
        
        # Save results
        self.save_results(results)
        
        print("\n✅ Evaluation complete!")


def main():
    """Run evaluation."""
    evaluator = TokenlessAttackEvaluator()
    evaluator.run_evaluation()


if __name__ == "__main__":
    main()
