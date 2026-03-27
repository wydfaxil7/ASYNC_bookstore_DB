import os
from groq import Groq
import asyncio

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def call_groq(prompt: str):
    """
    Async wrapper for groq API
    """
    def _call():
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content

    return await asyncio.to_thread(_call)