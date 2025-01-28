import ollama
import requests

response_llm = ollama.chat(
    model="sharkboo",
    messages=[
        {"role": "user", "content": "tell me a joke"}
        ]
)

print(response_llm["message"]["content"])