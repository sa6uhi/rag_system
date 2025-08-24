import json
import os
from typing import List, Dict, Any
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalDocumentProcessor:
    """Processes legal documents from JSON files"""
    
    def __init__(self):
        self.config = Config()
        self.documents = []
        
    def load_documents(self) -> List[Dict[str, Any]]:
        """Load documents from JSON files"""
        logger.info("Loading documents from JSON files...")
        
        # Load structured JSON file
        if os.path.exists(self.config.STRUCTURED_JSON_FILE):
            with open(self.config.STRUCTURED_JSON_FILE, 'r', encoding='utf-8') as f:
                structured_data = json.load(f)
                self.documents.extend(self._process_structured_data(structured_data))
                
        # Load output JSON file
        if os.path.exists(self.config.OUTPUT_JSON_FILE):
            with open(self.config.OUTPUT_JSON_FILE, 'r', encoding='utf-8') as f:
                output_data = json.load(f)
                self.documents.extend(self._process_output_data(output_data))
                
        logger.info(f"Loaded {len(self.documents)} document sections")
        return self.documents
    
    def _process_structured_data(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process structured JSON data into document sections"""
        documents = []
        
        # Process the main title
        if 'title' in data:
            documents.append({
                'id': 'title',
                'content': data['title'],
                'type': 'title',
                'metadata': {}
            })
            
        # Process sections
        if 'sections' in data:
            for section in data['sections']:
                section_id = f"section_{section.get('section_number', '')}"
                section_title = section.get('section_title', '')
                
                documents.append({
                    'id': section_id,
                    'content': section_title,
                    'type': 'section',
                    'metadata': {
                        'section_number': section.get('section_number', ''),
                        'section_title': section_title
                    }
                })
                
                # Process chapters in each section
                if 'chapters' in section:
                    for chapter in section['chapters']:
                        chapter_id = f"{section_id}_chapter_{chapter.get('chapter_number', '')}"
                        chapter_title = chapter.get('chapter_title', '')
                        
                        documents.append({
                            'id': chapter_id,
                            'content': chapter_title,
                            'type': 'chapter',
                            'metadata': {
                                'section_number': section.get('section_number', ''),
                                'chapter_number': chapter.get('chapter_number', ''),
                                'chapter_title': chapter_title
                            }
                        })
                        
                        # Process articles in each chapter
                        if 'articles' in chapter:
                            for article in chapter['articles']:
                                article_id = f"{chapter_id}_article_{article.get('article_number', '')}"
                                article_heading = article.get('article_heading', '')
                                
                                # Combine heading with content
                                article_content = article_heading + "\n"
                                if 'content' in article:
                                    article_content += "\n".join(article['content'])
                                    
                                documents.append({
                                    'id': article_id,
                                    'content': article_content,
                                    'type': 'article',
                                    'metadata': {
                                        'section_number': section.get('section_number', ''),
                                        'chapter_number': chapter.get('chapter_number', ''),
                                        'article_number': article.get('article_number', ''),
                                        'article_heading': article_heading
                                    }
                                })
                                
        return documents
    
    def _process_output_data(self, data: List[Any]) -> List[Dict[str, Any]]:
        """Process output JSON data into document sections"""
        documents = []
        
        # The output.json appears to be a different format, we'll treat it as raw text chunks
        # For now, we'll create simple document chunks
        content_str = ""
        for item in data[:100]:  # Limiting to first 100 items to avoid too much data
            if isinstance(item, str):
                content_str += item + "\n"
                
        # Split into chunks
        chunk_size = self.config.CHUNK_SIZE
        for i in range(0, len(content_str), chunk_size):
            chunk = content_str[i:i+chunk_size]
            if chunk.strip():
                documents.append({
                    'id': f'chunk_{len(documents)}',
                    'content': chunk,
                    'type': 'chunk',
                    'metadata': {
                        'source': 'output_json',
                        'chunk_index': len(documents)
                    }
                })
                
        return documents

if __name__ == "__main__":
    processor = LegalDocumentProcessor()
    docs = processor.load_documents()
    print(f"Processed {len(docs)} documents")
    if docs:
        print("Sample document:")
        print(f"ID: {docs[0]['id']}")
        print(f"Content: {docs[0]['content'][:200]}...")
        print(f"Type: {docs[0]['type']}")
        print(f"Metadata: {docs[0]['metadata']}")
