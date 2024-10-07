import requests, datetime, json
from enum import Enum


class Platform(Enum):
    OFFICIAL = 1
    WIKIA = 2
    WIKIPEDIA = 3
    FACEBOOK = 4
    TWITTER = 5
    TWITCH = 6
    INSTAGRAM = 8
    YOUTUBE = 9
    IPHONE = 10
    IPAD = 11
    ANDROID = 12
    STEAM = 13
    REDDIT = 14
    ITCH = 15
    EPICGAMES = 16
    GOG = 17
    DISCORD = 18
    PS4 = 48
    NintendoSwitch = 130


with open('./secrets.json', 'r') as fd:
    secrets = json.load(fd)

clientID = secrets.get("IGDB_clientID")
secret = secrets.get("IGDB_secret")

auth = requests.post(f'https://id.twitch.tv/oauth2/token?client_id={clientID}&client_secret={secret}&grant_type=client_credentials')

if auth.status_code == 200:
    access_token = auth.json()['access_token']    
else:
    print("Failed to fetch Authorization Token")

headers = {
    "Client-ID": clientID,
    "Authorization": f"Bearer {access_token}"
}

def getGameID(name):
    response = requests.post('https://api.igdb.com/v4/games/', headers=headers, data=f'fields id; sort rating desc;where name = "{name}"; limit 1;')
    if response.status_code == 200:
        try:
            data = response.json()[0]        
            return data['id']
        except Exception:
            print('Failed to get Game ID')
    else:
        print('Failed to get Game ID')

def getGameRelease(name, debug = False):
    response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=f'fields first_release_date; sort rating desc;where name = "{name}"; limit 1;')
    if response.status_code == 200:
        try:
            data = response.json()[0]        
            release = datetime.datetime.fromtimestamp(data['first_release_date']).strftime("%Y-%m-%d")
            if (debug):
                print('Game Release Date: ' + str(release))
            return release
        except Exception:
            print('Failed to get Release Date')
    else:
        print('Failed to get Release Date')

def getGameGenres(name, debug = False):
    
    response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=f'fields genres; sort rating desc;where name = "{name}"; limit 1;')
    
    if response.status_code == 200:              
        try:  
            data = response.json()[0]                
        except Exception:
            print('Failed to get Genres')
            return 
    else:
        print('Failed to get Genres')
        return 
    
    response = requests.post('https://api.igdb.com/v4/genres', headers=headers, data=f'fields name;')

    if response.status_code == 200:
        genres = list()
        debugString = "Game Genres:"
        data2 = response.json()            
        for genre in data2:                     
            if (genre['id'] in data['genres']):
                genres.append(genre['name'])
                debugString += " " + genre['name']
        if (debug):
            print(debugString)        
        return genres
    else:
        print('Failed to get Genres')      

def getGameThemes(name):
    response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=f'fields themes; sort rating desc;where name = "{name}"; limit 1;')
    if response.status_code == 200:
        try:        
            data = response.json()[0] 
        except Exception:
            print('Failed to get Themes')
            return  
    else:
        print('Failed to get Themes')
        return 
    
    response = requests.post('https://api.igdb.com/v4/themes', headers=headers, data=f'fields name;')
    
    if response.status_code == 200:
        genres = list()
        data2 = response.json()
        
        try:
            for genre in data2:                        
                if (genre['id'] in data['themes']):
                    genres.append(genre['name'])
            return genres
        except Exception:
            print('Failed to get Themes')        
            return
    else:
        print('Failed to get Themes')        

def getGamePlatforms(name, debug = False): 
    response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=f'fields platforms; sort rating desc;where name = "{name}"; limit 1;')
    if response.status_code == 200:
        try:
            data = response.json()[0]                                     
        except Exception:
            print('Failed to get Platforms')        
            return 
    else:
        print('Failed to get Platforms')        
        return 
    
    response = requests.post('https://api.igdb.com/v4/platforms', headers=headers, data=f'fields name; limit 500;')
    
    if response.status_code == 200:
        platforms = list()
        debugPlatforms = "Game Platforms:"
        data2 = response.json()        
        for platform in data2:                                   
            if (platform['id'] in data['platforms']):
                platforms.append(platform['name'])
                debugPlatforms += " " + platform['name'] + ","
        
        if(debug):
            debugPlatforms = debugPlatforms[:-1]
            print(debugPlatforms)

        return platforms
    else:
        print('Failed to get Platforms')    

def getGameModes(name):
    response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=f'fields game_modes; sort rating desc;where name = "{name}"; limit 1;')
    if response.status_code == 200:
        try:
            data = response.json()[0]             
        except Exception:
            print('Failed to get Game Modes')        
            return 
    else:
        print('Failed to get Game Modes')        
        return 
    
    response = requests.post('https://api.igdb.com/v4/game_modes', headers=headers, data=f'fields name;')
    
    if response.status_code == 200:
        gameModes = list()
        data2 = response.json()        
        for gameMode in data2:                        
            if (gameMode['id'] in data['game_modes']):
                gameModes.append(gameMode['name'])
        return gameModes
    else:
        print('Failed to get Themes')  

def getGameWebsites(id):
    response = requests.post('https://api.igdb.com/v4/websites', headers=headers, data=f'fields category,trusted,url; sort rating desc;where name = {id};')

    if (response.status_code == 200):
        data = response.json()
    else:
        print('Failed to get Websites')
    
    websites = list()

    for website in data:
        if (website['trusted']):
            websites.append({'category' : Platform(website['category']), 'url' : website['url']})

    return websites

def getCoverLink(id):
    response = requests.post('https://api.igdb.com/v4/covers', headers=headers, data=f'fields url; where game = {id};')            

    if response.status_code == 200:
        try:
            key = response.json()[0]['url'].split('t_thumb/')[1]
            #return f"https://images.igdb.com/igdb/image/upload/t_cover_big/{key}";   
            return f"https://images.igdb.com/igdb/image/upload/t_1080p_2x/{key}";   
        except Exception:
            print("Failed to find Cover Link")
    else:
        print("Failed to find Cover Link")        

def saveCover(id, fileName):
    response = requests.post('https://api.igdb.com/v4/covers', headers=headers, data=f'fields url; sort rating desc;where name = {id};')        
    if response.status_code == 200:
        try:
            key = response.json()[0]['url'].split('t_thumb/')[1]    
            response = requests.get(f"https://images.igdb.com/igdb/image/upload/t_cover_big/{key}")
        except Exception:
            print("Failed to download image")
            return
    else:
        print("Failed to download image")
        return

    if response.status_code == 200:
        with open(f"{fileName}.jpg", "wb") as file:
            file.write(response.content)
        print("Image downloaded successfully")
    else:
        print("Failed to download image")
