from dataclasses import dataclass
from datetime import datetime
import traceback
from typing import List, Optional
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import pygsheets

import config

my_config = config.load_config()

# Initialize Google Sheets
FIELDS = {
    "id": "מספר סידורי",
    "reported_at": "זמן דיווח",
    "vechicle_identifier": "צלם",
    "malfunction_type": "סוג תקלה",
    "details": "פירוט",
    "urgency": "דחיפות",
    "apc_or_tank": 'נגמ"ש/טנק',
    "reported_by": "מי דיווח",
    "status": "סטטוס",
    "closed_at": "תאריך סגירה",
}


@dataclass
class RepairLogRecord:
    id: str
    reported_at: datetime
    vechicle_identifier: str
    malfunction_type: str
    details: str
    reported_by: str
    urgency: Optional[str] = None
    apc_or_tank: Optional[str] = None
    status: Optional[str] = None
    closed_at: Optional[datetime] = None


gc: pygsheets.client.Client = pygsheets.authorize(
    service_file=my_config.google_sheets.json_file
)
# sh:pygsheets.Spreadsheet = gc.open("Vroombot")
sh: pygsheets.Spreadsheet = gc.open_by_key(my_config.google_sheets.sheet_id)
worksheet: pygsheets.Worksheet = sh.worksheet_by_title("Test")


def sheet_init():
    # Update the header row to match our expectations
    values = list(FIELDS.values())
    print(values)
    worksheet.update_row(index=1, values=values)


def add_record(record:RepairLogRecord):
    values = [""] * len(FIELDS.keys())
    for idx, key in enumerate(FIELDS.keys()):
        val = record.__dict__[key]
        if val:
            values[idx] = val
    worksheet.insert_rows(worksheet.rows, values=values, inherit=True)


# # Initialize your Telegram bot

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """The following commands are available:
        /hello - Say hello!

        You can also just send a message with the following three lines:
        
        123
        חימוש
        לא יורה

        And it will add a new record.
        """
    )

async def hello_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}  {update.message.chat_id}"
    )

async def parse_3_line_message(lines: List[str], update: Update):
    vehicle_identifier = lines[0]
    malfunction_type = lines[1]
    details = lines[2]
    reported_by = " ".join(
        [update.effective_user.first_name, update.effective_user.last_name]
    )
    add_record(
        record=RepairLogRecord(
            id=str(uuid.uuid4()),
            reported_at=str(datetime.now()),
            vechicle_identifier=vehicle_identifier,
            malfunction_type=malfunction_type,
            details=details,
            reported_by=reported_by,
        )
    )
    await update.message.reply_text(
        f"סבבה, הוספתי שורה"
    )

async def message_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    try:
        if not update.message.text:
            return
        lines = update.message.text.splitlines()
        if len(lines) == 3:
            await parse_3_line_message(update=update, lines=lines)
    except Exception as ex:
        # print exception with stack trace
        traceback.print_exc()
        return


app = ApplicationBuilder().token(my_config.telegram_bot_key).build()
app.add_handler(CommandHandler("help", help_handler))
app.add_handler(CommandHandler("hello", hello_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

# Start the bot
sheet_init()
app.run_polling()
