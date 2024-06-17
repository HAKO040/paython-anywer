# Requier Modules 
from pyrogram import Client, types, filters, enums
import asyncio 
import os
import requests
import json

# Bot Config Obj
class Config:
    SESSION : str = "<SESSSIONS_PYROGRAM>" # Pyrogram Sessions
    API_KEY : str = "<API_KEY_BOT>" # ApiKey Bot
    API_HASH: str = "95f5f60466a696e33a34f297c734d048" # APi_Hash
    API_ID  : int = 22119881 # Api id
    SUDO    : int = 5724519766 # Sudo id 
    CHANNLS : str = ['radfx2'] # CHannls List
 

# Check Bot Dirct Exists
if not os.path.exists('./.session'):
    os.mkdir('./.session')

# Check data base 
if not os.path.exists('./data.json'):
    json.dump({'users':[]} ,open('./data.json', 'w'), indent=3)

# Pyrogram Apps
app = Client(
    "./.session/rad", 
    bot_token=Config.API_KEY, 
    api_hash=Config.API_HASH, 
    api_id=Config.API_ID, 
    parse_mode=enums.ParseMode.DEFAULT
)

# get Sotrye Methods 
async def GET_STORES_DATA(chat_id: str, story_id: int):
    # Start Pyro Client
    app = Client(':memory:', api_hash=Config.API_HASH, api_id=Config.API_ID, session_string=Config.SESSION, workers=2, no_updates=True)
    try:
        await app.connect()
    except Exception as e:
        print(e)
        return (False, None)
    # Get Storys
    try:
        data = await app.download_media(await app.get_stories(chat_id=chat_id, story_ids=story_id) , in_memory=True,)
    except Exception as e:
        print(e)
        return (False, None)

    await app.disconnect()
    return (True, data)

# Check Join Medthodes
async def CHECK_JOIN_MEMBER(user_id: int, channls: list, API_KEY: str):
    """
    user_id : The member telegram id 
    channls : list channls 
    API_KEY : Bot Token
    """
    states = ['administrator','creator','member','restricted']
    # Start Loop
    for channl in channls:
        try:
            api =f"https://api.telegram.org/bot{API_KEY}/getChatMember?chat_id=@{channl}&user_id={user_id}"
            respons = requests.get(api).json()
            # Check Status 
            if respons['result']['status'] not in states:
                return (False, channl)
        except:
                return (False, channl)

    return (True, None)

# on Start Bot 
@app.on_message(filters.private & filters.regex('^/start$'))
async def ON_START_BOT(app: Client, message: types.Message):
    status, channl = await CHECK_JOIN_MEMBER(message.from_user.id, Config.CHANNLS, Config.API_KEY)
    if not status:
        await message.reply("""
                    ↫ : يرجا الاشتراك في قنات البوت لي اتتمكن من استخدامه \n\n ↫ : CH : ❲ @{} ❳\n ↫ :  قم بي ارسال ( /start ) بعد الاشتراك
        """.format(channl))
        return

    # Load data
    datas = json.load(open('./data.json'))
    if not message.from_user.id in datas['users']:
        datas['users'].append(message.from_user.id)
        json.dump(datas ,open('./data.json', 'w'), indent=3)
        await app.send_message(
            chat_id=Config.SUDO, text="""↫︙NEw User Join The Bot .\n\n  ↫ id :  ❲ {} ❳\n  ↫ username :  ❲ @{} ❳\n  ↫ firstname :  ❲ {} ❳\n\n↫︙members Count NEw : ❲ {} ❳"""
            .format(message.from_user.id, message.from_user.username, message.from_user.first_name,len(datas['users']))
        )
    await message.reply(text="↫ : اهلاً بك في بوت تحميل ستوريات تلكرام , قم بي ارسال رابط الاستوري وسيتم تحميله خلال ثواني .", reply_markup=types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton(text='❲ D E V❳', url='t.me/r_afx')]
    ]))



# On Send Story Url https://t.me/r_afx/s/5
@app.on_message(filters.private & filters.text)
async def ON_URL(app: Client, message: types.Message):
    url = message.text
    status, channl = await CHECK_JOIN_MEMBER(message.from_user.id, Config.CHANNLS, Config.API_KEY)
    if not status:
        await message.reply("""
                    ↫ : يرجا الاشتراك في قنات البوت لي اتتمكن من استخدامه \n\n ↫ : CH : ❲ @{} ❳\n ↫ :  قم بي ارسال ( /start ) بعد الاشتراك
        """.format(channl))
        return
    message_data = await message.reply(text="↫ : انتضر قليلاً جاري التحميل ")
    # Check Url 
    if not url.startswith('https://t.me/'):
        await message_data.edit(text="↫ : الرابط غير صالح قم بي ارسال رابط صالح")
        return
    # Get Stor data 
    # Split Url 
    try:
        chats_id = url.split('/')[-3]
        story_id = int(url.split('/')[-1])
    except Exception as e:
        await message_data.edit(text="↫ : الرابط غير صالح قم بي ارسال رابط صالح")
        return
        
    # Get Story And Download 
    status, story_data = await GET_STORES_DATA(chats_id, story_id)
    # Checkc data 
    if not status:
        await message_data.edit(text="↫ : عذرن حدثت مشكلا اثناء التحميل ")
        return
    await message_data.edit(text="↫ : تم التحميل بي نجاح")
    await app.send_video(
        chat_id=message.chat.id, video=story_data
    )

    

asyncio.run(app.run())