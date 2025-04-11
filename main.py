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
