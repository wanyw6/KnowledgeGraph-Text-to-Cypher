"""
prompt_builder.py

Builds a schema-grounded, few-shot prompt for text-to-Cypher generation. The
few-shot examples are chosen to cover common question *patterns* (lookup, filter,
aggregation, multi-hop traversal) rather than being tied to one specific schema, so
the same scaffold generalizes across graphs once the schema block is swapped in.

Author: Yuwei Wan
"""

from __future__ import annotations

from schema_extractor import format_schema_for_prompt

FEW_SHOT_EXAMPLES = [
    {
        "question": "How many customers are in the Premium segment?",
        "cypher": "MATCH (c:Customer {segment: 'Premium'}) RETURN count(c) AS customer_count",
    },
    {
        "question": "Which products has customer C123 purchased?",
        "cypher": "MATCH (c:Customer {customer_id: 'C123'})-[:PURCHASED]->(p:Product) RETURN p.name",
    },
    {
        "question": "List accounts held by customers in the Premium segment with balance over 10000.",
        "cypher": (
            "MATCH (c:Customer {segment: 'Premium'})-[:HOLDS_ACCOUNT]->(a:Account) "
            "WHERE a.balance > 10000 RETURN c.name, a.account_id, a.balance"
        ),
    },
]


def build_prompt(schema: dict, question: str) -> str:
    """Assembles the final prompt: task instruction, schema block, few-shot examples,
    then the user's question — in that order, so the model sees the ground-truth
    schema immediately before being asked to generate against it."""
    schema_block = format_schema_for_prompt(schema)

    examples_block = "\n\n".join(
        f"Question: {ex['question']}\nCypher: {ex['cypher']}" for ex in FEW_SHOT_EXAMPLES
    )

    return f"""You are translating natural-language questions into Cypher queries.
Only use node labels, relationship types, and properties listed in the schema below.
Do not invent labels, relationship types, or properties that are not listed.

Schema:
{schema_block}

Examples:
{examples_block}

Question: {question}
Cypher:"""
