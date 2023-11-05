# VROOMbot

Tracks repairs to vehicles in a shop.

## Installation

    pip install python-telegram-bot gspread oauth2client pygsheets

Create a file named .secrets in the dir `vroombot`, with the following values:

    GOOGLE_SHEETS_API_KEY=123456789
    GOOGLE_SHEETS_SHEET_ID=123456789
    TELEGRAM_BOT_KEY=123456789

Replace each `123456789` with the actual value.

### Telegram: Create a new Bot

Talk to the `@botfather` and ask it to create a new bot for you.
It will give you an API key, which you should use for `TELEGRAM_BOT_KEY`

### Google Sheets: Create Application and Service Account

1. Go to https://console.cloud.google.com/ and create a new Project.

2. Switch to that project.

3. Go to https://console.cloud.google.com/apis/library/sheets.googleapis.com?project=vroombot
(This is actually "Google Sheets API" under "APIs & Services" dashboard)
and click on "Enable".

4. Click on "Credentials".

~~5. Click on "CREATE CREDENTIALS" and choose "API Key".~~

~~6. Click on the key, and restrict it to only use "Google Sheets API".~~

~~It will give you an API key, which you should use for `GOOGLE_SHEETS_API_KEY`.~~

5. Click on "CREATE CREDENTIALS" and choose "Service Account". You'll be asked to enter
a name and description, everything else can be skipped with "Next".

6. After the account is created, click on it, and select "KEYS" form the top.

7. Select "ADD KEY", "Create New Key", and choose "JSON". It will download a JSON file
to you computer. Rename that file to be `google-sheets-bot-auth.json`, and put it
in the same directory as `.secrets`

### Google Sheets: Create sheet

1. Go to https://docs.google.com/spreadsheets/u/0/ and create a new sheet.

2. Look at the URL, it should be of the format https://docs.google.com/spreadsheets/d/AAAAAAAAAAAAA/edit#gid=0
Take the part of the "AAAAAAAA" and use that for `GOOGLE_SHEETS_SHEET_ID`

3. Click on "Share" in the upper-left corner, and give the bot's email "Editor" access.
My bot's email is `bot-account@vroombot.iam.gserviceaccount.com`. You can check yours
by going to https://console.cloud.google.com/iam-admin/serviceaccounts?project=vroombot
and clicking on the Service Account you're using.

4. You will also have to enable "Google Drive" access for the bot. Go to
https://console.cloud.google.com/apis/api/drive.googleapis.com/metrics?project=vroombot
and click on "Enable".

## Run

TODO

## Usage

TODO