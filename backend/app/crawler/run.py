"""Manual crawl entry point: python -m app.crawler.run"""
from app.database import SessionLocal
from app.services.crawler import crawl_all_feeds
from app.services.matcher import clear_cache


def main():
    clear_cache()
    db = SessionLocal()
    try:
        stats = crawl_all_feeds(db)
        print(f"Crawl results: {stats}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
