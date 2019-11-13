from telethon import TelegramClient
import time

api_hash = '2965d2383226a927db5fefbbb6f60b21'
api_id = 1119261

client = TelegramClient('pyapp',api_id,api_hash)
async def main():
    # me = await client.get_me()
    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        if dialog.title == 'GeekUniversity_AI_201 (15.02.2019)':
            # await dialog.send_message('Hello 2')
            # async for msg in client.iter_messages(dialog):
                #     print(msg.text)
                #     time.sleep(1)
            members = await client.get_participants(dialog)

    for member in members:
        print(member.first_name, member.last_name)
    pass



with client:
   client.loop.run_until_complete(main())
