"""
Vector store module.
Converts participant profiles into dense embeddings and indexes them using FAISS for semantic similarity retrieval.
"""

from typing import Any, Dict, List, Tuple
import numpy as np

_EMBEDDER = None


def get_embedder():
    """Lazy load sentence transformers model."""
    global _EMBEDDER
    if _EMBEDDER is None:
        try:
            from sentence_transformers import SentenceTransformer
            _EMBEDDER = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as e:
            print(f"SentenceTransformer not loaded (using TF-IDF fallback): {e}")
            _EMBEDDER = False
    return _EMBEDDER


def profile_to_text(profile: Dict[str, Any]) -> str:
    """Format a profile into a dense descriptive string for semantic embedding."""
    name = profile.get("name", "")
    role = profile.get("primary_role", "")
    skills = " ".join(profile.get("skills", []))
    bio = profile.get("summary", "") or profile.get("bio", "")
    superpower = profile.get("superpower", "")
    return f"Role: {role}. Skills: {skills}. Superpower: {superpower}. Bio: {bio}"


def project_to_text(project: Dict[str, Any]) -> str:
    """Format project requirements into a query text for retrieval."""
    summary = project.get("summary", "")
    capabilities = " ".join(project.get("critical_capabilities", []))
    roles = " ".join(project.get("required_roles", []))
    return f"Project: {summary}. Capabilities: {capabilities}. Roles: {roles}"


def build_profile_index(profiles: List[Dict[str, Any]]) -> Tuple[Any, List[Dict[str, Any]]]:
    """Build a FAISS normalized inner-product index over participant profiles."""
    if not profiles:
        return None, []

    texts = [profile_to_text(p) for p in profiles]
    embedder = get_embedder()

    if embedder:
        embeddings = embedder.encode(texts, convert_to_numpy=True)
        # Normalize for cosine similarity via inner product
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1e-9
        normalized = embeddings / norms

        import faiss
        dim = normalized.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(normalized.astype(np.float32))
        return index, profiles
    else:
        # Fallback keyword match score index
        return "fallback", profiles


def search_candidates(index: Any, profiles: List[Dict[str, Any]], project: Dict[str, Any], top_k: int = 10) -> List[Dict[str, Any]]:
    """Search and rank top matching candidates for a project."""
    if not profiles:
        return []

    query_text = project_to_text(project)
    embedder = get_embedder()

    if index != "fallback" and embedder:
        q_emb = embedder.encode([query_text], convert_to_numpy=True)
        q_norm = q_emb / max(np.linalg.norm(q_emb), 1e-9)

        k = min(top_k, len(profiles))
        distances, indices = index.search(q_norm.astype(np.float32), k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(profiles):
                candidate = dict(profiles[idx])
                # Scale cosine distance (-1..1) to 0..100 percentage
                candidate["semantic_score"] = round(float((dist + 1.0) / 2.0 * 100), 1)
                results.append(candidate)
        return results
    else:
        # Keyword heuristic relevance scoring
        results = []
        q_lower = query_text.lower()
        for p in profiles:
            p_text = profile_to_text(p).lower()
            score = 50.0
            for word in q_lower.split():
                if len(word) > 3 and word in p_text:
                    score += 5.0
            candidate = dict(p)
            candidate["semantic_score"] = min(98.0, score)
            results.append(candidate)
        results.sort(key=lambda x: x["semantic_score"], reverse=True)
        return results[:top_k]
