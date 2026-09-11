"""demo.py — schema-grounded text-to-Cypher prompt building + hallucination validation."""

import sys, os
sys.path.append(os.path.dirname(__file__))

from schema_extractor import format_schema_for_prompt, extract_valid_elements
from prompt_builder import build_prompt
from query_validator import validate_query

schema = {
    "nodes": {
        "Customer": ["customer_id", "name", "segment"],
        "Account": ["account_id", "balance", "opened_date"],
        "Product": ["product_id", "name", "category"],
    },
    "relationships": [
        {"type": "HOLDS_ACCOUNT", "from": "Customer", "to": "Account"},
        {"type": "PURCHASED", "from": "Customer", "to": "Product"},
    ],
}

print("=== Schema summary given to the LLM ===")
print(format_schema_for_prompt(schema))

question = "Which Premium customers hold an account with balance over 50000?"
prompt = build_prompt(schema, question)
print("\n=== Full prompt (would be sent to the LLM) ===")
print(prompt)

valid_elements = extract_valid_elements(schema)

print("\n=== Validating a correct, schema-grounded query ===")
good_query = "MATCH (c:Customer {segment: 'Premium'})-[:HOLDS_ACCOUNT]->(a:Account) WHERE a.balance > 50000 RETURN c.name"
print(validate_query(good_query, valid_elements))

print("\n=== Validating a hallucinated query (invented label + relationship) ===")
bad_query = "MATCH (c:Client)-[:OWNS]->(a:Account) WHERE a.balance > 50000 RETURN c.name"
print(validate_query(bad_query, valid_elements))
