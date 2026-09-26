import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    #подключение к базе
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def find_url_by_name(name):
    #ищем сайт
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM urls WHERE name = %s;", (name,))
            return cur.fetchone()


def insert_url(name):
    #добавляем сайт
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls (name) VALUES (%s) RETURNING *;",
                (name,)
            )
            row = cur.fetchone()
            conn.commit()
            return row

def find_url_by_id(id_):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s;", (id_,))
            return cur.fetchone()


def get_all_urls():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    urls.id,
                    urls.name,
                    last_checks.created_at AS last_check_date,
                    last_checks.status_code AS last_status_code
                FROM urls
                LEFT JOIN (
                    SELECT DISTINCT ON (url_id) 
                        url_id, 
                        created_at, 
                        status_code
                    FROM url_checks
                    ORDER BY url_id, id DESC
                ) AS last_checks ON urls.id = last_checks.url_id
                ORDER BY urls.id DESC;
                """
            )
            return cur.fetchall()

def insert_check(url_id, status_code, h1, title, description):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO url_checks (url_id, status_code, h1, title, description)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (url_id, status_code, h1, title, description)
            )
            return cur.fetchone()


def get_checks_by_url_id(url_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC;
                """,
                (url_id,)
            )
            return cur.fetchall()