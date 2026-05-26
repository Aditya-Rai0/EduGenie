from langchain_openai import ChatOpenAI

from app.config import get_settings

settings = get_settings()

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=settings.OPENAI_API_KEY,
)
