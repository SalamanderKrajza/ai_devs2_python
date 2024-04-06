import re
from typing import List, Dict
from langchain.docstore.document import Document

def extract_links_to_metadata(docs: List[Document]) -> List[Document]:
    for doc in docs:
        content = doc.page_content
        links = re.findall(r'\[.*?\]\((.*?)\)', content)
        unique_links = {}
        link_placeholders = {}
        
        for i, link in enumerate(links, start=1):
            if link not in unique_links:
                placeholder = f'${i}'
                unique_links[link] = placeholder
                link_placeholders[link] = placeholder
                doc.metadata['links'][f'link{i}'] = link
        
        for link, placeholder in link_placeholders.items():
            content = content.replace(f']({link})', f']({placeholder})')
        
        doc.page_content = content
    
    return docs