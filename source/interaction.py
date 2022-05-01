import random
import aiohttp

class Post_Interaction:
    def __init__(self):
        pass


    async def interact_with_post(self, session: aiohttp.ClientSession, post_id, user_xuid, token):
        try:
            chosen_message = self.choose_message()
            headers = {
                'x-xbl-contract-version': '107',
                'Accept': 'application/json',
                'Accept-Language': 'en-US',
                'Authorization': token
            }
            json = {
                "members":{
                   "me":{
                       "constants":{
                            "system":{
                                "initialize":True,
                                "xuid": user_xuid
                            }
                        },
                        "properties":{
                            "system":{
                                "description":{
                                    "text": chosen_message,
                                    "locale":"en"
                                }
                            }
                        }
                    }
                }
            }
            async with session.put(f'https://sessiondirectory.xboxlive.com/handles/{post_id}/session', headers=headers, json=json) as post_interaction:
                return post_interaction.status, chosen_message
        except Exception as e:
            print(f' \x1b[1;39m[\x1b[1;31m!\x1b[1;39m] Failed to interact with post | ID: \x1b[1;33m{post_id}\x1b[1;39m | Error: \x1b[1;31m{e}\x1b[1;39m')
            return None, None
        

    def choose_message(self):
        with open('message_lists/messages.txt', 'r') as messages:
            return random.choice(messages.readlines()).strip()