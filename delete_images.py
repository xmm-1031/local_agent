import chromadb
from chromadb.config import Settings

c = chromadb.PersistentClient(path="data/chroma", settings=Settings(anonymized_telemetry=False))
try:
    c.delete_collection("images")
    print("deleted images collection")
except Exception as e:
    print("delete_collection error:", e)
