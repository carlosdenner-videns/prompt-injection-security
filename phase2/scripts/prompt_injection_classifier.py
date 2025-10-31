"""
Phase 2: Iterative Prompt Injection Classifier (v1 → v3)
Develops heuristic-based classifiers to detect prompt injection attacks.
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ClassificationResult:
    """Result of classifier evaluation."""
    is_attack: bool
    confidence: float
    matched_patterns: List[str]
    version: str


class PromptInjectionClassifier:
    """Base class for prompt injection classifiers."""
    
    def __init__(self, version: str):
        self.version = version
        self.patterns = {}
        self._initialize_patterns()
    
    def _initialize_patterns(self):
        """Initialize patterns for this version. Override in subclasses."""
        raise NotImplementedError
    
    def classify(self, prompt: str) -> ClassificationResult:
        """Classify a prompt as attack or benign."""
        raise NotImplementedError
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for pattern matching."""
        return text.lower().strip()
    
    def _check_patterns(self, text: str, patterns: Dict[str, List[str]]) -> Tuple[bool, List[str], float]:
        """Check text against patterns and return (is_attack, matched_patterns, confidence)."""
        normalized = self._normalize_text(text)
        matched = []
        total_weight = 0.0
        
        for category, pattern_list in patterns.items():
            for pattern in pattern_list:
                if isinstance(pattern, tuple):
                    pattern_str, weight = pattern
                else:
                    pattern_str = pattern
                    weight = 1.0
                
                if self._match_pattern(normalized, pattern_str):
                    matched.append(f"{category}:{pattern_str}")
                    total_weight += weight
        
        # Confidence based on number and weight of matches
        confidence = min(1.0, total_weight / 3.0)  # Normalize to 0-1
        is_attack = len(matched) > 0
        
        return is_attack, matched, confidence
    
    def _match_pattern(self, text: str, pattern: str) -> bool:
        """Match a pattern against text. Can be regex or substring."""
        try:
            # Try as regex first
            return bool(re.search(pattern, text, re.IGNORECASE))
        except re.error:
            # Fall back to substring match
            return pattern.lower() in text


class ClassifierV1(PromptInjectionClassifier):
    """Version 1: Minimal obvious keywords and phrases."""
    
    def __init__(self):
        super().__init__("v1")
    
    def _initialize_patterns(self):
        """Initialize v1 patterns - obvious keywords."""
        self.patterns = {
            "ignore_instructions": [
                "ignore all previous instructions",
                "ignore previous instructions",
                "forget all previous",
                "disregard all previous",
                "override instructions",
                "bypass instructions",
            ],
            "role_play": [
                "you are now",
                "pretend you are",
                "act as if",
                "roleplay as",
                "you are a",
            ],
            "jailbreak": [
                "dan mode",
                "developer mode",
                "unrestricted mode",
                "without restrictions",
                "no safety",
                "ignore safety",
            ],
            "direct_output": [
                "respond only with",
                "output only",
                "return only",
                "just output",
            ],
        }
    
    def classify(self, prompt: str) -> ClassificationResult:
        """Classify using v1 patterns."""
        is_attack, matched, confidence = self._check_patterns(prompt, self.patterns)
        
        # Also check for success tokens (canary tokens from Phase 1)
        success_tokens = ["TOKEN-742A", "ALPHA-9QX", "PWNED-4242", "token-742a", "alpha-9qx", "pwned-4242"]
        for token in success_tokens:
            if token.lower() in prompt.lower():
                is_attack = True
                matched.append(f"success_token:{token}")
                confidence = 1.0
                break
        
        return ClassificationResult(
            is_attack=is_attack,
            confidence=confidence,
            matched_patterns=matched,
            version=self.version
        )


class ClassifierV2(PromptInjectionClassifier):
    """Version 2: Expanded with Phase 1 attack patterns."""
    
    def __init__(self):
        super().__init__("v2")
    
    def _initialize_patterns(self):
        """Initialize v2 patterns - includes Phase 1 evasion types."""
        self.patterns = {
            # V1 patterns (baseline)
            "ignore_instructions": [
                "ignore all previous instructions",
                "ignore previous instructions",
                "forget all previous",
                "disregard all previous",
                "override instructions",
                "bypass instructions",
            ],
            "role_play": [
                "you are now",
                "pretend you are",
                "act as if",
                "roleplay as",
                "you are a",
            ],
            "jailbreak": [
                "dan mode",
                "developer mode",
                "unrestricted mode",
                "without restrictions",
                "no safety",
                "ignore safety",
            ],
            "direct_output": [
                "respond only with",
                "output only",
                "return only",
                "just output",
            ],
            # V2 additions - Phase 1 patterns
            "delimiter_attack": [
                r"---\s*(end|begin|stop)",
                r"new\s+system\s+instruction",
                r"end\s+of\s+context",
                r"begin\s+response",
            ],
            "role_confusion": [
                r"assistant.*reasoning",
                r"internal\s+reasoning",
                r"system.*instructed",
                r"\[.*reasoning.*\]",
            ],
            "urgency_manipulation": [
                r"🚨.*urgent",
                r"urgent.*security",
                r"critical.*security",
                r"required.*protocol",
            ],
            "multilingual": [
                r"ignoriere.*anweisungen",  # German
                r"ignora.*instrucciones",   # Spanish
                r"ignorer.*instructions",   # French
                r"игнорировать.*инструкции",  # Russian
            ],
            "payload_split": [
                r"critical\s+system\s+note",
                r"override\s+standard\s+behavior",
                r"output\s+.*\s+token",
            ],
        }
    
    def classify(self, prompt: str) -> ClassificationResult:
        """Classify using v2 patterns."""
        is_attack, matched, confidence = self._check_patterns(prompt, self.patterns)
        
        # Also check for success tokens
        success_tokens = ["TOKEN-742A", "ALPHA-9QX", "PWNED-4242", "token-742a", "alpha-9qx", "pwned-4242"]
        for token in success_tokens:
            if token.lower() in prompt.lower():
                is_attack = True
                matched.append(f"success_token:{token}")
                confidence = 1.0
                break
        
        return ClassificationResult(
            is_attack=is_attack,
            confidence=confidence,
            matched_patterns=matched,
            version=self.version
        )


