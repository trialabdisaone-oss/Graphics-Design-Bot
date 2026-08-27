# Graphics Design Telegram Bot

A professional Telegram bot for graphic designers.  
Clients can view services, prices, portfolio, and place orders directly in Telegram.  
You (the designer) receive instant notifications + files for every new order.

---

## Features

- Beautiful main menu with inline buttons
- Services & pricing (fully editable)
- Portfolio link
- Complete order flow:
  1. Select service
  2. Enter name
  3. Describe the project
  4. Upload reference images/files
  5. Confirm order
- Automatic notification to your Telegram account
- All uploaded files are forwarded to you
- Easy to customize

---

## Quick Start (5 minutes)

### 1. Create the bot on Telegram

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Choose a name (e.g. `My Design Studio`)
4. Choose a username (must end with `bot`, e.g. `MyDesignStudio_bot`)
5. Copy the **token** BotFather gives you

### 2. Get your Telegram User ID

1. Search for **@userinfobot**
2. Start it → it will reply with your **ID** (a number)
3. Copy that number

### 3. Setup the project

```bash
# Go into the folder
cd graphics_design_bot

# Create virtual environment (recommended)
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
