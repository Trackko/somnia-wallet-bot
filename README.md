# Somnia Wallet Bot

A sophisticated bot for managing multiple wallets on the Somnia testnet with human-like transaction behavior.

## Overview

This bot automates Web3 interactions with the Somnia testnet while maintaining natural transaction patterns. It supports managing up to 100 wallets and distributes activities throughout the day to mimic human behavior.

## Features

### Web3 Functionality
- ✅ Transfer STT tokens between wallets
- ✅ Swap $PING and $PONG tokens
- ✅ Mint $PING and $PONG tokens
- ✅ Mint message NFTs
- ✅ Deploy token contracts
- ✅ Query wallet balances and statistics

### Advanced Management
- ✅ Support for 100+ wallets from a JSON file
- ✅ Human-like transaction behavior with random delays
- ✅ Variable gas prices to appear natural
- ✅ Daily transaction limits (3-4 transactions per wallet)
- ✅ Random wallet rotation to distribute activity
- ✅ Comprehensive activity logging

## Getting Started

### Prerequisites
- Python 3.8+
- Somnia testnet connection
- Wallet private keys

### Installation

1. Clone the repository:
```bash
git clone https://github.com/trackko/somnia-wallet-bot.git
cd somnia-wallet-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create wallet configuration:
Create a `wallets.json` file with your wallet details:
```json
[
  {
    "address": "0x123abc...",
    "private_key": "0xdef456..."
  },
  {
    "address": "0x789xyz...",
    "private_key": "0xuvw012..."
  }
  // Add up to 100 wallets
]
```

4. Update configuration:
Check and modify `config.json` if needed:
```json
{
  "rpc_url": "https://rpc-testnet.somnia.network",
  "ping_contract": "0x29e5AB2a0E89a698bbC599EaB9f7a2e3950D38Ea",
  "pong_contract": "0xeCb34091A4F2b132562C1B1f9AbA87E8e08F7C25",
  "sUSDT_contract": "0xEA90E4f6DcB636cf736A8d55D8ba935203cdC88F",
  "router_contract": "0xBdF4A9d9d614f96EeE32d0511c5a1d6f7981fb03"
}
```

### Usage

#### Automated Mode
Run the bot in automated mode for a specified number of days:

```bash
python main.py --days 30 --mode auto
```

The bot will:
- Randomly select wallets each day
- Execute 3-4 transactions per wallet per day
- Distribute transactions throughout the day
- Use human-like behavior patterns

#### Interactive Mode
Control the bot manually with interactive commands:

```bash
python main.py --mode interactive
```

In interactive mode, you can:
- List wallets
- Check wallet statistics
- Perform specific transactions
- Start automated farming

## Security Considerations

- **IMPORTANT**: Never commit your `wallets.json` file containing private keys
- Add `wallets.json` to your `.gitignore` file
- Consider encrypting wallet information for additional security
- Be aware of gas costs and monitor wallet balances

## Customization

### Transaction Types
Modify the `execute_random_activity` method in `bot.py` to adjust transaction types and frequencies.

### Timing Parameters
Adjust the delays in `run_automated_farming` to change the distribution of transactions:

```python
# For testing (shorter delays)
await asyncio.sleep(random.randint(60, 300))  # 1-5 minutes

# For production (realistic delays)
await asyncio.sleep(random.randint(1800, 14400))  # 30 mins to 4 hours
```

### Gas Price Variation
Modify the `_get_gas_price_with_variation` method to change how gas prices are calculated.

## Monitoring

The bot creates detailed logs in `bot_activity.log`, which you can monitor to track:
- Transaction successes and failures
- Wallet activities
- Daily limits and timing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Use it responsibly and in accordance with Somnia testnet terms of service. The authors are not responsible for any misuse of this software.
