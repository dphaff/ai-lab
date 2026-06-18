# AI Lab

Hands-on experiments for learning practical AI/LLM systems by building useful local tools.

## Current Projects

### 1. Spending Parser

Turns messy travel spending notes into structured data.

Pipeline:

→ messy notes
→ Python chunking
→ local LLM extraction
→ JSON validation
→ failed chunk retry
→ CSV export
→ SQLite database
→ simple query assistant
```

What this taught:

* local LLMs with Ollama
* chunking messy inputs
* structured JSON extraction
* validation and retry logic
* CSV export
* SQLite basics
* intent-based querying
* when to use AI vs deterministic code

Key lesson:

AI is useful for fuzzy interpretation. Code is better for strict rules, validation, calculations, and database work.

---

### 2. Journal RAG

A private local RAG prototype for asking questions about personal journals.

Pipeline:

→ journal files
→ chunking
→ embeddings
→ SQLite storage
→ similarity search
→ retrieved journal excerpts
→ local LLM answer
```

What this taught:

* embeddings
* cosine similarity
* retrieval
* chunk quality
* metadata
* separating raw journals from era reviews
* evaluating whether answers are grounded in evidence

Key lesson:

RAG quality depends heavily on chunking, retrieval, and evidence. The final answer can sound plausible even when it underweights important details.

---

## Current Limitations

* Small local models can return invalid JSON or weak answers.
* The journal RAG needs better citations/evidence display.
* The spending parser still has imperfect category classification.
* No UI yet.
* No automated tests yet.
* Private input/output data is excluded from GitHub.

---

## Privacy

Private data is ignored via `.gitignore`:

```text
inputs/
outputs/
journal_rag/journal_files/
journal_rag/*.db
```

Only code and documentation should be committed.
