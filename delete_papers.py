import chromadb
from chromadb.config import Settings

c = chromadb.PersistentClient(path=r"data/chroma", settings=Settings(anonymized_telemetry=False))
try:
    c.delete_collection("papers")
    print("deleted papers collection")
except Exception as e:
    print("delete_collection error:", e)
