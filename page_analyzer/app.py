import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from page_analyzer.db import (find_url_by_name, insert_url, find_url_by_id,
                              get_all_urls, insert_check, get_checks_by_url_id)
from page_analyzer.url import normalize_url, validate_url
from page_analyzer.parser import extract_page_data

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')


@app.route('/')
def index():
    return render_template('index.html')

@app.post('/urls')
def urls_post():
    raw_url = request.form.get('url', '').strip()
    errors = validate_url(raw_url)

    if errors:
        flash('Некорректный URL', 'danger')
        return render_template('index.html', url=raw_url), 422

    normalized_url = normalize_url(raw_url)
    existing_url = find_url_by_name(normalized_url)

    if existing_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('url_detail', id=existing_url['id']))

    new_url = insert_url(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_detail', id=new_url['id']))

@app.get('/urls/<int:id>')
def url_detail(id):
    url = find_url_by_id(id)
    if not url:
        return render_template('404.html'), 404
    checks = get_checks_by_url_id(id)
    return render_template('url.html', url=url, checks=checks)


@app.get('/urls')
def urls_get():
    urls = get_all_urls()
    return render_template('urls.html', urls=urls)

@app.post('/urls/<int:id>/checks')
def url_checks_post(id):
    url = find_url_by_id(id)
    if not url:
        return render_template('404.html'), 404

    try:
        response = requests.get(url['name'], timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url_detail', id=id))

    page_data = extract_page_data(response.text)
    insert_check(
        id,
        response.status_code,
        page_data['h1'],
        page_data['title'],
        page_data['description'],
    )
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url_detail', id=id))