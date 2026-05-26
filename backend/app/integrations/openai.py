from openai import AsyncOpenAI

from app.config import get_settings

settings = get_settings()

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def generate_text(
    prompt: str,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = 4096,
) -> str:
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content or ""
