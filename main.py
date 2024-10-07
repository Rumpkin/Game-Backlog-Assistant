from notion_client import Client
from IGDB import *
from getCompeletionTime import getTimeToCompelete
import json
import os

with open('./secrets.json', 'r') as fd:
    secrets = json.load(fd)

notion_token = secrets.get("notion_token")
notion_page_id = secrets.get("notion_page_id")
notion_database_id = secrets.get("notion_database_id")

def write_text(client, page_id, text, type='paragraph'):
    client.blocks.children.append(
      block_id=page_id,
      children=[{
        "object": "block",
        "type": type,
        type: {
          "rich_text": [{ "type": "text", "text": { "content": text } }]
        }
      }]
    )

def write_dict_to_file_as_json(content, file_name):
    content_as_json_str = json.dumps(content)

    with open(file_name, 'w') as f:
        f.write(content_as_json_str)

def read_text(client, page_id):
    response = client.blocks.children.list(block_id=page_id)
    return response['results']

def safe_get(data, dot_chained_keys):
    keys = dot_chained_keys.split('.')
    for key in keys:
        try:
            if isinstance(data, list):
                data = data[int(key)]
            else:
                data = data[key]
        except (KeyError, TypeError, IndexError):
            return None
    return data

def create_simple_blocks_from_content(client, content):
    page_simple_blocks = []
    for block in content:
        block_id = block['id']
        block_type = block['type']
        has_children = block['has_children']
        rich_text = block[block_type].get('rich_text')

        if not rich_text:
            return

        simple_block = {
            'id': block_id,
            'type': block_type,
            'text': rich_text[0]['plain_text']
        }

        if has_children:
            nested_children = read_text(client, block_id)
            simple_block['children'] = create_simple_blocks_from_content(client, nested_children)

        page_simple_blocks.append(simple_block)


    return page_simple_blocks
    
def write_row(client, database_id, coverLink, title, consoles, releaseDate, online, genres, length):
    client.pages.create(
        **{
            "parent": {
                "database_id": database_id
            },
            "cover": {
                "type": "external",
                "external": {
                    "url": coverLink
                }
            },
            'properties': {                
                'title': {'title': [{'text': {'content': title}}]},
                'Status': {'select': {'name': "Backlog"}},
                'Release Date': {'date': {'start': releaseDate}},
                'genre': {'multi_select': genres},
                'Console': {'multi_select': consoles},
                'Online': {'multi_select': online},        
                'Length': {'number':length}        
            }
        }
    )

# Adicionado ao código original
def check_game(client, database_id, title):
    response = client.databases.query(database_id, 
        **{
            "filter": {
                "property": "title",
                "title": {
                    "equals": title
                }
            }
        }
    )

    if len(response['results']) != 0:
        return True
    else:  
        return False

def write_game(client, title, debug = False):
    print('--- Adding ' + title + ' ---')
    failed = False
    consoles = list()

    # Adicionado ao código original
    gameExists = check_game(client, notion_database_id, title)
    if gameExists:
        print(f"{title} already exists in database!")
        failed = True
        return failed


    consolesData = getGamePlatforms(title, debug)
    if (consolesData != None):
        for console in consolesData:
            consoles.append({'name':console})


    releaseDate = getGameRelease(title, debug)
    if (releaseDate == None):
        releaseDate = datetime.datetime.now().strftime("%Y-%m-%d")
        failed = True


    genres = list()
    genresData = getGameGenres(title)    
    if (genresData != None):
        for genre in genresData:
            genres.append({'name':genre})


    themes = getGameThemes(title)
    if (themes != None):
        for theme in themes:
            genres.append({'name':theme})

    if (debug):
        debugGenres = "Game Genres:"
        for genre in genres:
            debugGenres += " " + genre["name"] + ","
        debugGenres = debugGenres[:-1]
        print(debugGenres)

    online = list()
    gameModeData = getGameModes(title)
    if (gameModeData != None):
        for gameMode in gameModeData:
            online.append({'name':gameMode})    
        

    cover = getCoverLink(getGameID(title))
    if (cover == None):
        cover = 'https://www.nctm.org/uploadedImages/Publications/TCM_Blog/checkerboard.png'

    length = getTimeToCompelete(title)

    if not failed:
        write_row(client, notion_database_id, cover, title, consoles, releaseDate, online, genres, length)
        print('Game Added to Database')
    else:
        print('Game Not Added to Database')
    return failed

def main():
    client = Client(auth=notion_token)

    q = input('Single Game? y/n ')
    if (q.lower() == 'y'):
        title = input('Game title: ')
        write_game(client, title, True)        
    else:
        if (not os.path.exists('./games.txt')):
            with open('./games.txt', 'w') as fd:
                fd.close()
            
            print("Please add at least 1 game to the 'games.txt' file")
            return

        with open ('./games.txt', 'r') as fd:
            if (fd.readlines() == []):
                print("Please add at least 1 game to the 'games.txt' file")
                return



        lines = list()
        with open('./games.txt', 'r') as fd:
            games = fd.read().format().split('\n')               
            fd.close()

        with open('./games.txt', 'r') as fd:
            lines = fd.readlines()         
            fd.close()
            
        count = 0
        for game in games:
            fail = write_game(client, game)   
            
            if (fail):
                count += 1
            else:            
                lines.pop(count)            

            with open('./games.txt', 'w') as fd:
                fd.writelines(lines)

if __name__ == '__main__':
    main()

