
import os
from claude_api import Client

def ask_claude(prompt: str, attachment = None):
    cookie = os.getenv('CLAUDE_COOKIE')
    claude_api = Client(cookie)
    conversation_id = claude_api.create_new_chat()['uuid']
    if attachment is not None:
        response = claude_api.send_message(prompt, conversation_id, attachment=attachment)
        return response
    else:
        response = claude_api.send_message(prompt, conversation_id)
        return response