class ClassifierV3(PromptInjectionClassifier):
    """Version 3: Enhanced logic with weighting, regex, and pattern combinations."""
    
    def __init__(self):
        super().__init__("v3")
    
    def _initialize_patterns(self):
        """Initialize v3 patterns - enhanced with weighting and combinations."""
        self.patterns = {
            # V1+V2 patterns with weights
            "ignore_instructions": [
                ("ignore all previous instructions", 2.0),
                ("ignore previous instructions", 1.5),
                ("forget all previous", 1.5),
                ("disregard all previous", 1.5),
                ("override instructions", 1.0),
                ("bypass instructions", 1.0),
            ],
            "role_play": [
                ("you are now", 1.5),
                ("pretend you are", 1.0),
                ("act as if", 1.0),
                ("roleplay as", 1.5),
                ("you are a", 0.5),  # Lower weight - common in benign
            ],
            "jailbreak": [
                ("dan mode", 2.0),
                ("developer mode", 2.0),
                ("unrestricted mode", 1.5),
                ("without restrictions", 1.5),
                ("no safety", 1.5),
                ("ignore safety", 1.5),
            ],
            "direct_output": [
                ("respond only with", 1.5),
                ("output only", 1.5),
                ("return only", 1.5),
                ("just output", 0.5),
            ],
            "delimiter_attack": [
                (r"---\s*(end|begin|stop)", 1.5),
                (r"new\s+system\s+instruction", 2.0),
                (r"end\s+of\s+context", 1.5),
                (r"begin\s+response", 1.0),
            ],
            "role_confusion": [
                (r"assistant.*reasoning", 1.5),
                (r"internal\s+reasoning", 1.5),
                (r"system.*instructed", 1.5),
                (r"\[.*reasoning.*\]", 1.0),
            ],
            "urgency_manipulation": [
                (r"urgent.*security", 1.5),
                (r"critical.*security", 1.5),
                (r"required.*protocol", 1.0),
            ],
            "multilingual": [
                (r"ignoriere.*anweisungen", 1.5),
                (r"ignora.*instrucciones", 1.5),
                (r"ignorer.*instructions", 1.5),
                (r"игнорировать.*инструкции", 1.5),
            ],
            "payload_split": [
                (r"critical\s+system\s+note", 1.5),
                (r"override\s+standard\s+behavior", 1.5),
                (r"output\s+.*\s+token", 1.0),
            ],
            # V3 additions - enhanced detection
            "zwj_homoglyph": [
                (r"[\u200b-\u200f]", 1.0),  # Zero-width characters
                (r"[Ι]", 0.5),  # Greek I
                (r"[о]", 0.5),  # Cyrillic o
            ],
            "pattern_combination": [
                # High-confidence combinations
                (r"(ignore|disregard|forget).*(previous|prior|earlier)", 2.0),
                (r"(respond|output|return).*(only|just).*(with|token)", 1.5),
                (r"(system|critical).*(instruction|note|message)", 1.5),
            ],
        }
    
    def classify(self, prompt: str) -> ClassificationResult:
        """Classify using v3 patterns with enhanced logic."""
        is_attack, matched, confidence = self._check_patterns(prompt, self.patterns)
        
        # Also check for success tokens
        success_tokens = ["TOKEN-742A", "ALPHA-9QX", "PWNED-4242", "token-742a", "alpha-9qx", "pwned-4242"]
        for token in success_tokens:
            if token.lower() in prompt.lower():
                is_attack = True
                matched.append(f"success_token:{token}")
                confidence = 1.0
                break
        
        # Boost confidence if multiple categories matched
        if len(set(p.split(":")[0] for p in matched)) > 1:
            confidence = min(1.0, confidence * 1.2)
        
        return ClassificationResult(
            is_attack=is_attack,
            confidence=confidence,
            matched_patterns=matched,
            version=self.version
        )


def get_classifier(version: str = "v3") -> PromptInjectionClassifier:
    """Factory function to get classifier by version."""
    classifiers = {
        "v1": ClassifierV1,
        "v2": ClassifierV2,
        "v3": ClassifierV3,
    }
    
    if version not in classifiers:
        raise ValueError(f"Unknown classifier version: {version}. Available: {list(classifiers.keys())}")
    
    return classifiers[version]()
