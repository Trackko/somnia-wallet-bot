#!/usr/bin/env python3
import asyncio
import argparse
import logging
import json
import os
from bot import SomniaWalletBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_activity.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SomniaWalletBot")

async def main():
    parser = argparse.ArgumentParser(description='Somnia Wallet Bot')
    parser.add_argument('--wallets', type=str, default='wallets.json', help='Path to wallet JSON file')
    parser.add_argument('--config', type=str, default='config.json', help='Path to config file')
    parser.add_argument('--days', type=int, default=7, help='Number of days to run the bot')
    parser.add_argument('--mode', type=str, default='auto', choices=['auto', 'interactive'], 
                       help='Bot operation mode: auto or interactive')
    
    args = parser.parse_args()
    
    # Check if files exist
    if not os.path.exists(args.wallets):
        logger.error(f"Wallet file {args.wallets} not found!")
        return
        
    if not os.path.exists(args.config):
        logger.warning(f"Config file {args.config} not found, creating default...")
        default_config = {
            "rpc_url": "https://rpc-testnet.somnia.network",
            "ping_contract": "0x29e5AB2a0E89a698bbC599EaB9f7a2e3950D38Ea",
            "pong_contract": "0xeCb34091A4F2b132562C1B1f9AbA87E8e08F7C25",
            "sUSDT_contract": "0xEA90E4f6DcB636cf736A8d55D8ba935203cdC88F",
            "router_contract": "0xBdF4A9d9d614f96EeE32d0511c5a1d6f7981fb03"
        }
        with open(args.config, 'w') as f:
            json.dump(default_config, f, indent=2)
    
    # Initialize the bot
    bot = SomniaWalletBot(args.wallets, args.config)
    
    if args.mode == 'auto':
        logger.info(f"Starting automated mode for {args.days} days")
        await bot.run_automated_farming(days=args.days)
    else:
        # Interactive mode
        logger.info("Starting interactive mode")
        await interactive_mode(bot)

async def interactive_mode(bot):
    """Interactive CLI mode for the bot"""
    print("\nSomnia Wallet Bot - Interactive Mode")
    print("------------------------------------")
    
    while True:
        print("\nAvailable commands:")
        print("1. List wallets")
        print("2. Check wallet stats")
        print("3. Transfer STT")
        print("4. Swap tokens")
        print("5. Mint token")
        print("6. Mint message NFT")
        print("7. Run automated farming")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "0":
            print("Exiting...")
            break
            
        elif choice == "1":
            print("\nWallet List:")
            for idx, wallet in enumerate(bot.wallets):
                print(f"{idx}: {wallet['address']}")
                
        elif choice == "2":
            wallet_idx = int(input("Enter wallet index: "))
            if 0 <= wallet_idx < len(bot.wallets):
                stats = await bot.get_wallet_stats(wallet_idx)
                print("\nWallet Stats:")
                for key, value in stats.items():
                    print(f"{key}: {value}")
            else:
                print("Invalid wallet index!")
                
        elif choice == "3":
            wallet_idx = int(input("Enter wallet index: "))
            if 0 <= wallet_idx < len(bot.wallets):
                to_address = input("Enter recipient address: ")
                amount = float(input("Enter amount to transfer: "))
                result = await bot.transfer_stt(wallet_idx, to_address, amount)
                print(f"\nTransfer result: {result}")
            else:
                print("Invalid wallet index!")
                
        elif choice == "4":
            wallet_idx = int(input("Enter wallet index: "))
            if 0 <= wallet_idx < len(bot.wallets):
                print("\nAvailable tokens: ping, pong")
                token_in = input("Enter token to swap from: ")
                token_out = input("Enter token to swap to: ")
                amount = float(input("Enter amount to swap: "))
                result = await bot.swap_tokens(wallet_idx, token_in, token_out, amount)
                print(f"\nSwap result: {result}")
            else:
                print("Invalid wallet index!")
                
        elif choice == "5":
            wallet_idx = int(input("Enter wallet index: "))
            if 0 <= wallet_idx < len(bot.wallets):
                print("\nAvailable tokens: ping, pong")
                token_type = input("Enter token type to mint: ")
                result = await bot.mint_token(wallet_idx, token_type)
                print(f"\nMint result: {result}")
            else:
                print("Invalid wallet index!")
                
        elif choice == "6":
            wallet_idx = int(input("Enter wallet index: "))
            if 0 <= wallet_idx < len(bot.wallets):
                message = input("Enter message for NFT: ")
                result = await bot.mint_message_nft(wallet_idx, message)
                print(f"\nNFT mint result: {result}")
            else:
                print("Invalid wallet index!")
                
        elif choice == "7":
            days = int(input("Enter number of days to run farming: "))
            print(f"\nStarting automated farming for {days} days...")
            print("This will run in the background. You can continue using other commands.")
            # Run farming in background
            asyncio.create_task(bot.run_automated_farming(days))
            
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    asyncio.run(main())
