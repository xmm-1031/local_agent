from __future__ import annotations
import argparse
from pathlib import Path

from src.db import VectorDB
from src.utils import ensure_dir
from src.papers import PaperEngine
from src.images import ImageEngine

ROOT = Path(__file__).parent.resolve()
LIBRARY_DIR = ROOT / "library"
PAPERS_DIR = LIBRARY_DIR / "papers"
IMAGES_DIR = LIBRARY_DIR / "images"
DB_DIR = ROOT / "data" / "chroma"

def parse_topics(s: str) -> list[str]:
    topics = [t.strip() for t in s.split(",") if t.strip()]
    if not topics:
        raise ValueError("topics 不能为空，例如：--topics \"CV,NLP,RL\"")
    return topics

def cmd_add_paper(args):
    ensure_dir(PAPERS_DIR); ensure_dir(DB_DIR)
    vdb = VectorDB(DB_DIR)
    papers_col = vdb.get_or_create("papers")

    engine = PaperEngine()
    topics = parse_topics(args.topics)

    res = engine.add_paper(papers_col, Path(args.path), topics, PAPERS_DIR)
    print("add_paper 完成：")
    print(res)

def cmd_search_paper(args):
    ensure_dir(DB_DIR)
    vdb = VectorDB(DB_DIR)
    papers_col = vdb.get_or_create("papers")

    engine = PaperEngine()
    results = engine.search_paper(papers_col, args.query, top_k=args.top_k)

    print(f"search_paper: {args.query}")
    for i, r in enumerate(results, 1):
        print(f"{i}. score={r.score:.4f} topic={r.topic} page={r.page} chunk={r.chunk} path={r.path}")
        if args.show_snippet and r.snippet:
            print(f"   snippet: {r.snippet}")

def cmd_organize_folder(args):
    ensure_dir(PAPERS_DIR); ensure_dir(DB_DIR)
    vdb = VectorDB(DB_DIR)
    papers_col = vdb.get_or_create("papers")

    engine = PaperEngine()
    topics = parse_topics(args.topics)

    done = engine.organize_folder(papers_col, Path(args.folder), topics, PAPERS_DIR)
    print(f"organize_folder 完成：共处理 {len(done)} 个PDF")
    for x in done[:5]:
        print(" -", x)
    if len(done) > 5:
        print(" ...")

def cmd_search_image(args):
    ensure_dir(DB_DIR); ensure_dir(IMAGES_DIR)
    vdb = VectorDB(DB_DIR)
    images_col = vdb.get_or_create("images")

    engine = ImageEngine()

    # 如果库是空的：先索引一次本地图片库
    try:
        if images_col.count() == 0:
            print("🧱 images index is empty, indexing library/images ...")
            engine.index_folder(images_col, IMAGES_DIR, batch_size=16)
    except Exception:
        pass

    results = engine.search_image(images_col, args.query, top_k=args.top_k)

    print(f"search_image: {args.query}")
    for i, r in enumerate(results, 1):
        print(f"{i}. score={r.score:.4f} norm={r.norm_score:.4f} path={r.path}")


def main():
    parser = argparse.ArgumentParser("Local Multimodal AI Agent")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("add_paper", help="添加/分类论文PDF")
    p1.add_argument("path", type=str)
    p1.add_argument("--topics", type=str, required=True)
    p1.set_defaults(func=cmd_add_paper)

    p2 = sub.add_parser("search_paper", help="语义搜索论文")
    p2.add_argument("query", type=str)
    p2.add_argument("--top_k", type=int, default=5)
    p2.add_argument("--show_snippet", action="store_true")
    p2.set_defaults(func=cmd_search_paper)

    p3 = sub.add_parser("search_image", help="以文搜图")
    p3.add_argument("query", type=str)
    p3.add_argument("--top_k", type=int, default=5)
    p3.set_defaults(func=cmd_search_image)

    # 附加命令：批量整理（README提到的一键整理） :contentReference[oaicite:13]{index=13}
    p4 = sub.add_parser("organize_folder", help="一键整理某个PDF文件夹")
    p4.add_argument("folder", type=str)
    p4.add_argument("--topics", type=str, required=True)
    p4.set_defaults(func=cmd_organize_folder)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
