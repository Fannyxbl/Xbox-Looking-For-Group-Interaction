import asyncio
import aiohttp
import colorama
import os
import getpass
import time
from source import user_info, interaction, post_collection

class Xbox_LFG_Interaction:
    def __init__ (self):
        self.authorization_token = ''
        self.user_xuid = ''
        self.done = []
        self.filtered_tags = self.collect_tags()

    async def interaction_loop(self):
        session = aiohttp.ClientSession()
        while True:
            status_code, response_data = await post_collection.LFG_Post_Collector().retrieve_posts(session, self.authorization_token)
            if status_code == 200:
                for result in range(len(response_data['results'])):
                    post_id = response_data['results'][result]['id']
                    post_tags = response_data['results'][result]['searchAttributes']['tags']
                    found_tags = await self.check_tags(post_tags)
                    
                    if post_id not in self.done and found_tags:
                        interaction_status, message = await interaction.Post_Interaction().interact_with_post(session, post_id, self.user_xuid, self.authorization_token)
                        if interaction_status == 200:
                            print(f' \x1b[1;39m[\x1b[1;36m+\x1b[1;39m] Successfully interacted with post [\x1b[1;36m{post_id}\x1b[1;39m] | Message: [\x1b[1;33m{message}\x1b[1;39m] ')
                        elif interaction_status == None:
                            pass
                        else:
                            print(f' \x1b[1;39m[\x1b[1;31m!\x1b[1;39m] Failed to interact with post [\x1b[1;33m{post_id}\x1b[1;39m]')
                        self.done.append(post_id)
                    else:
                        pass
            elif status_code == 401:
                print(' \x1b[1;39m[\x1b[1;31m!\x1b[1;39m] Authorization Token is invalid!')
                self.authorization_token = getpass.getpass(' \x1b[1;39m[\x1b[1;36m?\x1b[1;39m] Update Authorization Token: ');print('')
            elif status_code == None:
                pass
            else:
                print(' \x1b[1;39m[\x1b[1;31m!\x1b[1;39m] Failed to retrieve recent posts')
            

    async def startup(self):
        colorama.init(autoreset=True)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(' \x1b[1;39m[\x1b[1;36m*\x1b[1;39m] Xbox LFG Automatic Interaction\n')
        self.authorization_token = getpass.getpass(' \x1b[1;39m[\x1b[1;36m?\x1b[1;39m] Authorization Token: ');print('')
        time.sleep(2)
        session = aiohttp.ClientSession()
        self.user_xuid = await user_info.User_Info().retrieve_user_info(session, self.authorization_token)
        await self.interaction_loop()
    

    async def check_tags(self, post_tags):
        if post_tags is not None and len(self.filtered_tags) > 0:
            for tag in post_tags:
                if tag.lower().strip().replace(' ', '') in self.filtered_tags:
                    return True
            return False
        elif len(self.filtered_tags) <= 0:
            return True 
        else:
            return False


    @staticmethod
    def collect_tags():
        with open('tag_lists/tags.txt', 'r') as tags:
            return [tag.lower().strip().replace(' ', '') for tag in tags.readlines()]


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Xbox_LFG_Interaction().startup())
    loop.close()
