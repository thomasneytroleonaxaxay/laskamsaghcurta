import os
import csv
# -*- coding: utf-8 -*-
import requests
from licensing.methods import Helpers

phone_path = r"/storage/emulated/0/giv/captcha2.csv"
pc_path = r"C:\join\captcha2.csv"

captcha_api_key = None

if os.path.exists(phone_path):
    print("Telefon fayli topildi!")
    def GetMachineCode():
        machine_code = Helpers.GetMachineCode(v=2)
        return machine_code

    machine_code = GetMachineCode()
    with open(phone_path, 'r') as f:
        reader = csv.reader(f)
        captcha_api_key = next(reader)[0]
    with open(r"/storage/emulated/0/giv/proxy.csv", 'r') as f: 
        reader = csv.reader(f)
        ROTATED_PROXY = next(reader)[0]

    # Load givs from randogiv.csv
    givs = []
    bot_mapping = {}
    with open(r"/storage/emulated/0/giv/rangiv.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 1:
                givs.append(row[0].strip())
                bot_mapping[row[0].strip()] = row[1].strip()
    with open(r"/storage/emulated/0/giv/ranochiqkanal.csv", 'r') as f:
        premium_channels = [row[0] for row in csv.reader(f)]
        
    with open(r"/storage/emulated/0/giv/ranyopiqkanal.csv", 'r') as f:
        yopiq_channels = [row[0] for row in csv.reader(f)]
    with open(r"/storage/emulated/0/giv/ranlimit.csv", 'r') as f:
        reader = csv.reader(f)
        limituzz = int(next(reader)[0])
    print(f"Kutiladigan vaqt - {limituzz}")
    
elif os.path.exists(pc_path):
    print("Kompyuter fayli topildi!")
    import subprocess
    def get_hardware_id():
        hardware_id = str(subprocess.check_output('wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()
        return hardware_id

    machine_code = get_hardware_id()
    with open(pc_path, 'r') as f:
        reader = csv.reader(f)
        captcha_api_key = next(reader)[0]
    with open(r"C:\join\proxy.csv", 'r') as f:
        reader = csv.reader(f)
        ROTATED_PROXY = next(reader)[0]
    givs = []
    bot_mapping = {}
    with open(r"C:\join\randogiv.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 1:
                givs.append(row[0].strip())
                bot_mapping[row[0].strip()] = row[1].strip()

    with open(r"C:\join\randolimit.csv", 'r') as f:
        reader = csv.reader(f)
        limituzz = int(next(reader)[0])
    print(f"Kutiladigan vaqt - {limituzz}")

    with open(r"C:\join\ranochiqkanal.csv", 'r') as f: 
        premium_channels = [row[0] for row in csv.reader(f)]
    with open(r"C:\join\ranyopiqkanal.csv", 'r') as f: 
        yopiq_channels = [row[0] for row in csv.reader(f)]
else:
    print("Hech qaysi fayl topilmadi!")
    
# GitHub repository URL
url = "https://raw.githubusercontent.com/Enshteyn40/crdevice/refs/heads/main/randomizecaptcha.csv"

# URL'dan CSV faylni yuklab olish
response = requests.get(url)

# Ma'lumotlarni qatorlarga ajratish
lines = response.text.splitlines()

# Olingan qatorlarni tozalash
hash_values_list = [line.strip() for line in lines]
print(machine_code)

# Mashina kodini tekshirish
if machine_code in hash_values_list:
    import base64
    import asyncio
    from urllib.parse import unquote
    from telethon.tl.functions.messages import ImportChatInviteRequest
    import aiohttp
    import zipfile
    import shutil
    import tempfile
    import time
    import aiohttp_proxy
    import requests
    import fake_useragent
    from telethon import TelegramClient
    from telethon.tl.functions.channels import JoinChannelRequest
    from telethon.sessions import StringSession
    from telethon.tl.types import InputUser, InputBotAppShortName
    from telethon.tl.functions.messages import RequestAppWebViewRequest
    import csv
    from termcolor import colored
    from twocaptcha import TwoCaptcha

    channels = premium_channels + yopiq_channels

    async def run(phone, start_params, channels, index):
        api_id = 22962676
        api_hash = '543e9a4d695fe8c6aa4075c9525f7c57'

        tg_client = TelegramClient(f"sessions/{phone}", api_id, api_hash)
        await tg_client.connect()
        if not await tg_client.is_user_authorized():
            print('Sessiyasi yoq raqam ')
        else:
            async with tg_client:
                me = await tg_client.get_me()
                name = me.username or me.first_name + (me.last_name or '')
                for yopiq_link in yopiq_channels:
                    try:
                        await tg_client(ImportChatInviteRequest(yopiq_link)) 
                        time.sleep(limituzz)
                        print(colored(f"{name} | Kanalga a'zo bo'ldi {yopiq_link}", "green"))
                    except Exception as e:
                        print(colored(f"{name} | Kanalga qo'shilishda xatolik {yopiq_link}: {e}", "red")) 

                for ochiq_link in premium_channels:
                    try:
                        await tg_client(JoinChannelRequest(ochiq_link)) 
                        time.sleep(limituzz)
                        print(colored(f"{name} | Kanalga a'zo bo'ldi {ochiq_link}", "green"))
                    except Exception as e:
                        print(colored(f"{name} | Kanalga qo'shilishda xatolik {ochiq_link}: {e}", "red"))   

                for start_param in start_params:
                    bot_username = bot_mapping.get(start_param)
                    if not bot_username:
                        print(colored(f"Giv uchun mos bot topilmadi: {start_param}", "yellow"))
                        continue
                    print(bot_username)
                    bot_entity = await tg_client.get_entity(bot_username)
                    bot = InputUser(user_id=bot_entity.id, access_hash=bot_entity.access_hash)
                    bot_app = InputBotAppShortName(bot_id=bot, short_name="JoinLot")

                    web_view = await tg_client(
                        RequestAppWebViewRequest(
                            peer=bot,
                            app=bot_app,
                            platform="android",
                            write_allowed=True,
                            start_param=start_param
                        )
                    )

                    init_data = unquote(web_view.url.split('tgWebAppData=', 1)[1].split('&tgWebAppVersion')[0])

                    headers = {
                        'accept': '*/*',
                        'accept-language': 'ru-RU,ru;q=0.5',
                        'cache-control': 'no-cache',
                        'dnt': '1',
                        'pragma': 'no-cache',
                        'priority': 'u=1, i',
                        'referer': f'https://randomgodbot.com/api/lottery/snow/main.html?tgWebAppStartParam={start_param}',
                        'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        'sec-gpc': '1',
                        'user-agent': fake_useragent.UserAgent().random,
                        'x-requested-with': 'XMLHttpRequest',
                    }
                    proxy_conn = aiohttp_proxy.ProxyConnector().from_url(ROTATED_PROXY) if ROTATED_PROXY else None
                    async with aiohttp.ClientSession(headers=headers, connector=proxy_conn) as http_client:
                        try:
                            encoded_init_data = base64.b64encode(init_data.encode()).decode()
                            url = f"https://95.217.212.109/lot_join?userId={me.id}&startParam={start_param}&id={encoded_init_data}"
                            response = await http_client.get(url=url, ssl=False)
                            response.raise_for_status()

                            response_json = await response.json()
                            if response_json.get('ok') and response_json.get('result') == 'success':
                                print(colored(f"{name} | Giv uchun muvaffaqiyatli qo'shildi:", "green"))
                            else:
                                print(colored(f"{name} | Giv uchun qo'shilish muvaffaqiyatsiz yoki givda allaqachon qatnashib bo'lgan: {response_json}", "red"))

                        except Exception as err:
                            print(colored(f"{name} | Giv so'rov yuborishda xatolik: {err}", "yellow"))

    async def main():
        phonecsv = "phone"
        try:
            with open(f'{phonecsv}.csv', 'r') as file:
                phones = [line.strip() for line in file if line.strip()]
        except Exception as e:
            print(f"Telefon raqamlarini yuklashda xatolik: {e}")
            return

        success_count = 0

        for index, phone in enumerate(phones, start=1):
            print(colored(f"[{index}] {phone} uchun jarayon boshlanmoqda...", "blue"))
            await run(phone, givs, channels, index)
            success_count += 1
            print(colored(f"[{index}] Phone: {phone} | Jarayon yakunlandi.", "magenta"))

        print(colored(f"Umumiy muvaffaqiyatli hisoblar: {success_count}", "green"))

    if __name__ == '__main__':
        asyncio.run(main())
else:
    print("Kodni sotib olish uchun @Enshteyn40 ga murojat qiling")
