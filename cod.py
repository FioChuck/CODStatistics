#update 2
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
   from settings import *
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

####################### LOCAL #######################
client = asyncio.run(login()) #authenticate with COD API

masterDict = {}
print('Downloading Player Stats:')
print('')

for player in playerList:
    print(player)
    print(playerList[player])

    masterDict[player] = asyncio.run(get_stats(player,client,playerList[player]))
print('')
print('Download Complete')
print('')

output = open('/Users/charlesfiorenza/Projects/temp/cod.pkl', 'wb+')
pickle.dump(masterDict, output)
output.close()

####################### LOCAL #######################
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
    playerDict = rootDict[player]['lifetime']['mode']['br_all']['properties']
    playerDict['comrade'] = player
    df = pd.DataFrame([playerDict])
    lifetime_df = lifetime_df.append(df, ignore_index=True)

## BR Weekly Stats DF Definition ##
# animals list
slapdick = []

weekly_df = pd.DataFrame()
for player in playerList:
    try:
        playerDict = rootDict[player]['weekly']['mode']['br_all']['properties']
        playerDict['comrade'] = player
        df = pd.DataFrame([playerDict])
        weekly_df = weekly_df.append(df, ignore_index=True)
    except:
        slapdick.append(player)

##### Lifetime Stats #####
print('')
print('---------- HHB STATS ---------')
# print(list(lifetime_df.columns.values))

winMult = 1.5
topFiveMult = 1
killsMult = 1
downsMult = 1
revivesMult = 1
deathsMult = -1

HhbGamesPlayed = lifetime_df['gamesPlayed'].sum(axis = 0, skipna = True)
HhbTopFive = lifetime_df['topFive'].sum(axis = 0, skipna = True)
HhbKills = lifetime_df['kills'].sum(axis = 0, skipna = True)
HhbRevives = lifetime_df['revives'].sum(axis = 0, skipna = True)
HhbDeaths = lifetime_df['deaths'].sum(axis = 0, skipna = True)
HhbWins = lifetime_df['wins'].sum(axis = 0, skipna = True)
HhbDowns = lifetime_df['downs'].sum(axis = 0, skipna = True)

print('HHB ALL TIME WIN PERCENTAGE: ' + str(100*HhbWins/HhbGamesPlayed))
print('HHB ALL TIME KILLS PER GAME: ' + str(HhbKills/HhbGamesPlayed))
print('------- LIFETIME STATS -------')
## MVP ##
mvp = lifetime_df[['comrade']]
mvp['playerEffeciency*'] = \
    100*(((winMult*lifetime_df['wins']/lifetime_df['gamesPlayed'])/ (HhbWins/HhbGamesPlayed)\
    +(topFiveMult*lifetime_df['topFive']/lifetime_df['gamesPlayed'])/ (HhbTopFive/HhbGamesPlayed)\
    +(killsMult*lifetime_df['kills']/lifetime_df['gamesPlayed'])/ (HhbKills/HhbGamesPlayed)\
    +(downsMult*lifetime_df['downs']/lifetime_df['gamesPlayed'])/ (HhbDowns/HhbGamesPlayed)\
    +(revivesMult*lifetime_df['revives']/lifetime_df['gamesPlayed'])/ (HhbRevives/HhbGamesPlayed)\
    +(deathsMult*lifetime_df['deaths']/lifetime_df['gamesPlayed'])/ (HhbDeaths/HhbGamesPlayed)))/\
    +(winMult\
    +topFiveMult\
    +killsMult\
    +downsMult\
    +revivesMult\
    +deathsMult)


mvp = mvp.sort_values('playerEffeciency*',ascending=False)
mvp = mvp.reset_index(drop=True)
mvp.loc['mean'] = mvp.mean()
print('MVP: ' + mvp.iloc[0,0])
print(t.tabulate(mvp, headers='keys', tablefmt='psql'))

