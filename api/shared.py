import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI

def _get(name: str, fallback: str | None = None):
    # Hem OPENAI_ENDPOINT hem OPENAIENDPOINT vb. destekle
    return os.getenv(name) or (fallback and os.getenv(fallback))

def get_search_client():
    endpoint = _get("SEARCH_ENDPOINT", "SEARCHENDPOINT")
    index    = _get("SEARCH_INDEX",    "SEARCHINDEX") or "arkgpt-kb"
    key      = _get("SEARCH_KEY",      "SEARCHKEY")
    if not (endpoint and key):
        raise RuntimeError("SEARCH_ENDPOINT/SEARCH_KEY (veya SEARCHENDPOINT/SEARCHKEY) eksik")
    return SearchClient(endpoint=endpoint, index_name=index, credential=AzureKeyCredential(key))

def get_openai_client():
    endpoint = _get("OPENAI_ENDPOINT", "OPENAIENDPOINT")
    api_key  = _get("OPENAI_API_KEY",  "OPENAIAPIKEY")
    if not (endpoint and api_key):
        raise RuntimeError("OPENAI_ENDPOINT/OPENAI_API_KEY (veya OPENAIENDPOINT/OPENAIAPIKEY) eksik")
    return AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2024-06-01")