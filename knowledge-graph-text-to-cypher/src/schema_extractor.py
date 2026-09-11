"""
schema_extractor.py

Extracts a compact, LLM-friendly schema summary from a graph's structural metadata.
In a live system this would query Neo4j's schema procedures (e.g. `CALL db.schema.visualization()`
or APOC's `apoc.meta.schema()`); here it operates on an explicit schema dict so the
logic can be demonstrated and tested without a running database.

Author: Yuwei Wan
"""

from __future__ import annotations


def format_schema_for_prompt(schema: dict) -> str:
    """
    Converts a structured schema dict into a compact textual form suitable for
    inclusion in an LLM prompt — labels and relationships only, with key properties,
    not the full property list (which for a real production graph can run to
    hundreds of fields and would dominate the prompt budget for no benefit).

    Expected schema shape:
    {
        "nodes": {"Customer": ["customer_id", "name", "segment"], ...},
        "relationships": [
            {"type": "HOLDS_ACCOUNT", "from": "Customer", "to": "Account"},
            ...
        ],
    }
    """
    lines = ["Node labels and key properties:"]
    for label, props in schema.get("nodes", {}).items():
        lines.append(f"  ({label} {{{', '.join(props)}}})")

    lines.append("\nRelationships:")
    for rel in schema.get("relationships", []):
        lines.append(f"  (:{rel['from']})-[:{rel['type']}]->(:{rel['to']})")

    return "\n".join(lines)


def extract_valid_elements(schema: dict) -> dict:
    """Flattens the schema into sets of valid labels/relationship-types/properties,
    used by the query validator to check a generated Cypher query for hallucinated
    elements."""
    labels = set(schema.get("nodes", {}).keys())
    rel_types = {rel["type"] for rel in schema.get("relationships", [])}
    properties = {p for props in schema.get("nodes", {}).values() for p in props}
    return {"labels": labels, "relationship_types": rel_types, "properties": properties}
