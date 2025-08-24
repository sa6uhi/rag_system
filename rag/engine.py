import google.generativeai as genai
from typing import List, Dict, Tuple
import logging
from config import Config
from processing.document_processor import LegalDocumentProcessor
from rag.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGEngine:
    """Main RAG engine for legal question answering"""
    
    def __init__(self):
        self.config = Config()
        self.processor = LegalDocumentProcessor()
        self.vector_store = VectorStore()
        self.model = None
        
        if self.config.GEMINI_API_KEY:
            genai.configure(api_key=self.config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            logger.info("Gemini model initialized")
        else:
            logger.warning("Gemini API key not found. RAG engine will work in fallback mode.")
            
        self._initialize_documents()
        
    def _initialize_documents(self) -> None:
        """Load and index legal documents"""
        logger.info("Initializing legal documents...")
        
        documents = self.processor.load_documents()
        
        self.vector_store.add_documents(documents)
        
        logger.info(f"Indexed {self.vector_store.get_document_count()} documents")
        
    def search_documents(self, query: str, top_k: int = None) -> List[Tuple[Dict, float]]:
        """Search for relevant documents"""
        if top_k is None:
            top_k = self.config.TOP_K_RESULTS
            
        return self.vector_store.search(
            query=query,
            top_k=top_k,
            threshold=self.config.SIMILARITY_THRESHOLD
        )
        
    def generate_answer(self, query: str, context_docs: List[Tuple[Dict, float]] = None) -> str:
        """Generate answer using RAG approach"""
        if context_docs is None:
            context_docs = self.search_documents(query)
            
        context_text = "\n\n".join([
            f"[Mənbə #{i+1} (Uyğunluq: {score:.2f})]\nID: {doc['id']}\nNöv: {doc['type']}\nMəzmun: {doc['content']}\nMetadata: {doc['metadata']}" 
            for i, (doc, score) in enumerate(context_docs)
        ])
        
        prompt = self._create_prompt(query, context_text)
        
        if self.model:
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                logger.error(f"Error generating response with Gemini: {e}")
                return self._fallback_response(query, context_text)
        else:
            return self._fallback_response(query, context_text)
            
    def _create_prompt(self, query: str, context: str) -> str:
        """Create prompt for the language model"""
        prompt = f"""Siz Azərbaycan Respublikasının Cinayət Məcəlləsi üzrə həqiqi hüquq mütəxəssisinin rolunu oynayırsınız. Aşağıdakı suala cavab verməlisiniz:

Sual: {query}

Aşağıdakı mənbələrdən istifadə edərək cavab verin:

{context}

Təlimatlar:
1. Cavabınızı yalnız verilmiş mənbələrə əsasən verin
2. Cavabınız Azərbaycan dilində olmalıdır
3. Mümkün qədər dəqiq və ətraflı olun
4. Mənbələri göstərin (məsələn: "Maddə 1.1-ə əsasən...")
5. Əgər cavab mənbələrdə tamamilə yoxdursa, lakin bəzi əlaqəli məlumatlar varsa, bu məlumatları təqdim edin və çatışmadığını bildirin
6. Əgər mənbələrdə heç bir əlaqəli məlumat yoxdursa, "Mənbələrdə bu suala cavab tapılmadı" deyin
7. Hər bir məqaləni və ya bəndi dəqiq göstərin
8. Əgər suala tam cavab yoxdursa, ən yaxın məlumatları təqdim edin

Cavab:"""
        
        return prompt
        
    def _fallback_response(self, query: str, context: str) -> str:
        """Fallback response when LLM is not available"""
        if len(context.strip()) < 50:
            return f"""Hazırda sualınıza dəqiq cavab tapa bilmədik. Bu, aşağıdakı səbəblərdən biri ola bilər:

1. Sualınızla əlaqəli məlumat mənbələrimizdə mövcud deyil
2. Sualınızın ifadəsi mənbələrdə istifadə olunan terminlərdən fərqlidir

Təkliflərimiz:
- Sualınızı fərqli şəkildə ifadə etməyinizi tövsiyyə edirik
- Məsələn, "cinayət törətmək" əvəzinə "cinayətin tərkibi" və ya konkret məqalələri qeyd etməyinizi tövsiyyə edirik

Əgər hüquqi məsləhət lazımdırsa, hüquq mütəxəssisinə müraciət etməyinizi tövsiyyə edirik."""

        return f"""Təəssüf ki, hazırda cavab yaratmaq mümkün deyil. Ancaq verilən sual üzrə mənbələrdən tapılan məlumatlar:

Sual: {query}

Tapılan məlumatlar:
{context[:1000]}...

Ətraflı məlumat üçün hüquq mütəxəssisinə müraciət edin."""

    def get_document_stats(self) -> Dict[str, int]:
        """Get statistics about indexed documents"""
        return {
            'total_documents': self.vector_store.get_document_count()
        }

rag_engine = None

def get_rag_engine() -> RAGEngine:
    """Get singleton instance of RAG engine"""
    global rag_engine
    if rag_engine is None:
        rag_engine = RAGEngine()
    return rag_engine

if __name__ == "__main__":
    engine = get_rag_engine()
    
    print("RAG Engine initialized")
    stats = engine.get_document_stats()
    print(f"Document stats: {stats}")
    
    test_query = "Cinayət törətmək üçün hansı şərtlər vardır?"
    print(f"\nTest query: {test_query}")
    
    results = engine.search_documents(test_query)
    print(f"Found {len(results)} relevant documents")
    
    answer = engine.generate_answer(test_query, results)
    print(f"\nGenerated answer:\n{answer}")
