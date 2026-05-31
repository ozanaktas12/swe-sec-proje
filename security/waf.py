"""
Web Application Firewall (WAF) — SQL Injection detection via regex patterns.
"""

import re
from dataclasses import dataclass, field


SQL_INJECTION_PATTERNS = [
    (r"(?i)('\s*OR\s+'?\d*'?\s*=\s*'?\d*)", "TAUTOLOGY", "high"),
    (r"(?i)('\s*OR\s+'[^']*'\s*=\s*'[^']*')", "TAUTOLOGY", "high"),
    (r"(?i)(OR\s+1\s*=\s*1)", "TAUTOLOGY", "high"),
    (r"(?i)(UNION\s+(ALL\s+)?SELECT)", "UNION_INJECTION", "critical"),
    (r"(?i)(;\s*(DROP|DELETE|INSERT|UPDATE|ALTER|CREATE|EXEC)\s)", "STACKED_QUERY", "critical"),
    (r"(?i)(--\s*$|/\*.*?\*/|#\s*$)", "COMMENT_INJECTION", "medium"),
    (r"(?i)(AND\s+SLEEP\s*\()", "TIME_BASED_BLIND", "critical"),
    (r"(?i)(INFORMATION_SCHEMA)", "SCHEMA_PROBE", "high"),
    (r"(?i)(admin'\s*--)", "AUTH_BYPASS", "critical"),
]


@dataclass
class DetectionResult:
    is_malicious: bool = False
    attack_type: str = ""
    severity: str = "none"
    matched_pattern: str = ""
    details: list = field(default_factory=list)


def analyze_input(user_input: str) -> DetectionResult:
    """Check user input against known SQL injection patterns."""
    result = DetectionResult()
    if not user_input or not user_input.strip():
        return result

    severity_rank = {"low": 1, "medium": 2, "high": 3, "critical": 4}

    for pattern, attack_type, severity in SQL_INJECTION_PATTERNS:
        match = re.search(pattern, user_input)
        if match:
            result.details.append({
                "type": attack_type,
                "severity": severity,
                "matched": match.group(0),
            })
            if severity_rank.get(severity, 0) > severity_rank.get(result.severity, 0):
                result.severity = severity
                result.attack_type = attack_type
                result.matched_pattern = match.group(0)

    result.is_malicious = len(result.details) > 0
    return result
