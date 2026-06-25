from backend.llm import get_provider

COACH_SYSTEM_PROMPT = """You are a friendly career coach helping a software engineer document their daily work experience.
Your goal: guide them to reflect on what they did, extract meaningful details.

Rules:
1. Keep it conversational. Ask one question at a time.
2. After they describe something, ask a follow-up to get specifics: what technology, what was the outcome, any numbers?
3. When they've provided enough detail (tech + outcome), acknowledge and suggest they've done a great job recording.
4. Always end with a question to keep the conversation going.
5. Be encouraging. This is for their own growth, not an interrogation.

Respond in Chinese (the user speaks Chinese)."""


def get_coach_response(user_message: str, conversation_history: list[dict] = None) -> str:
    """Generate the next coach message based on conversation context."""
    provider = get_provider()
    history = conversation_history or []
    messages = []
    for msg in history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})

    if len(messages) == 1:
        response = provider.chat(COACH_SYSTEM_PROMPT, user_message)
    else:
        full_context = "\n".join([f"{'用户' if m['role']=='user' else '教练'}: {m['content']}" for m in messages])
        response = provider.chat(COACH_SYSTEM_PROMPT, full_context)
    return response
