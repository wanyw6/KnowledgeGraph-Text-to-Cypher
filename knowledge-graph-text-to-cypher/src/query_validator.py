"""
query_validator.py

Lightweight static validation that a generated Cypher query only references schema
elements known to actually exist — catches the most common LLM failure mode
(hallucinated labels/relationship types/properties) before a query is ever executed
against the database.

This is intentionally a regex-based structural check, not a full Cypher parser —
sufficient to flag hallucinated identifiers, which is the failure mode schema
grounding is meant to prevent, without the engineering cost of a full grammar.

Author: Yuwei Wan
"""

from __future__ import annotations

import re


def extract_referenced_labels(cypher: str) -> set[str]:
    """Finds patterns like (c:Customer) or (:Product) and extracts the label."""
    return set(re.findall(r":(\w+)\s*[\{\)]", cypher))


def extract_referenced_rel_types(cypher: str) -> set[str]:
    """Finds patterns like -[:HOLDS_ACCOUNT]-> and extracts the relationship type."""
    return set(re.findall(r"\[:(\w+)\]", cypher))


def validate_query(cypher: str, valid_elements: dict) -> dict:
    """
    Returns a validation report: whether the query is clean, and any hallucinated
    labels or relationship types found that don't exist in the actual schema.
    """
    referenced_labels = extract_referenced_labels(cypher)
    referenced_rels = extract_referenced_rel_types(cypher)

    unknown_labels = referenced_labels - valid_elements["labels"]
    unknown_rels = referenced_rels - valid_elements["relationship_types"]

    return {
        "is_valid": not unknown_labels and not unknown_rels,
        "unknown_labels": unknown_labels,
        "unknown_relationship_types": unknown_rels,
    }
