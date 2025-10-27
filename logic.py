import os
from ..shared import get_search_client, get_openai_client, chat_answer

def handle_ask(q: str):
    search = get_search_client()
    results = search.search(q, top=5)

    snippets, citations = [], []
    for r in results:
        snippets.append(r.get("content",""))
        citations.append({"title": r.get("title",""), "url": r.get("url","")})

    context = "\n\n---\n\n".join(snippets) if snippets else "No matching context."
    prompt = (
        "You are Arkgpt. Answer ONLY using the context below. "
        "If the context is insufficient, say what is missing.\n\n"
        f"Context:\n{context}\n\nQuestion: {q}\nAnswer:"
    )
    aoai = get_openai_client()
    deployment = os.getenv("CHATMODELDEPLOYMENT", "gpt-4o-mini")
    answer = chat_answer(aoai, deployment, prompt)
    return answer, citations