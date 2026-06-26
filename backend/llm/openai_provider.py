from openai import OpenAI
from backend.llm.base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o", base_url: str | None = None, disable_thinking: bool = False):
        kwargs = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        self.client = OpenAI(**kwargs)
        self.model = model
        self.disable_thinking = disable_thinking

    def chat(self, system_prompt: str, user_message: str) -> str:
        kwargs = dict(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=2048,
        )
        if self.disable_thinking:
            kwargs["extra_body"] = {"thinking": {"type": "disabled"}}
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
