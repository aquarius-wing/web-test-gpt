import os
import sys
from claude_api import Client


def ask_claude(prompt: str, attachment=None, attachments=None):
    cookie = os.getenv('CLAUDE_COOKIE')
    claude_api = Client(cookie)
    conversation_id = claude_api.create_new_chat()['uuid']
    response = claude_api.send_message(prompt, conversation_id, attachment=attachment, attachments=attachments)
    return response


if __name__ == '__main__':
    ask_claude('hello')
