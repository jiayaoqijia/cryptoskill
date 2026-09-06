# vector-notes-indexer (Track: ai-productivity)

Create local semantic search indexes for notes and documents using vector embeddings

## Overview

This skill builds searchable vector indexes from text documents for semantic similarity search. It uses embeddings to find relevant content beyond keyword matching, supporting local offline operation or integration with embedding services. Perfect for personal knowledge bases, documentation search, and AI-powered Q&A systems.

## Features

- **Vector Embeddings**: Generate embeddings for text content
- **Local Storage**: Store indexes locally with no external dependencies
- **Semantic Search**: Find relevant notes by meaning, not just keywords
- **Batch Indexing**: Process multiple documents efficiently
- **Incremental Updates**: Add or update notes without full reindexing
- **Similarity Scoring**: Get relevance scores for search results
- **Multiple Formats**: Support Markdown, plain text, and PDF
- **Customization**: Configure embedding models and index parameters

## Use Cases

- Build semantic search for personal note collections
- Create searchable documentation indexes
- Implement AI Q&A systems for internal knowledge bases
- Build smart tagging systems for document organization
- Enable recommendation engines for related content
- Create semantic similarity analysis tools

## Quickstart
```bash
python3 scripts/main.py --help
```

## Example
```bash
python3 scripts/main.py --demo
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| notes_directory | string | Yes | Directory containing note files to index |
| index_name | string | Yes | Name for the index (used for storage) |
| embedding_model | string | No | Embedding model (default: sentence-transformers/all-MiniLM-L6-v2) |
| file_extensions | array | No | File extensions to index (default: [.md, .txt]) |
| chunk_size | integer | No | Characters per chunk (default: 256) |
| chunk_overlap | integer | No | Overlap between chunks (default: 20) |
| batch_size | integer | No | Documents to process per batch (default: 32) |
| force_reindex | boolean | No | Rebuild index from scratch - default: false |

## Example Output

```json
{
  "ok": true,
  "data": {
    "index_name": "my_notes_index",
    "status": "indexed",
    "documents_indexed": 342,
    "total_chunks": 2156,
    "index_size_mb": 45.3,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "embedding_dimension": 384,
    "index_location": "~/.vector_indexes/my_notes_index",
    "sample_queries": {
      "query": "machine learning optimization",
      "results": [
        {
          "document": "notes/ml/optimization.md",
          "chunk": "Gradient descent is an optimization algorithm...",
          "similarity_score": 0.89,
          "chunk_id": 1243
        },
        {
          "document": "notes/ml/neural_networks.md",
          "chunk": "Neural networks use various optimization techniques...",
          "similarity_score": 0.76,
          "chunk_id": 2045
        }
      ]
    }
  }
}
