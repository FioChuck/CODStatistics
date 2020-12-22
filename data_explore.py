#update 3
import asyncio
import callofduty
from callofduty import Mode, Platform, Title
import numpy as np
import warnings
import pickle
import pandas as pd
import tabulate as t
import numpy as np

##### Passwords #####
try:
   from local_settings import *
except ImportError:
   pass

##### Definitions #####
async def login():
    client = await callofduty.Login("chasfiorenza@gmail.com", ACCOUNT_PASSWORD)
    return client

async def get_stats(person,client,mode):
    await asyncio.sleep(1)
    player = await client.GetPlayer(mode, person)
    await asyncio.sleep(1)
    profile = await player.profile(Title.ModernWarfare, Mode.Warzone)
    await asyncio.sleep(1)
    return profile

#### Main ####
playerList = {
"VOGN3RPO5EIDON#7978865": Platform.Activision,\
"ZAC210": Platform.Activision,\
"The_IronLotus23#8048742": Platform.Activision,\
"FioChuck#1806888": Platform.Activision,\
"Magz0213#1655927": Platform.Activision,\
"delta-sniper025#2663829": Platform.Activision,\
"Amancalledmann#7804230": Platform.Activision,\
"brew_of_crew#7807519": Platform.Activision,\
"Carruthless011#8767310": Platform.Activision,\
"Keeeef25#3095949": Platform.Activision,\
# "BopperMagoo#7723579":Platform.Activision,\
"JakeDantana#9120888":Platform.Activision\
# "StoneMountain64": Platform.Activision,\
# "CouRageJD#6520410": Platform.Activision,\
# "symfuhny#9112896": Platform.Activision,\
# "SmittyBarstool": Platform.PlayStation,\
# "Nickmercs#11526":Platform.BattleNet\
}

#
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', 7)

##### Load Pickle File #####
pkl_file = open('/Users/charlesfiorenza/Projects/temp/cod.pkl','rb')
rootDict = pickle.load(pkl_file)
pkl_file.close()

#### Main ####

## BR Lifetime Stats DF Definition ##
lifetime_df = pd.DataFrame()
for player in playerList:
    playerDict = rootDict[player]['lifetime']['mode']
    playerDict['comrade'] = player
    df = pd.DataFrame([playerDict])
    lifetime_df = lifetime_df.append(df, ignore_index=True)

print(rootDict['FioChuck#1806888'])