## Barry Bonds ##
barryBonds = lifetime_df[['comrade','scorePerMinute']]
barryBonds['killsPerGame*'] = lifetime_df['kills']/lifetime_df['gamesPlayed']
barryBonds['downsPerGame'] = lifetime_df['downs']/lifetime_df['gamesPlayed']
barryBonds['kD'] = lifetime_df['kills']/lifetime_df['deaths']
barryBonds = barryBonds.sort_values('killsPerGame*',ascending=False)
barryBonds = barryBonds.reset_index(drop=True)
barryBonds.loc['mean'] = barryBonds.mean()
print('BARRY BONDS: ' + barryBonds.iloc[0,0])
print(t.tabulate(barryBonds, headers='keys', tablefmt='psql'))

## WAR ##
war = lifetime_df[['comrade','wins','gamesPlayed']]
war['winPercentage*'] = 100 * lifetime_df['wins']/lifetime_df['gamesPlayed']
war = war.sort_values('winPercentage*',ascending=False)
war = war.reset_index(drop=True)
war.loc['mean'] = war.mean()
print('WAR: ' + war.iloc[0,0])
print(t.tabulate(war, headers='keys', tablefmt='psql'))

## MEDIC ##
medic = lifetime_df[['comrade','revives','gamesPlayed']]
medic['revivesPerGame*'] = lifetime_df['revives']/lifetime_df['gamesPlayed']
medic = medic.sort_values('revivesPerGame*',ascending=False)
medic = medic.reset_index(drop=True)
medic.loc['mean'] = medic.mean()
print('MEDIC: ' + medic.iloc[0,0])
print(t.tabulate(medic, headers='keys', tablefmt='psql'))

## ASSCLOWN ##
assclown = lifetime_df[['comrade','deaths','gamesPlayed']]
assclown['deathsPerGame*'] = lifetime_df['deaths']/lifetime_df['gamesPlayed']
assclown = assclown.sort_values('deathsPerGame*',ascending=False)
assclown = assclown.reset_index(drop=True)
assclown.loc['mean'] = assclown.mean()
print('ASSCLOWN: ' + assclown.iloc[0,0])
print(t.tabulate(assclown, headers='keys', tablefmt='psql'))

## FINISHER ##
finisher = lifetime_df[['comrade','kills','downs']]
finisher['killsPerDown*'] = lifetime_df['kills']/lifetime_df['downs']
finisher = finisher.sort_values('killsPerDown*',ascending=False)
finisher = finisher.reset_index(drop=True)
finisher.loc['mean'] = finisher.mean()
print('FINISHER: ' + finisher.iloc[0,0])
print(t.tabulate(finisher, headers='keys', tablefmt='psql'))

## NINTH INNING ##
finisher = lifetime_df[['comrade','topFive']]
finisher['topFivePercentage*'] = 100*lifetime_df['topFive']/lifetime_df['gamesPlayed']
finisher = finisher.sort_values('topFivePercentage*',ascending=False)
finisher = finisher.reset_index(drop=True)
finisher.loc['mean'] = finisher.mean()
print('NINTH INNING: ' + finisher.iloc[0,0])
print(t.tabulate(finisher, headers='keys', tablefmt='psql'))

## CLUTCH GENE ##
clutch = lifetime_df[['comrade','wins','topFive']]
clutch['topFiveWinPercentage*'] = 100*lifetime_df['wins']/lifetime_df['topFive']
clutch = clutch.sort_values('topFiveWinPercentage*',ascending=False)
clutch = clutch.reset_index(drop=True)
clutch.loc['mean'] = clutch.mean()
print('CLUTCH GENE: ' + clutch.iloc[0,0])
print(t.tabulate(clutch, headers='keys', tablefmt='psql'))

## RED ZONE ##
finisher = lifetime_df[['comrade','topTen']]
finisher['topTenPercentage*'] = 100*lifetime_df['topTen']/lifetime_df['gamesPlayed']
finisher = finisher.sort_values('topTenPercentage*',ascending=False)
finisher = finisher.reset_index(drop=True)
finisher.loc['mean'] = finisher.mean()
print('RED ZONE: ' + finisher.iloc[0,0])
print(t.tabulate(finisher, headers='keys', tablefmt='psql'))

