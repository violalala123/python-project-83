from bs4 import BeautifulSoup


def extract_page_data(html_text):

    soup = BeautifulSoup(html_text, 'html.parser')

    h1_tag = soup.find('h1')
    h1 = h1_tag.text.strip() if h1_tag else ''

    title_tag = soup.find('title')
    title = title_tag.text.strip() if title_tag else ''

    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = ''
    if description_tag and description_tag.get('content'):
        description = description_tag['content'].strip()

    return {
        'h1': h1,
        'title': title,
        'description': description,
    }