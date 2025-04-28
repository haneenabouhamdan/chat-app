import asyncio
from typing import Dict

active_connections: Dict[str, asyncio.Queue] = {}

def add_connection(user_id: str, queue: asyncio.Queue):
    active_connections[user_id] = queue

def remove_connection(user_id: str):
    active_connections.pop(user_id, None)

def send_message_to_user(user_id: str, message: str):
    if user_id in active_connections:
        active_connections[user_id].put_nowait(message)
