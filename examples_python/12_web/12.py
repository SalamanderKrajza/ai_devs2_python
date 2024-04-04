import json
import re
from requests_html import HTMLSession
import html2text

class CustomWebLoader:
    def __init__(self, url, selector):
        self.url = url
        self.selector = selector

    def load(self):
        session = HTMLSession()
        response = session.get(self.url)
        element = response.html.find(self.selector, first=True)
        if element:
            html_content = element.html
            markdown_content = html2text.html2text(html_content)
            return [{"page_content": markdown_content, "metadata": {}}]
        else:
            return []

loader = CustomWebLoader("https://brain.overment.com", ".main")
docs = loader.load()

def replace_urls(doc):
    url_to_placeholder = {}

    def replace_url(match):
        url = match.group(0)
        if url not in url_to_placeholder:
            placeholder = f"${len(url_to_placeholder) + 1}"
            url_to_placeholder[url] = placeholder
            doc["metadata"][placeholder] = url
        return url_to_placeholder[url]

    doc["page_content"] = re.sub(r"((http|https):\/\/[^\s]+|\.\/[^\s]+)(?=\))", replace_url, doc["page_content"])

for doc in docs:
    replace_urls(doc)

with open("docs.json", "w") as f:
    json.dump(docs, f, indent=2)
