from langchain.docstore.document import Document
from typing import List

def search_docs(docs: List[Document], keywords: List[str]) -> List[Document]:
    def filter_func(doc: Document) -> bool:
        for keyword in keywords:
            # remove punctuation
            keyword = ''.join(char for char in keyword if char.isalnum())
            if keyword.lower() in doc.page_content.lower() and len(keyword) > 3:
                print('Found:' + keyword)
                return True
        return False

    # filter() returns these [elements from docs] that all labeled True by filter_finc
    return list(filter(filter_func, docs))
