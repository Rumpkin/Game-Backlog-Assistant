# Game Backlog Assistant

This program will help you easily add to and manage your gaming backlog via helpful tools and easy UI. Using this program you can enter the name of a game and get the Amount of time to complete, genres, release date, platforms, and more of the game. Addionitally the program will add it to a notion database to help you more easily manage it with easy and clean UI.

![Alt text](/images/example1.png)

![Alt text](/images/example2.png)

## Notion Setup

1. Create a notion account at https://www.notion.so/signup

2. Create a copy of the Video Game Backlog Tracker at https://www.notion.so/templates/videogame-backlog-tracker

3. Create a new integration at https://www.notion.so/profile/integrations

4. Allow the integration to Read, Update, and Insert Content

5. Take note of the Internal Integration Secret Key for later

6. Go back to your copy of the Video Game Backlog Tracker and Add a new Connection to your previously created integration

![Alt text](/images/Connection.png)

## IGDB Setup

1. Go to https://api-docs.igdb.com/#getting-started and follow the sets to create an account

2. Go to https://dev.twitch.tv/console/apps and create a new application

![Alt text](/images/IGDB.png)

3. Manage that application and take note of the Client ID and Client Secret for later use

## Installation
1. Clone this repository:

```
git clone https://github.com/Rumpkin/Game-Backlog-Assistant.git
cd Game-Backlog-Assistant
```

2. Set up your environment variables:

- Open the secrets.json file in the project root directory
- Add the following environment variables as requested
- Example:
```
{
    "notion_token" : "YourNotionToken",    
    "notion_database_id" : "Notion_Database_ID",
    "IGDB_clientID" : "IGDB_ClientID",
    "IGDB_secret" : "IGDB_Secret"
}
```

### Not sure how to find an environment variable look below 

<details>
<summary>Finding Your Notion Client ID</summary>

You can find your Client ID under the settings for the integretion you created while setting up notion

> Integrations link: https://www.notion.so/profile/integrations

![Alt text](/images/Integration_Secret_Key_Referenece1.png)

</details>

<details>
<summary>Finding Your Notion Database ID</summary>

You can find you notion database id by first getting the database link. You can copy the database link by clicking on the ... and then "Copy link to Table"

![Alt text](/images/Notion_Link.png)

After getting the link copy the numbers and letters after www.notion.so/ and before ?v=

Example: www.notion.so/ <u>**453a0a7fd9e347b6b1ebe69f9332f7e7**<u> ?v=67d6d5201d3541b98b87226188300fef&pvs=4

</details>

<details>
<summary>Finding Your IGDB Client ID and Secret Token</summary>

You can find you IGDB Client ID and Secret if you manage your Twitch Application you created when setting up IGDB

> Twitch Applications Link: https://dev.twitch.tv/console/apps 

![Alt text](/images/IGDB_Manage.png)

</details>

## Usage

Run the "Start Windows.bat" or "Start Linux.sh" script to start the program:

Once started, the program will prompt you with whether you want to add a single game or a list of games:

```
Single Game? y/n 
```

If you type yes it will prompt you for the game's title 

```
Single Game? y/n y
Game title: 
```

And then add it to the notion database

```
Single Game? y/n y
Game title: Spiritfarer
--- Adding Spiritfarer ---
Game Platforms: PC (Microsoft Windows), Google Stadia, PlayStation 4, Xbox One, Linux, Mac, Nintendo Switch
Game Release Date: 2020-08-17
Game Genres: Platform, Action, Fantasy
Game Added to Database
```

If you type no it will try to locate a file name "games.txt" and will add all the games located in the file

```
Single Game? y/n n
--- Adding Tunic ---
Game Added to Database
--- Adding Celeste ---
Game Added to Database
--- Adding Katana Zero ---
Game Added to Database
--- Adding Ghost of Tsushima ---
Game Added to Database
```

After adding a game to the database the program will delete the title from the games.txt file

**Note: Spelling and Capitalization Matters**

The program will not be able to find games that are misspelled or misscapitalized

:x: Ghost of Sushima

:x: Ghost **O**f Tsushima

:white_check_mark: Ghost of Tsushima

## Thank you And Enjoy
If you have any questions or issues feel free to ask for help