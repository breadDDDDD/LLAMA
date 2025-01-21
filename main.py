from ollama import chat
from ollama import ChatResponse
from llama_parse import LlamaParse 
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.core.embeddings import resolve_embed_models

response: ChatResponse = chat(
    model ="llama3.2",
    messages=[{
        'role': 'user',
        'content': 'what are u'
    },
    ]
)
print(response.message.content)