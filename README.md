# Schema-Grounded Text-to-Cypher for Knowledge Graph Q&A

Translates natural-language business questions into Cypher queries against a
knowledge graph, grounded in the graph's actual schema — so non-technical
stakeholders can query structured relationship data (e.g. customer-account-product
networks) without writing queries themselves.

Based on the semantic-schema-prompting method from my paper *"Prompting large
language models based on semantic schema for text-to-Cypher transformation"*
(Decision Support Systems, 2025), and the hybrid knowledge-graph RAG Q&A system I
built for an industrial knowledge graph at Cardiff/Tata Steel.

## Why schema grounding matters

An LLM asked to write Cypher without seeing the actual graph schema will hallucinate
node labels, relationship types, and property names that don't exist in your
database — producing queries that fail silently or return wrong results. This
project's core contribution is injecting a compact, structured schema representation
into the prompt so generated queries are grounded in what the graph actually contains.

## Contents

- **`src/schema_extractor.py`** — extracts a compact schema summary (node labels,
  relationship types, key properties) from a Neo4j graph, formatted for LLM
  consumption without dumping the full raw schema (which wastes context and dilutes
  attention on the parts relevant to a given question).
- **`src/prompt_builder.py`** — constructs the schema-grounded prompt template, with
  few-shot examples mapping question patterns to Cypher patterns.
- **`src/query_validator.py`** — a lightweight static check that a generated Cypher
  query only references labels/relationship types/properties that exist in the
  extracted schema, catching hallucinated queries before they're executed.
- **`src/demo.py`** — walkthrough on a small synthetic customer/account/product graph
  schema (no live Neo4j instance or LLM API call required — demonstrates the
  schema-extraction and validation logic in isolation).
