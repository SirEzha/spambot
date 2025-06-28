# ollama_check.py
import aiohttp

async def is_spam_with_ollama(message_text: str) -> bool:
    prompt = f"You are a spam checker for a Telegram chat. Your role is to check, whether the following message is spam or not. You will output your verdict in the following format: 'SPAM 0-10', where 0-10 is your confidence that given message is spam in a format of a single number. Examples of your answers: 'SPAM 8', 'SPAM 0'. Message: ''"
    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:11434/api/generate", json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }) as resp:
            data = await resp.json()
            reply = data['response'].strip().lower()
            return 'yes' in reply
