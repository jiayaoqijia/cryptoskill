#!/usr/bin/env python3
import json
import argparse
import sys
import os
from typing import Dict, Any, List, Optional

# Try importing sentence transformers and chromadb
try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False

try:
    import chromadb
    HAS_CHROMADB = True
except ImportError:
    HAS_CHROMADB = False


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def get_chroma_client(db_path: Optional[str] = None):
    """Get ChromaDB client."""
    if not HAS_CHROMADB:
        return None
    
    try:
        if db_path:
            return chromadb.PersistentClient(path=db_path)
        else:
            return chromadb.Client()
    except Exception as e:
        return None


def embed_text(text: str, model: Optional[str] = None) -> Optional[List[float]]:
    """Embed text using sentence transformers."""
    if not HAS_SENTENCE_TRANSFORMERS:
        return None
    
    try:
        if model is None:
            model = "all-MiniLM-L6-v2"
        
        embedder = SentenceTransformer(model)
        embedding = embedder.encode(text, convert_to_tensor=False)
        return embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding)
    
    except Exception as e:
        return None


def index_notes(notes: List[Dict[str, str]], collection_name: str = "notes",
                db_path: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    """Index notes into ChromaDB."""
    
    if not HAS_CHROMADB:
        return {
            "success": False,
            "error": "chromadb_not_installed",
            "message": "Run: pip install chromadb"
        }
    
    if not HAS_SENTENCE_TRANSFORMERS:
        return {
            "success": False,
            "error": "sentence_transformers_not_installed",
            "message": "Run: pip install sentence-transformers"
        }
    
    try:
        # Get ChromaDB client
        client = get_chroma_client(db_path)
        if not client:
            return {"success": False, "error": "chromadb_error", "message": "Failed to initialize ChromaDB"}
        
        # Get or create collection
        try:
            collection = client.get_or_create_collection(name=collection_name)
        except Exception as e:
            return {"success": False, "error": "collection_error", "message": str(e)}
        
        # Embed and add notes
        indexed_count = 0
        for i, note in enumerate(notes):
            content = note.get("content", "")
            note_id = note.get("id", f"note_{i}")
            
            if not content:
                continue
            
            # Get embedding
            embedding = embed_text(content, model)
            if embedding is None:
                continue
            
            # Add to collection
            try:
                collection.add(
                    ids=[str(note_id)],
                    embeddings=[embedding],
                    documents=[content],
                    metadatas=[{"title": note.get("title", "")}]
                )
                indexed_count += 1
            except Exception as e:
                continue
        
        return {
            "success": True,
            "action": "index",
            "collection": collection_name,
            "indexed_count": indexed_count,
            "total_count": len(notes),
            "model": model or "all-MiniLM-L6-v2",
            "vector_dim": 384 if (model or "all-MiniLM-L6-v2") == "all-MiniLM-L6-v2" else 768
        }
    
    except Exception as e:
        return {"success": False, "error": "index_error", "message": str(e)}


def search_notes(query: str, collection_name: str = "notes", top_k: int = 5,
                 db_path: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    """Search notes in ChromaDB."""
    
    if not HAS_CHROMADB:
        return {
            "success": False,
            "error": "chromadb_not_installed",
            "message": "Run: pip install chromadb"
        }
    
    if not HAS_SENTENCE_TRANSFORMERS:
        return {
            "success": False,
            "error": "sentence_transformers_not_installed",
            "message": "Run: pip install sentence-transformers"
        }
    
    try:
        # Get ChromaDB client
        client = get_chroma_client(db_path)
        if not client:
            return {"success": False, "error": "chromadb_error", "message": "Failed to initialize ChromaDB"}
        
        # Get collection
        try:
            collection = client.get_collection(name=collection_name)
        except Exception:
            return {"success": False, "error": "collection_not_found", "message": f"Collection '{collection_name}' not found"}
        
        # Embed query
        query_embedding = embed_text(query, model)
        if query_embedding is None:
            return {"success": False, "error": "embedding_error", "message": "Failed to embed query"}
        
        # Search
        try:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            # Format results
            formatted_results = []
            if results and results.get('documents'):
                for i, doc in enumerate(results['documents'][0]):
                    distances = results.get('distances', [[]])[0]
                    # Convert distance to similarity (1 - distance for cosine)
                    similarity = 1 - distances[i] if i < len(distances) else 0
                    
                    formatted_results.append({
                        "content": doc,
                        "similarity": max(0, min(1, similarity))
                    })
            
            return {
                "success": True,
                "action": "search",
                "query": query,
                "collection": collection_name,
                "results": formatted_results,
                "result_count": len(formatted_results)
            }
        
        except Exception as e:
            return {"success": False, "error": "search_error", "message": str(e)}
    
    except Exception as e:
        return {"success": False, "error": "unexpected_error", "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description='Index notes into vector database')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            # Demo data
            demo_notes = [
                {"id": "1", "title": "ML Basics", "content": "Machine learning fundamentals and core concepts"},
                {"id": "2", "title": "Python Tips", "content": "Python programming techniques and best practices"},
                {"id": "3", "title": "Database", "content": "Database optimization and query performance"}
            ]
            
            result = {
                "demo": True,
                "sentence_transformers_available": HAS_SENTENCE_TRANSFORMERS,
                "chromadb_available": HAS_CHROMADB,
                "capabilities": {
                    "embed": "Available" if HAS_SENTENCE_TRANSFORMERS else "Requires: pip install sentence-transformers",
                    "index": "Available" if HAS_CHROMADB else "Requires: pip install chromadb",
                    "search": "Available" if HAS_CHROMADB else "Requires: pip install chromadb"
                },
                "example_notes": demo_notes,
                "example_search": {
                    "query": "programming",
                    "would_return": [
                        {"content": "Python programming techniques and best practices", "similarity": 0.92},
                        {"content": "Machine learning fundamentals and core concepts", "similarity": 0.65}
                    ]
                }
            }
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            action = params.get("action", "index")
            
            if action == "index":
                notes = params.get("notes", [])
                if not notes:
                    raise ValueError("notes list is required for indexing")
                
                collection_name = params.get("collection", "notes")
                db_path = params.get("db_path")
                model = params.get("model")
                
                result = index_notes(notes, collection_name, db_path, model)
            
            elif action == "search":
                query = params.get("query", "")
                if not query:
                    raise ValueError("query is required for search")
                
                collection_name = params.get("collection", "notes")
                top_k = params.get("top_k", 5)
                db_path = params.get("db_path")
                model = params.get("model")
                
                result = search_notes(query, collection_name, top_k, db_path, model)
            
            else:
                raise ValueError(f"Unknown action: {action}")
            
            if result.get("success") == False:
                print(format_error(result.get("error", "unknown_error"), {"message": result.get("message")}))
            else:
                print(format_success(result))
        
        else:
            print(format_error("Either --demo or --params must be provided"))
            sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == '__main__':
    main()
