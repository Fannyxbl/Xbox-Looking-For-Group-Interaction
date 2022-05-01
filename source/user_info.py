import aiohttp
import os

class User_Info:
    def __init__(self):
        pass

    async def retrieve_user_info(self, session: aiohttp.ClientSession, token):
        try:
            headers={
                'Authorization': token,
                'x-xbl-contract-version': '2'
            }

            async with session.get('https://profile.xboxlive.com/users/me/profile/settings', headers=headers) as user_info_request:
                if user_info_request.status == 200:
                    response_data = await user_info_request.json()
                    xuid = response_data['profileUsers'][0]['id']
                    print(f'\n \x1b[1;39m[\x1b[1;36m*\x1b[1;39m] Retrieved Profile Information! \n [\x1b[1;36m*\x1b[39m] My XUID: \x1b[1;36m{xuid}\n')
                    return xuid
                else:
                    print(' \x1b[1;39m[\x1b[1;31m!\x1b[1;39m] Failed to retrieve user info!')
                    os._exit(0)
        except:
            print(' \x1b[1;39m[\x1b[1;31m!\x1b[1;39m] Failed to retrieve user info!')
            os._exit(0)