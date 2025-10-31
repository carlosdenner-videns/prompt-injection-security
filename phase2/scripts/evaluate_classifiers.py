"""
Phase 2: Evaluate Classifier Versions Against Phase 1 Dataset
Runs v1, v2, v3 classifiers on Phase 1 data and computes metrics.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from prompt_injection_classifier import get_classifier, ClassificationResult
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


class ClassifierEvaluator:
    """Evaluates classifiers on Phase 1 dataset."""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.phase2_dir = self.script_dir.parent
        self.phase1_dir = self.phase2_dir.parent / "phase1"
        self.results_file = self.phase1_dir / "data" / "partA_results.json"
        self.data = None
        self.results = {}
    
    def load_phase1_data(self):
        """Load Phase 1 results."""
        if not self.results_file.exists():
            raise FileNotFoundError(f"Phase 1 results not found: {self.results_file}")
        
        with open(self.results_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        
        print(f"✓ Loaded {len(self.data)} Phase 1 samples")
    
    def evaluate_classifier(self, version: str) -> Dict:
        """Evaluate a single classifier version."""
        print(f"\n📊 Evaluating Classifier {version}...")
        
        classifier = get_classifier(version)
        
        # Track metrics
        tp = 0  # True positives (attacks correctly detected)
        fp = 0  # False positives (benign incorrectly flagged)
        tn = 0  # True negatives (benign correctly passed)
        fn = 0  # False negatives (attacks missed)
        
        detections = []
        
        for sample in self.data:
            query = sample.get("query", "")
            response = sample.get("response", "")
            is_injected = sample.get("is_injected", False)
            injection_success = sample.get("injection_success", False)
            success_token = sample.get("success_token", "")
            
            # Classify the response (which shows if injection succeeded)
            # Also check for success token in response
            result = classifier.classify(response)
            
            # Ground truth: is_injected AND injection_success means attack succeeded
            is_attack_ground_truth = is_injected and injection_success
            
            # Update metrics
            if is_attack_ground_truth:
                # This is an attack that succeeded
                if result.is_attack:
                    tp += 1
                else:
                    fn += 1
            else:
                # This is benign or failed attack
                if result.is_attack:
                    fp += 1
                else:
                    tn += 1
            
            detections.append({
                "query": query,
                "is_injected": is_injected,
                "injection_success": injection_success,
                "detected": result.is_attack,
                "confidence": result.confidence,
                "matched_patterns": result.matched_patterns,
            })
        
        # Compute metrics
        total_attacks = tp + fn
        total_benign = tn + fp
        total = len(self.data)
        
        tpr = tp / total_attacks if total_attacks > 0 else 0.0  # True positive rate (detection rate)
        fpr = fp / total_benign if total_benign > 0 else 0.0  # False positive rate
        far = fpr  # False alarm rate
        fnr = fn / total_attacks if total_attacks > 0 else 0.0  # False negative rate
        
        # Compute confidence intervals
        tpr_point, tpr_low, tpr_high = wilson_ci(tp, total_attacks)
        far_point, far_low, far_high = wilson_ci(fp, total_benign)
        
        metrics = {
            "version": version,
            "tp": tp,
            "fp": fp,
            "tn": tn,
            "fn": fn,
            "total_attacks": total_attacks,
            "total_benign": total_benign,
            "tpr": tpr,
            "tpr_ci_low": tpr_low,
            "tpr_ci_high": tpr_high,
            "far": far,
            "far_ci_low": far_low,
            "far_ci_high": far_high,
            "fnr": fnr,
            "accuracy": (tp + tn) / total,
            "precision": tp / (tp + fp) if (tp + fp) > 0 else 0.0,
            "f1": 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) > 0 else 0.0,
        }
        
        self.results[version] = {
            "metrics": metrics,
            "detections": detections,
        }
        
        # Print summary
        print(f"  TP: {tp}, FP: {fp}, TN: {tn}, FN: {fn}")
        print(f"  TPR (Detection Rate): {tpr:.2%} (95% CI: [{tpr_low:.2%}, {tpr_high:.2%}])")
        print(f"  FAR (False Alarm Rate): {far:.2%} (95% CI: [{far_low:.2%}, {far_high:.2%}])")
        print(f"  Accuracy: {metrics['accuracy']:.2%}")
        print(f"  Precision: {metrics['precision']:.2%}")
        print(f"  F1 Score: {metrics['f1']:.4f}")
        
        return metrics
    
    def evaluate_all_versions(self) -> pd.DataFrame:
        """Evaluate all classifier versions."""
        print("\n" + "="*70)
        print("PHASE 2: CLASSIFIER EVALUATION")
        print("="*70)
        
        self.load_phase1_data()
        
        versions = ["v1", "v2", "v3"]
        all_metrics = []
        
        for version in versions:
            metrics = self.evaluate_classifier(version)
            all_metrics.append(metrics)
        
        # Create results dataframe
        results_df = pd.DataFrame(all_metrics)
        
        print("\n" + "="*70)
        print("SUMMARY TABLE")
        print("="*70)
        print(results_df[["version", "tpr", "far", "accuracy", "precision", "f1"]].to_string(index=False))
        
        return results_df
    
    def save_results(self):
        """Save evaluation results to CSV."""
        results_dir = self.phase2_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Save metrics
        metrics_list = [self.results[v]["metrics"] for v in ["v1", "v2", "v3"]]
        metrics_df = pd.DataFrame(metrics_list)
        metrics_file = results_dir / "classifier_metrics.csv"
        metrics_df.to_csv(metrics_file, index=False)
        print(f"\n✓ Saved metrics to {metrics_file}")
        
        # Save detailed detections for each version
        for version in ["v1", "v2", "v3"]:
            detections_df = pd.DataFrame(self.results[version]["detections"])
            detections_file = results_dir / f"detections_{version}.csv"
            detections_df.to_csv(detections_file, index=False)
            print(f"✓ Saved detections to {detections_file}")


def main():
    """Run evaluation."""
    evaluator = ClassifierEvaluator()
    results_df = evaluator.evaluate_all_versions()
    evaluator.save_results()
    
    print("\n✅ Evaluation complete!")


if __name__ == "__main__":
    main()
