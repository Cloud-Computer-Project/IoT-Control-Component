# src/deps.py
from fastapi import Request
from .storage import InMemoryStore

def get_store(request: Request) -> InMemoryStore:
    return request.app.state.store
