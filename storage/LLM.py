import ollama

def questionAnswer(context: str, question: str):
    response = ollama.chat(model="qwen2.5-coder:7b", messages=[
        {
                "role": "system",
                "content": """You are a code assistant helping users understand a GitHub repository.
Answer questions using only the provided code context.
Always reference specific file paths and function names in your answers.
If the answer isn't in the context, say so clearly."""
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
    ])
    return (response.message.content)