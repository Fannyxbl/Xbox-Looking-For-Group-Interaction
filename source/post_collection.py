import aiohttp
import random
import json

class LFG_Post_Collector:
    def __init__(self):
        self.club_ids = [
            '267695549', # Fortnite
            '1791712750', # Minecraft
            '1628516715', # Apex Legends
            '787008472', # Call of Duty: Modern Warfare
            '2030093255', # Forza Horizon 5
            '1717113201' # Sea of Thieves
        ]

    async def retrieve_posts(self, session: aiohttp.ClientSession, token):
        try:
            id = random.choice(self.club_ids)
            headers = {
                'x-xbl-contract-version': '107',
                'Accept': 'application/json',
                'Accept-Language': 'en-US',
                'Authorization': token
            }
            payload = {
                'type': 'search',
                'templateName':'global(lfg)',
                'orderBy':'suggestedLfg desc',
                'communicatePermissionRequired':True,
                'includeScheduled': True,
                'filter':f'session/titleId eq {id} and session/roles/lfg/confirmed/needs ge 1'
            }
            async with session.post(f'https://sessiondirectory.xboxlive.com/handles/query?include=relatedInfo,roleInfo,activityInfo', headers=headers, json=payload) as recent_posts:
                return recent_posts.status, json.loads(await recent_posts.read())
        except Exception as e:
            print(f' \x1b[1;39m[\x1b[1;31m!\x1b[1;39m] Failed to retrieve recent posts')
            return None, None
