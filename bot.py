import logging
import json
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
from config import load_config
from wallet import SomniaWallet

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SomniaWalletBot:
    def __init__(self, config):
        """Initialize the bot with configuration."""
        self.config = config
        self.wallet = SomniaWallet(config)
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /start is issued."""
        user = update.effective_user
        await update.message.reply_html(
            f"Hi {user.mention_html()}! I'm the Somnia Wallet Bot. Use /help to see available commands."
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /help is issued."""
        help_text = """
Available commands:
/start - Start the bot
/help - Show this help message
/balance - Check your wallet balance
/deposit - Get deposit address
/withdraw <address> <amount> - Withdraw funds
/price - Check current Somnia token price
        """
        await update.message.reply_text(help_text)

    async def balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check wallet balance."""
        user_id = update.effective_user.id
        balance = self.wallet.get_balance(user_id)
        await update.message.reply_text(f"Your current balance: {balance} SOMN")

    async def deposit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate deposit address."""
        user_id = update.effective_user.id
        address = self.wallet.get_deposit_address(user_id)
        await update.message.reply_text(f"Send SOMN to this address:\n\n{address}")

    async def withdraw(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Withdraw funds."""
        user_id = update.effective_user.id
        args = context.args
        
        if len(args) != 2:
            await update.message.reply_text("Usage: /withdraw <address> <amount>")
            return
            
        address, amount = args[0], args[1]
        
        try:
            amount = float(amount)
        except ValueError:
            await update.message.reply_text("Amount must be a number.")
            return
            
        result = self.wallet.withdraw(user_id, address, amount)
        
        if result["success"]:
            await update.message.reply_text(f"Withdrawal successful! Transaction ID: {result['tx_id']}")
        else:
            await update.message.reply_text(f"Withdrawal failed: {result['message']}")

    async def price(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check Somnia token price."""
        try:
            # Mock API call for now - replace with actual API endpoint
            price = 0.125  # Example price in USD
            price_change = 5.2  # Example price change percentage
            await update.message.reply_text(f"SOMN Price: ${price:.4f} USD (24h change: {price_change}%)")
        except Exception as e:
            logger.error(f"Error fetching price: {e}")
            await update.message.reply_text("Error fetching current price.")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle user messages."""
        # Simple echo for now - can be expanded later
        await update.message.reply_text("Use /help to see available commands.")

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks."""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        if data == "balance":
            user_id = update.effective_user.id
            balance = self.wallet.get_balance(user_id)
            await query.edit_message_text(text=f"Your current balance: {balance} SOMN")
        elif data == "price":
            price = 0.125  # Example price
            await query.edit_message_text(text=f"SOMN Price: ${price:.4f} USD")

    def run(self, token=None):
        """Run the bot."""
        if token is None:
            token = self.config.get("BOT_TOKEN")
            
        application = Application.builder().token(token).build()
        
        # Register command handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("balance", self.balance))
        application.add_handler(CommandHandler("deposit", self.deposit))
        application.add_handler(CommandHandler("withdraw", self.withdraw))
        application.add_handler(CommandHandler("price", self.price))
        
        # Register message handlers
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Register button callback handler
        application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Start the Bot
        if self.config.get("MODE") == "webhook":
            application.run_webhook(
                listen=self.config.get("WEBHOOK_LISTEN", "0.0.0.0"),
                port=self.config.get("WEBHOOK_PORT", 8443),
                url_path=token,
                webhook_url=f"{self.config.get('WEBHOOK_URL')}/{token}"
            )
        else:
            application.run_polling()
            
    def run_interactive(self):
        """Run the bot in interactive CLI mode for testing."""
        print("Running in interactive mode")
        print("Available commands: balance, deposit, withdraw, price, exit")
        
        user_id = 12345  # Mock user ID for testing
        
        while True:
            command = input("> ").strip().lower()
            
            if command == "exit":
                break
            elif command == "balance":
                balance = self.wallet.get_balance(user_id)
                print(f"Balance: {balance} SOMN")
            elif command == "deposit":
                address = self.wallet.get_deposit_address(user_id)
                print(f"Deposit address: {address}")
            elif command.startswith("withdraw"):
                parts = command.split()
                if len(parts) != 3:
                    print("Usage: withdraw <address> <amount>")
                    continue
                    
                _, address, amount = parts
                try:
                    amount = float(amount)
                except ValueError:
                    print("Amount must be a number")
                    continue
                    
                result = self.wallet.withdraw(user_id, address, amount)
                if result["success"]:
                    print(f"Withdrawal successful! Transaction ID: {result['tx_id']}")
                else:
                    print(f"Withdrawal failed: {result['message']}")
            elif command == "price":
                print("SOMN Price: $0.125 USD (24h change: 5.2%)")
            else:
                print("Unknown command. Available commands: balance, deposit, withdraw, price, exit")
