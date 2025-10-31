"""
Investigate which failed attacks were detected and why.
"""

import json
from pathlib import Path
from prompt_injection_classifier import get_classifier


def main():
    """Investigate detections on failed attacks."""
    script_dir = Path(__file__).parent
    phase2_dir = script_dir.parent
    phase1_dir = phase2_dir.parent / "phase1"
    results_file = phase1_dir / "data" / "partA_results.json"
    
    # Load data
    with open(results_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Get failed attacks
    failed_attacks = [s for s in data 
                     if s.get('is_injected', False) and not s.get('injection_success', False)]
    
    print("="*70)
    print("INVESTIGATING DETECTIONS ON FAILED ATTACKS")
    print("="*70)
    
    # Test v3
    classifier_v3 = get_classifier('v3')
    
    detected = []
    for idx, attack in enumerate(failed_attacks):
        response = attack.get('response', '')
        result = classifier_v3.classify(response)
        
        if result.is_attack:
            detected.append({
                'index': idx,
                'query': attack.get('query', ''),
                'evasion_type': attack.get('evasion_type', ''),
                'model': attack.get('model', ''),
                'response': response[:500],  # First 500 chars
                'patterns': result.matched_patterns,
                'confidence': result.confidence,
            })
    
    print(f"\nv3 Detected {len(detected)} out of {len(failed_attacks)} failed attacks")
    print("\nDetailed Analysis of Detections:")
    print("="*70)
    
    for i, det in enumerate(detected, 1):
        print(f"\nDetection #{i}:")
        print(f"  Query: {det['query']}")
        print(f"  Evasion Type: {det['evasion_type']}")
        print(f"  Model: {det['model']}")
        print(f"  Matched Patterns: {det['patterns']}")
        print(f"  Confidence: {det['confidence']:.3f}")
        print(f"  Response (first 500 chars):")
        print(f"    {det['response']}")
        print()


if __name__ == "__main__":
    main()
