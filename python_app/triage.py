from dataclasses import dataclass

from sentence_transformers import SentenceTransformer, util
import streamlit as st

from config import (
    DEPARTMENTS,
    EMBEDDING_MODEL,
    GENERAL_SERVICES,
    ROUTING_THRESHOLD,
    URGENT_KEYWORDS,
)


@dataclass(frozen=True)
class TriageResult:
    department: str
    priority: str


@st.cache_resource(show_spinner="Loading the routing model (first run only)...")
def _load_router():
    model = SentenceTransformer(EMBEDDING_MODEL)
    names = [name for name in DEPARTMENTS if name != GENERAL_SERVICES]
    descriptions = [f"{name}: {DEPARTMENTS[name]['summary']}" for name in names]
    embeddings = model.encode(descriptions, convert_to_tensor=True)
    return model, names, embeddings


def triage_report(title: str, description: str) -> TriageResult:
    model, names, department_embeddings = _load_router()
    text = f"{title}. {description}"

    query_embedding = model.encode(text, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, department_embeddings)[0]
    best_index = int(scores.argmax())
    best_score = float(scores[best_index])

    department = names[best_index] if best_score >= ROUTING_THRESHOLD else GENERAL_SERVICES
    lowered = text.lower()
    priority = "urgent" if any(keyword in lowered for keyword in URGENT_KEYWORDS) else "normal"
    return TriageResult(department=department, priority=priority)
