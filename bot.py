"""
Graphics Design Telegram Bot
============================
A ready-to-use bot for graphic designers.
Easily customize services, prices, portfolio, and contact info.

Author: Created for your graphics design business
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any

from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InputMediaPhoto,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# Load environment variables
load_dotenv()

# ====================== CONFIGURATION ======================
# Edit these values to match your business

BOT_TOKEN = os.getenv("BOT_TOKEN")  # From @BotFather
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # Your Telegram user ID (get it from @userinfobot)

# Your business info
BUSINESS_NAME = "Your Design Studio"
DESIGNER_NAME = "Your Name"
CONTACT_TELEGRAM = "@yourusername"
CONTACT_EMAIL = "hello@yourdesign.com"
CONTACT_WHATSAPP = "+1234567890"  # Optional
PORTFOLIO_LINK = "https://behance.net/yourname"  # or Dribbble / personal site
INSTAGRAM = "@yourdesign"

# Services & Prices (edit freely)
SERVICES = {
    "logo": {
        "name": "Logo Design",
        "price": "From $80",
        "description": "Professional logo + brand guidelines + source files",
        "delivery": "3-5 days",
    },
    "branding": {
        "name": "Full Branding Package",
        "price": "From $250",
        "description": "Logo + color palette + typography + social media kit + business cards",
        "delivery": "7-10 days",
    },
    "social": {
        "name": "Social Media Graphics",
        "price": "From $40 / post",
        "description": "Instagram posts, stories, carousels, highlights",
        "delivery": "1-3 days",
    },
    "poster": {
        "name": "Poster / Flyer Design",
        "price": "From $60",
        "description": "Print-ready posters, flyers, event graphics",
        "delivery": "2-4 days",
    },
    "banner": {
        "name": "YouTube / Web Banners",
        "price": "From $50",
        "description": "YouTube thumbnails, channel art, website banners",
        "delivery": "1-3 days",
    },
    "package": {
        "name": "Product Packaging",
        "price": "From $120",
        "description": "Product labels, box design, mockups",
        "delivery": "5-7 days",
    },
    "other": {
        "name": "Custom / Other",
        "price": "Custom quote",
        "description": "Tell me what you need and I'll give you a quote",
        "delivery": "Depends on project",
    },
}

# Conversation states
(
    SELECT_SERVICE,
    CLIENT_NAME,
    PROJECT_DESCRIPTION,
    REFERENCE_FILES,
    CONFIRM_ORDER,
) = range(5)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ====================== KEYBOARDS ======================

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎨 Services & Prices", callback_data="services")],
        [InlineKeyboardButton("🖼 Portfolio", callback_data="portfolio")],
        [InlineKeyboardButton("📝 Place an Order", callback_data="order")],
        [InlineKeyboardButton("📞 Contact Me", callback_data="contact")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
    ]
    return InlineKeyboardMarkup(keyboard)


def services_keyboard():
    keyboard = []
    for key, service in SERVICES.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{service['name']} — {service['price']}",
                callback_data=f"service_{key}"
            )
        ])
    keyboard.append([InlineKeyboardButton("« Back to Menu", callback_data="back_main")])
    return InlineKeyboardMarkup(keyboard)


def order_services_keyboard():
    keyboard = []
    for key, service in SERVICES.items():
        keyboard.append([
            InlineKeyboardButton(service["name"], callback_data=f"order_{key}")
        ])
    keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="cancel")])
    return InlineKeyboardMarkup(keyboard)


def confirm_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("✅ Confirm Order", callback_data="confirm_yes"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def skip_keyboard():
    keyboard = [[InlineKeyboardButton("⏭ Skip / No files", callback_data="skip_files")]]
    return InlineKeyboardMarkup(keyboard)


# ====================== HANDLERS ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message"""
    user = update.effective_user
    welcome_text = (
        f"👋 Hello {user.first_name}!\n\n"
        f"Welcome to *{BUSINESS_NAME}*\n"
        f"I'm {DESIGNER_NAME}, professional graphic designer.\n\n"
        "I create logos, branding, social media graphics, posters, packaging and more.\n\n"
        "What would you like to do?"
    )
    await update.message.reply_text(
        welcome_text,
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown",
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all inline button presses"""
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_main":
        await query.edit_message_text(
            "🏠 Main Menu\n\nWhat would you like to do?",
            reply_markup=main_menu_keyboard(),
        )

    elif data == "services":
        text = "🎨 *Our Services & Prices*\n\nSelect a service to see details:"
        await query.edit_message_text(
            text,
            reply_markup=services_keyboard(),
            parse_mode="Markdown",
        )

    elif data.startswith("service_"):
        service_key = data.replace("service_", "")
        service = SERVICES.get(service_key)
        if service:
            text = (
                f"✨ *{service['name']}*\n\n"
                f"💰 Price: *{service['price']}*\n"
                f"⏱ Delivery: {service['delivery']}\n\n"
                f"{service['description']}\n\n"
                "Ready to order? Click the button below."
            )
            keyboard = [
                [InlineKeyboardButton("📝 Order This Service", callback_data=f"order_{service_key}")],
                [InlineKeyboardButton("« Back to Services", callback_data="services")],
            ]
            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown",
            )

    elif data == "portfolio":
        text = (
            f"🖼 *Portfolio*\n\n"
            f"You can view my latest work here:\n"
            f"👉 {PORTFOLIO_LINK}\n\n"
            f"Instagram: {INSTAGRAM}\n\n"
            "I can also send you specific examples based on the style you like. "
            "Just tell me what you're looking for!"
        )
        keyboard = [
            [InlineKeyboardButton("🌐 Open Portfolio", url=PORTFOLIO_LINK)],
            [InlineKeyboardButton("« Back to Menu", callback_data="back_main")],
        ]
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    elif data == "contact":
        text = (
            f"📞 *Contact Me*\n\n"
            f"👤 Designer: {DESIGNER_NAME}\n"
            f"📱 Telegram: {CONTACT_TELEGRAM}\n"
            f"📧 Email: {CONTACT_EMAIL}\n"
        )
        if CONTACT_WHATSAPP:
            text += f"💬 WhatsApp: {CONTACT_WHATSAPP}\n"
        text += f"\nInstagram: {INSTAGRAM}\n\nFeel free to message me anytime!"
        keyboard = [[InlineKeyboardButton("« Back to Menu", callback_data="back_main")]]
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    elif data == "about":
        text = (
            f"ℹ️ *About {BUSINESS_NAME}*\n\n"
            f"Hi! I'm {DESIGNER_NAME}, a professional graphic designer specializing in:\n\n"
            "• Logo & Brand Identity\n"
            "• Social Media Design\n"
            "• Print & Packaging\n"
            "• Digital Marketing Assets\n\n"
            "I focus on clean, modern, and memorable designs that help your brand stand out.\n\n"
            "Every project is unique — I work closely with clients to deliver exactly what they need."
        )
        keyboard = [[InlineKeyboardButton("« Back to Menu", callback_data="back_main")]]
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    elif data == "order" or data.startswith("order_"):
        # Start order conversation
        if data.startswith("order_"):
            service_key = data.replace("order_", "")
            context.user_data["service"] = service_key
        else:
            context.user_data.pop("service", None)

        await query.edit_message_text(
            "📝 *Place an Order*\n\n"
            "Please select the service you need:",
            reply_markup=order_services_keyboard(),
            parse_mode="Markdown",
        )
        return SELECT_SERVICE

    elif data == "cancel":
        context.user_data.clear()
        await query.edit_message_text(
            "❌ Order cancelled.\n\nYou can start again anytime from the menu.",
            reply_markup=main_menu_keyboard(),
        )
        return ConversationHandler.END


# ====================== ORDER CONVERSATION ======================

async def select_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "cancel":
        context.user_data.clear()
        await query.edit_message_text(
            "❌ Order cancelled.",
            reply_markup=main_menu_keyboard(),
        )
        return ConversationHandler.END

    if data.startswith("order_"):
        service_key = data.replace("order_", "")
        context.user_data["service"] = service_key
        service_name = SERVICES[service_key]["name"]

        await query.edit_message_text(
            f"✅ Selected: *{service_name}*\n\n"
            "Now, please type your *full name* (or company name):",
            parse_mode="Markdown",
        )
        return CLIENT_NAME

    return SELECT_SERVICE


async def get_client_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["client_name"] = update.message.text.strip()
    await update.message.reply_text(
        "Great! Now describe your project in detail:\n\n"
        "• What do you need?\n"
        "• Preferred style / colors?\n"
        "• Any specific requirements?\n"
        "• Deadline?",
        reply_markup=ReplyKeyboardRemove(),
    )
    return PROJECT_DESCRIPTION


async def get_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["description"] = update.message.text.strip()
    await update.message.reply_text(
        "Perfect. If you have any reference images, logos, or files, "
        "please send them now (you can send multiple).\n\n"
        "When you're done, click *Skip / No files* or just type /done",
        reply_markup=skip_keyboard(),
        parse_mode="Markdown",
    )
    context.user_data["files"] = []
    return REFERENCE_FILES


async def receive_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive photos or documents"""
    if "files" not in context.user_data:
        context.user_data["files"] = []

    if update.message.photo:
        # Get highest resolution photo
        file_id = update.message.photo[-1].file_id
        context.user_data["files"].append({"type": "photo", "file_id": file_id})
        await update.message.reply_text(
            f"✅ Photo received ({len(context.user_data['files'])} file(s) so far).\n"
            "Send more or click Skip / type /done when finished."
        )
    elif update.message.document:
        file_id
