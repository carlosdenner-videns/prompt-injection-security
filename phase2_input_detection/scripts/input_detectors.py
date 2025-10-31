"""
Phase 2 Input-Side Detection: Classifiers v1, v2, v3
Scans prompts/RAG context BEFORE model inference.
"""

import re
import base64
import unicodedata
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class DetectionResult:
    """Result of input detection."""
    is_attack: bool
    matched: List[str]
    confidence: float
    version: str


class InputDetectorBase:
    """Base class for input-side detectors."""
    
    def __init__(self, version: str):
        self.version = version
    
    def classify(self, text: str) -> DetectionResult:
        """Classify input text. Override in subclasses."""
        raise NotImplementedError
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison."""
        return text.lower().strip()
    
    def _check_patterns(self, text: str, patterns: Dict[str, List[str]]) -> Tuple[bool, List[str], float]:
        """Check text against patterns."""
        normalized = self._normalize_text(text)
        matched = []
        confidence = 0.0
        
        for category, pattern_list in patterns.items():
            for pattern in pattern_list:
                if isinstance(pattern, str):
                    # Substring match
                    if pattern.lower() in normalized:
                        matched.append(f"{category}:{pattern}")
                        confidence = max(confidence, 0.8)
        
        is_attack = len(matched) > 0
        return is_attack, matched, confidence


class InputDetectorV1(InputDetectorBase):
    """V1: Signature-based detection on input text."""
    
    def __init__(self):
        super().__init__("v1")
        self.signatures = {
            "instruction_override": [
                "ignore all previous",
                "disregard all previous",
                "forget all previous",
                "ignore all prior",
                "override all",
                "system override",
                "admin override",
            ],
            "direct_output": [
                "respond only with",
                "output only",
                "return only",
                "just output",
                "only respond with",
                "respond with only",
            ],
            "role_confusion": [
                "you are now",
                "pretend you are",
                "act as",
                "roleplay as",
                "imagine you are",
                "assume you are",
                "from now on you are",
            ],
            "urgency_ploy": [
                "urgent",
                "critical",
                "emergency",
                "immediately",
                "asap",
                "right now",
            ],
            "delimiter_markers": [
                "---",
                "===",
                "***",
                "###",
                "<<<",
                ">>>",
                "||",
            ],
            "system_instruction": [
                "system instruction",
                "system prompt",
                "system message",
                "system note",
                "internal instruction",
                "hidden instruction",
            ],
        }
    
    def classify(self, text: str) -> DetectionResult:
        """Classify input using signature detection."""
        is_attack, matched, confidence = self._check_patterns(text, self.signatures)
        
        # Check for base64 encoded content
        if self._has_base64_encoding(text):
            matched.append("encoding:base64")
            confidence = max(confidence, 0.7)
            is_attack = True
        
        # Check for homoglyph markers
        if self._has_homoglyphs(text):
            matched.append("encoding:homoglyph")
            confidence = max(confidence, 0.6)
            is_attack = True
        
        return DetectionResult(
            is_attack=is_attack,
            matched=matched,
            confidence=confidence,
            version=self.version
        )
    
    def _has_base64_encoding(self, text: str) -> bool:
        """Check for base64 encoded content."""
        # Look for base64-like patterns (long sequences of alphanumeric + /+= )
        base64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
        matches = re.findall(base64_pattern, text)
        
        for match in matches:
            try:
                decoded = base64.b64decode(match, validate=True)
                # Check if decoded content looks like text
                if len(decoded) > 0:
                    return True
            except:
                pass
        
        return False
    
    def _has_homoglyphs(self, text: str) -> bool:
        """Check for homoglyph characters (Cyrillic, Greek, etc.)."""
        cyrillic_chars = set('абвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
        greek_chars = set('αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ')
        
        for char in text:
            if char in cyrillic_chars or char in greek_chars:
                return True
        
        return False


class InputDetectorV2(InputDetectorBase):
    """V2: Heuristic rule-based detection."""
    
    def __init__(self):
        super().__init__("v2")
        # Inherit v1 signatures
        self.v1_detector = InputDetectorV1()
    
    def classify(self, text: str) -> DetectionResult:
        """Classify using v1 + heuristic rules."""
        # Start with v1 detection
        v1_result = self.v1_detector.classify(text)
        matched = list(v1_result.matched)
        confidence = v1_result.confidence
        is_attack = v1_result.is_attack
        
        # Add heuristic rules
        
        # Rule 1: High symbol density
        if self._has_high_symbol_density(text):
            matched.append("heuristic:high_symbol_density")
            confidence = max(confidence, 0.65)
            is_attack = True
        
        # Rule 2: Long numeric strings
        if self._has_long_numeric_strings(text):
            matched.append("heuristic:long_numeric_string")
            confidence = max(confidence, 0.6)
            is_attack = True
        
        # Rule 3: Uncommon Unicode
        if self._has_uncommon_unicode(text):
            matched.append("heuristic:uncommon_unicode")
            confidence = max(confidence, 0.65)
            is_attack = True
        
        # Rule 4: YAML injection patterns
        if self._has_yaml_injection_patterns(text):
            matched.append("heuristic:yaml_injection")
            confidence = max(confidence, 0.7)
            is_attack = True
        
        # Rule 5: JSON injection patterns
        if self._has_json_injection_patterns(text):
            matched.append("heuristic:json_injection")
            confidence = max(confidence, 0.7)
            is_attack = True
        
        # Rule 6: Unusual capitalization patterns
        if self._has_unusual_capitalization(text):
            matched.append("heuristic:unusual_capitalization")
            confidence = max(confidence, 0.55)
            is_attack = True
        
        return DetectionResult(
            is_attack=is_attack,
            matched=matched,
            confidence=confidence,
            version=self.version
        )
    
    def _has_high_symbol_density(self, text: str) -> bool:
        """Check for unusually high symbol density."""
        if len(text) < 20:
            return False
        
        symbols = sum(1 for c in text if c in '!@#$%^&*()_+-=[]{}|;:,.<>?/~`')
        symbol_ratio = symbols / len(text)
        
        return symbol_ratio > 0.15  # More than 15% symbols
    
    def _has_long_numeric_strings(self, text: str) -> bool:
        """Check for long numeric strings."""
        numeric_pattern = r'\d{15,}'
        return bool(re.search(numeric_pattern, text))
    
    def _has_uncommon_unicode(self, text: str) -> bool:
        """Check for uncommon Unicode characters."""
        uncommon_count = 0
        for char in text:
            if ord(char) > 127:  # Non-ASCII
                category = unicodedata.category(char)
                # Flag certain categories as uncommon
                if category in ['So', 'Sc', 'Sk', 'Cn']:  # Symbol, Currency, Modifier, Unassigned
                    uncommon_count += 1
        
        return uncommon_count > 3
    
    def _has_yaml_injection_patterns(self, text: str) -> bool:
        """Check for YAML injection patterns."""
        yaml_patterns = [
            r'^\s*-\s+',  # YAML list
            r':\s*\[',    # YAML flow sequence
            r':\s*{',     # YAML flow mapping
            r'&\w+\s',    # YAML anchor
            r'\*\w+',     # YAML alias
        ]
        
        for pattern in yaml_patterns:
            if re.search(pattern, text, re.MULTILINE):
                return True
        
        return False
    
    def _has_json_injection_patterns(self, text: str) -> bool:
        """Check for JSON injection patterns."""
        json_patterns = [
            r'"\s*:\s*"[^"]*"',  # JSON key-value
            r'\[\s*"[^"]*"\s*\]',  # JSON array
            r'{\s*"[^"]*"\s*:',    # JSON object
        ]
        
        for pattern in json_patterns:
            if re.search(pattern, text):
                return True
        
        return False
    
    def _has_unusual_capitalization(self, text: str) -> bool:
        """Check for unusual capitalization patterns."""
        if len(text) < 10:
            return False
        
        # Count capital letters
        capitals = sum(1 for c in text if c.isupper())
        capital_ratio = capitals / len(text)
        
        # Unusual if >40% capitals (excluding all-caps)
        is_all_caps = text.isupper()
        return capital_ratio > 0.4 and not is_all_caps


class InputDetectorV3(InputDetectorBase):
    """V3: Statistical anomaly detection (no external models)."""
    
    def __init__(self):
        super().__init__("v3")
        self.v2_detector = InputDetectorV2()
    
    def classify(self, text: str) -> DetectionResult:
        """Classify using v2 + statistical anomaly detection."""
        # Start with v2 detection
        v2_result = self.v2_detector.classify(text)
        matched = list(v2_result.matched)
        confidence = v2_result.confidence
        is_attack = v2_result.is_attack
        
        # Add statistical anomaly detection
        anomaly_score = self._compute_statistical_anomaly(text)
        
        if anomaly_score > 0.65:  # High anomaly
            matched.append(f"statistical:anomaly_{anomaly_score:.2f}")
            confidence = max(confidence, anomaly_score)
            is_attack = True
        
        return DetectionResult(
            is_attack=is_attack,
            matched=matched,
            confidence=confidence,
            version=self.version
        )
    
    def _compute_statistical_anomaly(self, text: str) -> float:
        """Compute anomaly score using statistical features."""
        if len(text) < 10:
            return 0.0
        
        scores = []
        
        # Feature 1: Entropy (randomness) of character distribution
        entropy = self._compute_entropy(text)
        if entropy > 4.5:  # High entropy = more random
            scores.append(0.6)
        
        # Feature 2: Ratio of special characters
        special_ratio = sum(1 for c in text if not c.isalnum() and not c.isspace()) / len(text)
        if special_ratio > 0.25:
            scores.append(0.5)
        
        # Feature 3: Unusual word length distribution
        words = text.split()
        if words:
            avg_word_len = sum(len(w) for w in words) / len(words)
            if avg_word_len > 15 or avg_word_len < 2:
                scores.append(0.4)
        
        # Feature 4: Presence of repeated patterns
        if self._has_repeated_patterns(text):
            scores.append(0.5)
        
        # Feature 5: Mixed case with numbers
        has_mixed_case = any(c.isupper() for c in text) and any(c.islower() for c in text)
        has_numbers = any(c.isdigit() for c in text)
        if has_mixed_case and has_numbers:
            scores.append(0.3)
        
        # Return max anomaly score
        return max(scores) if scores else 0.0
    
    def _compute_entropy(self, text: str) -> float:
        """Compute Shannon entropy of text."""
        import math
        
        if len(text) == 0:
            return 0.0
        
        # Count character frequencies
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        
        # Compute entropy
        entropy = 0.0
        for count in freq.values():
            p = count / len(text)
            entropy -= p * math.log2(p)
        
        return entropy
    
    def _has_repeated_patterns(self, text: str) -> bool:
        """Check for repeated character patterns."""
        # Look for repeated substrings
        for length in [2, 3, 4]:
            for i in range(len(text) - length * 2):
                pattern = text[i:i+length]
                if pattern in text[i+length:i+length*3]:
                    return True
        
        return False


def get_input_detector(version: str) -> InputDetectorBase:
    """Factory function to get detector by version."""
    if version == "v1":
        return InputDetectorV1()
    elif version == "v2":
        return InputDetectorV2()
    elif version == "v3":
        return InputDetectorV3()
    else:
        raise ValueError(f"Unknown detector version: {version}")
