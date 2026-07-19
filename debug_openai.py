import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
key = os.getenv('OPENAI_API_KEY')
print('OPENAI_API_KEY present:', bool(key))
print('OPENAI_API_KEY sample:', key[:8] + '...' if key else None)
client = OpenAI(api_key=key)
try:
    resp = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': 'Say hi'}],
        max_tokens=5,
        temperature=0
    )
    print('SUCCESS:', resp.choices[0].message.content)
except Exception as e:
    print('EXCEPTION:', type(e).__name__)
    print(e)
    import traceback
    traceback.print_exc()
