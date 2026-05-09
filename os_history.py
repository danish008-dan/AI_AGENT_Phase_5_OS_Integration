# os_layer/os_history.py

from collections import deque

history_store = deque(maxlen=100)

def add_history(entry):
    history_store.append(entry)

def get_history():
    return list(history_store)