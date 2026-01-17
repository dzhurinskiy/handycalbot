"""Telegram Stars donation handlers."""

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, Message, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PreCheckoutQueryHandler,
    filters,
)

from calendarbot.db.session import async_session_factory
from calendarbot.i18n import get_text
from calendarbot.services.user import UserService

logger = logging.getLogger(__name__)

# Donation amounts in Telegram Stars
DONATION_OPTIONS = [
    (50, "50 Stars"),
    (100, "100 Stars"),
    (500, "500 Stars"),
    (1000, "1000 Stars"),
]


async def donate_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /donate command - show donation options."""
    if not update.effective_user or not update.message:
        return

    # Get user's language
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    # Create buttons for each donation amount
    buttons = []
    row = []
    for amount, label in DONATION_OPTIONS:
        row.append(InlineKeyboardButton(f"* {label}", callback_data=f"donate_{amount}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    # Add custom amount button
    buttons.append(
        [
            InlineKeyboardButton(
                f"* {t.donation.custom_amount_button}", callback_data="donate_custom"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        f"{t.donation.support_title} *\n\n"
        f"{t.donation.support_description}\n\n"
        f"{t.donation.support_helps}\n\n"
        f"{t.donation.select_amount}",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )


async def donate_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle donation amount selection."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    # Get user's language
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    # Handle donate_menu from welcome message button
    if query.data == "donate_menu":
        buttons = []
        row = []
        for amount, label in DONATION_OPTIONS:
            row.append(InlineKeyboardButton(f"* {label}", callback_data=f"donate_{amount}"))
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        buttons.append(
            [
                InlineKeyboardButton(
                    f"* {t.donation.custom_amount_button}", callback_data="donate_custom"
                )
            ]
        )
        keyboard = InlineKeyboardMarkup(buttons)

        await query.edit_message_text(
            f"{t.donation.support_title} *\n\n"
            f"{t.donation.support_description}\n\n"
            f"{t.donation.support_helps}\n\n"
            f"{t.donation.select_amount}",
            reply_markup=keyboard,
            parse_mode="Markdown",
        )
        return

    if query.data == "donate_custom":
        await query.edit_message_text(
            t.donation.custom_amount_prompt,
            parse_mode="Markdown",
        )
        # Store state in context to handle the next message
        if context.user_data is None:
            context.user_data = {}
        context.user_data["awaiting_custom_donation"] = True
        return

    # Extract amount from callback data
    amount = int(query.data.replace("donate_", ""))

    # Send invoice (check that message is accessible)
    if isinstance(query.message, Message):
        await send_donation_invoice(query.message.chat_id, amount, context, t)
        await query.delete_message()


async def custom_donation_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle custom donation amount input."""
    if not update.message or not update.message.text or not update.effective_user:
        return

    # Check if we're expecting a custom donation amount
    if not context.user_data or not context.user_data.get("awaiting_custom_donation"):
        return

    # Clear the state
    context.user_data["awaiting_custom_donation"] = False

    # Get user's language
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    try:
        amount = int(update.message.text.strip())
        if amount < 1 or amount > 10000:
            await update.message.reply_text(t.donation.invalid_amount)
            return
    except ValueError:
        await update.message.reply_text(t.donation.invalid_number)
        return

    # Send invoice
    await send_donation_invoice(update.message.chat_id, amount, context, t)


async def send_donation_invoice(
    chat_id: int, amount: int, context: ContextTypes.DEFAULT_TYPE, t=None
) -> None:
    """Send a Telegram Stars invoice for donation."""
    if t is None:
        t = get_text("en")

    title = "Support HandyCalBot"
    description = f"Donate {amount} Telegram Stars to support HandyCalBot development"
    payload = f"donation_{amount}"

    # Create the invoice
    # For Telegram Stars, we use "XTR" as currency
    prices = [LabeledPrice(label=f"{amount} Stars", amount=amount)]

    try:
        await context.bot.send_invoice(
            chat_id=chat_id,
            title=title,
            description=description,
            payload=payload,
            provider_token="",  # Empty for Telegram Stars
            currency="XTR",  # Telegram Stars currency code
            prices=prices,
            start_parameter=f"donate_{amount}",
        )
    except Exception as e:
        logger.error(f"Failed to send donation invoice: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text=t.donation.donation_error,
        )


async def precheckout_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle pre-checkout query - approve all donations."""
    query = update.pre_checkout_query
    if not query:
        return

    # Always approve donation payments
    await query.answer(ok=True)


async def successful_payment_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle successful payment - thank the user."""
    if not update.message or not update.message.successful_payment:
        return

    payment = update.message.successful_payment
    amount = payment.total_amount

    # Get user's language
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = (
            await user_service.get_user(update.effective_user.id) if update.effective_user else None
        )
        t = get_text(user.language if user else "en")

    await update.message.reply_text(
        f"{t.donation.thank_you}\n\n"
        f"{t.donation.you_donated.format(amount=amount)}\n\n"
        f"{t.donation.thank_you_running} *",
        parse_mode="Markdown",
    )

    if update.effective_user:
        logger.info(f"Received donation of {amount} Stars from user {update.effective_user.id}")


def setup_donation_handlers(app: Application) -> None:
    """Register donation handlers."""
    app.add_handler(CommandHandler("donate", donate_command))
    app.add_handler(CallbackQueryHandler(donate_callback, pattern=r"^donate_"))
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
    # Handle custom donation amount - must be after other handlers
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            custom_donation_handler,
        ),
        group=1,  # Lower priority group
    )
