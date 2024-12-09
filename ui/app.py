import chainlit as cl

from src.app import chat_app
from ui.utils import generate_random_sender_id

sender_id = generate_random_sender_id()


@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()

    await cl.sleep(1)
    msg.content = await chat_app.chat(sender_id=sender_id, text=message.content)

    await msg.update()
