# **Flippy Discord Bot**

Flippy is a fun and interactive Discord bot built using Python and the `nextcord` library. It provides users with engaging games such as craps, roulette, coinflip, and a slot machine, along with reward systems and balance tracking.

## **Features**
- **Daily Rewards**: Users can claim daily coins to play games.
- **Balance Tracking**: Keeps track of users' coin balances.
- **Interactive Games**:
  - **Coinflip**: Wager an amount and bet on heads or tails to win big!
  - **Slots**: Spin a slot machine with emoji results and multipliers.
  - **Roulette**: Bet on red, black, or green for exciting chances to win coins.
  - **Craps**: Roll dice in a fast-paced game of chance.
- **Help Command**: Displays all available bot commands.

## **Commands**
Below is a list of available commands and their functionalities:

| Command            | Description                                                                                      |
|--------------------|--------------------------------------------------------------------------------------------------|
| `/daily`           | Claims your daily coin reward (500 coins every 24 hours).                                       |
| `/balance`         | Shows your current coin balance.                                                                |
| `/coinflip`        | Bet on `heads` or `tails`, and wager an amount to win or lose coins.                            |
| `/slots [amount]`  | Wager an amount and spin the slot machine. Win multipliers based on matching emojis.             |
| `/roulette [amount]` | Bet on red, black, or green in a game of roulette. Green has the lowest odds but the highest payout. |
| `/craps [amount]`  | Roll dice to win coins. Match a "point" roll or get a 7/11 to win; rolling 2, 3, or 12 loses.    |
| `/help`            | Displays a list of all available commands and their descriptions.                               |

---

## **Setup Instructions**

Follow these steps to set up and run Flippy on your local machine or a hosting platform like Replit:

### **Prerequisites**
- Python 3.8 or later
- A Discord Developer Bot Token
- Libraries:
  - `nextcord`
  - `wavelink`
  - `flask`

### **1. Clone the Repository**
Clone this repository to your local machine:
```bash
git clone https://github.com/<your-username>/Flippy.git
cd Flippy
```

### **2. Install Dependencies**
Install all required dependencies:
```bash
pip install -r requirements.txt
```

If you're on Replit, dependencies are automatically managed via `replit.nix`.

### **3. Set Up Environment Variables**
Create a `.env` file in the project directory to store your bot token:
```plaintext
Token=<YOUR_BOT_TOKEN>
```

Replace `<YOUR_BOT_TOKEN>` with your Discord Bot token. **Do not share this token.**

### **4. Run the Bot**
Run the bot with the following command:
```bash
python main.py
```

For Replit hosting, the `host.py` file ensures the bot stays online.

---

## **Games Overview**

### **Coinflip**
Bet on heads or tails. If you guess correctly, you win your wagered amount.

### **Slots**
Spin a slot machine with various emoji combinations:
- Match three 🍇 for a **2x multiplier**.
- Match three 🍒 for a **3x multiplier**.
- Other combinations offer higher multipliers.

### **Roulette**
Bet on:
- 🔴 **Red** (45% chance to win).
- ⚫ **Black** (45% chance to win).
- 🟢 **Green** (10% chance, pays 2x).

### **Craps**
Roll dice to win:
- **First Roll**: 7 or 11 wins; 2, 3, or 12 loses.
- **Subsequent Rolls**: Match your "point" roll to win; rolling a 7 loses.

---

## **File Overview**
- **`main.py`**: The core bot code, including all commands and game logic.
- **`host.py`**: Flask server for keeping the bot alive when hosted on platforms like Replit.
- **`user_data.json`**: Tracks users' balances and daily reward data.
- **`.replit`**: Configuration file for running the bot on Replit.
- **`requirements.txt`**: Specifies all dependencies.

---

## **Hosting Flippy**
You can host Flippy on:
1. **Replit**:
   - Add your bot token as a secret in Replit's Secrets Manager.
   - Ensure the `host.py` file is present to keep the bot running.

2. **Local Machine**:
   - Run `python main.py` to start the bot.

3. **Cloud Hosting (Optional)**:
   - Use services like Heroku, AWS, or Google Cloud to host Flippy for long-term use.

---

## **Contact**
If you have any questions, feel free to reach out:
- Discord: tri4ngulum
- GitHub: https://github.com/MithunMahesh
