import os
import time
from datetime import datetime

import psycopg2
from fastapi import FastAPI, HTTPException, Query
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


DB_NAME = os.getenv("DB_NAME", "parser_db")
DB_USER = os.getenv("DB_USER", "parser_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "parser_password")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
CHROME_BIN = os.getenv("CHROME_BIN", "/usr/bin/chromium")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")

app = FastAPI(title="Task7 Parser")


def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )


def init_db():
    last_error = None

    for _ in range(10):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS parsed_items (
                            id SERIAL PRIMARY KEY,
                            source_url TEXT NOT NULL,
                            title TEXT NOT NULL,
                            url TEXT NOT NULL,
                            page INTEGER NOT NULL,
                            collected_at TIMESTAMP NOT NULL
                        )
                        """
                    )
            return
        except psycopg2.OperationalError as exc:
            last_error = exc
            time.sleep(3)

    raise RuntimeError(f"Database is unavailable: {last_error}") from last_error


def create_driver():
    options = Options()
    options.binary_location = CHROME_BIN
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(executable_path=CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)


def parse_wiki_category(start_url, max_pages=5):
    rows = []
    page = 1
    current_url = start_url
    driver = create_driver()

    try:
        while current_url and page <= max_pages:
            driver.get(current_url)
            time.sleep(2)

            for element in driver.find_elements(By.CSS_SELECTOR, ".mw-category-group a"):
                title = (element.text or "").strip()
                href = element.get_attribute("href")
                if not title or not href:
                    continue

                rows.append(
                    {
                        "title": title,
                        "url": href,
                        "page": page,
                        "collected_at": datetime.utcnow(),
                    }
                )

            next_url = None
            for element in driver.find_elements(By.CSS_SELECTOR, "#mw-pages a"):
                text = (element.text or "").strip().lower()
                if text in {"следующая страница", "next page"}:
                    next_url = element.get_attribute("href")
                    break

            current_url = next_url
            page += 1
    finally:
        driver.quit()

    return rows


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/parse")
def parse(url=Query(...), max_pages=Query(5, ge=1, le=50)):
    try:
        rows = parse_wiki_category(url, max_pages=max_pages)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Parser failed: {exc}") from exc

    if not rows:
        return {"saved": 0}

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO parsed_items (source_url, title, url, page, collected_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [
                    (url, row["title"], row["url"], row["page"], row["collected_at"])
                    for row in rows
                ],
            )

    return {"saved": len(rows)}


@app.get("/items")
def items(limit=Query(100, ge=1, le=1000)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, source_url, title, url, page, collected_at
                FROM parsed_items
                ORDER BY id DESC
                LIMIT %s
                """,
                (limit,),
            )
            data = cur.fetchall()

    return [
        {
            "id": row[0],
            "source_url": row[1],
            "title": row[2],
            "url": row[3],
            "page": row[4],
            "collected_at": row[5],
        }
        for row in data
    ]
