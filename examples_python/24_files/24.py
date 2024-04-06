from langchain.document_loaders import TextLoader
import html2text
from bs4 import BeautifulSoup
import json
import re
from typing import List
from langchain.docstore.document import Document
from helpers import extract_links_to_metadata

# --------------------------------------------------------------
# Load html from file (Normally it would be scrapped)
# --------------------------------------------------------------
loader = TextLoader("aidevs.html", encoding="utf-8")
html = loader.load()[0]

# --------------------------------------------------------------
# Extract only desired section (we want analyze only part of the page)
# --------------------------------------------------------------
soup = BeautifulSoup(html.page_content, 'html.parser')
authors = soup.select_one("#instructors")

# --------------------------------------------------------------
# Convert to markdown to make it cleaner before seraching for its content
# --------------------------------------------------------------
authors_html = str(authors) if authors else ''
markdown = html2text.html2text(authors_html)
with open("aidevs.md", 'w', encoding="utf-8") as file: file.write(markdown)
# --------------------------------------------------------------
# Split content to sections
# --------------------------------------------------------------
# NOTE: Regex from course didn't worked for me. 
# Possibly due to different lib that extract markdown from html
# I've tested few options but decided to spilt text just by ".jpeg)"
# as image was at beggining of each author box. 
# Keep in mind that we don't save the image url in that way 
# 
# 
# chunks = re.split(r'(?m)^###\s.*$', markdown)
# chunks = markdown.split("###")[1:]
chunks = markdown.split(".jpeg)")[1:]

# --------------------------------------------------------------
# Create docs with metadata basing on splitted markdown
# --------------------------------------------------------------
docs = []
for chunk in chunks:
    # Extract author name
    author_match = re.search(r'### (.*(?:\n.*)?) ', chunk)
    author = author_match.group(1).replace(' \n', '').strip() if author_match else ''

    # --------------------------------------------------------------
    # Create metadata for author
    # --------------------------------------------------------------
    # NOTE: In typescript there was IDocMetadata object but while i was looking 
    # for python implementation it seems overcomplicated: suggested creating neww class
    # inherit from Document, call its init, make some changes etc 
    # So i decided to stick with dict
    metadata = {
        'source': 'aidevs',
        'section': 'instructors',
        'author': author,
        'links': {},
    }

    # get all links in the chunk
    doc = Document(
        page_content=re.sub(r'[\n\\]', '', chunk).replace(r'\s{2,}', ' '),
        metadata=metadata
    )
    docs.append(doc)

# --------------------------------------------------------------
# Filter docs by some condition
# --------------------------------------------------------------
# I am not sure, maybe it's useful if i dont add [1:] into split
# but my frist chunk is longer than 50 characters so i am not sure if that was a reason
docs_filtered = [doc for doc in docs if len(doc.page_content) > 50] 
print("Are they the same?", docs == docs_filtered)

# --------------------------------------------------------------
# Extract links 
# --------------------------------------------------------------
docs = extract_links_to_metadata(docs)

# --------------------------------------------------------------
# Save links to json
# --------------------------------------------------------------
with open('aidevs.json', 'w') as f:
    json.dump([doc.dict() for doc in docs], f, indent=2)