##### Weekly Stats #####
print('------- WEEKLY STATS -------')
# print(list(weekly_df.columns.values)) # diplays all possible metrics
# print('Weekly Slapdicks:')
# for folks in slapdick:
#     print(folks)

# print(list(weekly_df.columns.values))

## SIMP ##
simp = weekly_df[['comrade']]
simp['matchesPlayed*'] = weekly_df['matchesPlayed']
simp = simp.sort_values('matchesPlayed*',ascending=True)
simp = simp.reset_index(drop=True)
simp.loc['mean'] = simp.mean()
print('SIMP: ' + simp.iloc[0,0])
print(t.tabulate(simp, headers='keys', tablefmt='psql'))

## GULAG CHAMP ##
gulag = weekly_df[['comrade','gulagKills','gulagDeaths']]
gulag['gulagWinPercentage*'] = (100 * weekly_df['gulagKills'])/ (weekly_df['gulagDeaths'] + weekly_df['gulagKills'])
gulag = gulag.sort_values('gulagWinPercentage*',ascending=False)
gulag = gulag.reset_index(drop=True)
gulag.loc['mean'] = gulag.mean()
print('GULAG CHAMP: ' + gulag.iloc[0,0])
print(t.tabulate(gulag, headers='keys', tablefmt='psql'))

## PUNISHER ##
punisher = weekly_df[['comrade','damageDone','matchesPlayed']]
punisher['damagePerGame*'] = weekly_df['damageDone']/weekly_df['matchesPlayed']
punisher = punisher.sort_values('damagePerGame*',ascending=False)
punisher = punisher.reset_index(drop=True)
punisher.loc['mean'] = punisher.mean()
print('PUNISHER: ' + punisher.iloc[0,0])
print(t.tabulate(punisher, headers='keys', tablefmt='psql'))

# WANDERER ##
wanderer = weekly_df[['comrade','distanceTraveled','matchesPlayed']]
wanderer['distancePerGame*'] = weekly_df['distanceTraveled']/weekly_df['matchesPlayed']
wanderer = wanderer.sort_values('distancePerGame*',ascending=False)
wanderer = wanderer.reset_index(drop=True)
wanderer.loc['mean'] = wanderer.mean()
print('WANDERER: ' + wanderer.iloc[0,0])
print(t.tabulate(wanderer, headers='keys', tablefmt='psql'))

## SHARPSHOOTER ##
sniper = weekly_df[['comrade','headshots','headshotPercentage']]
sniper['headshotPercentage*'] = weekly_df['headshotPercentage']
sniper = sniper.sort_values('headshotPercentage*',ascending=False)
sniper = sniper.reset_index(drop=True)
sniper.loc['mean'] = sniper.mean()
print('SHARPSHOOTER: ' + sniper.iloc[0,0])
print(t.tabulate(sniper, headers='keys', tablefmt='psql'))

## Barry Bonds ##
barryBonds = weekly_df[['comrade','scorePerMinute']]
barryBonds['killsPerGame*'] = weekly_df['kills']/weekly_df['matchesPlayed']
barryBonds['kD'] = weekly_df['kills']/weekly_df['deaths']
barryBonds = barryBonds.sort_values('killsPerGame*',ascending=False)
barryBonds = barryBonds.reset_index(drop=True)
barryBonds.loc['mean'] = barryBonds.mean()
print('BARRY BONDS: ' + barryBonds.iloc[0,0])
print(t.tabulate(barryBonds, headers='keys', tablefmt='psql'))

## ASSCLOWN ##
assclown = weekly_df[['comrade','deaths','matchesPlayed']]
assclown['deathsPerGame*'] = weekly_df['deaths']/weekly_df['matchesPlayed']
assclown = assclown.sort_values('deathsPerGame*',ascending=False)
assclown = assclown.reset_index(drop=True)
assclown.loc['mean'] = assclown.mean()
print('ASSCLOWN: ' + assclown.iloc[0,0])
print(t.tabulate(assclown, headers='keys', tablefmt='psql'))

# print('')
# print(list(weekly_df.columns.values))
