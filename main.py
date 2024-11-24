import nextcord
from nextcord.ext import commands
from nextcord.shard import EventItem
from nextcord.ext import commands
from nextcord.ui import View, Button
import wavelink
import random
import os
import datetime
import asyncio
import json
from host import host

bot_version = "0.0.1"

intents = nextcord.Intents.all()
client = nextcord.Client()
bot = commands.Bot(command_prefix=".", intents=intents)

games = ["Coinflip"]


@bot.event
async def on_ready():
  print("Bot Ready!")
  await bot.change_presence(activity=nextcord.Activity(
    type=nextcord.ActivityType.playing, name=f"{games[0]}"))





class CrapsView(nextcord.ui.View):

  def __init__(self, interaction: nextcord.Interaction, amount: int):
    super().__init__()
    self.interaction = interaction
    self.dice_emojis = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
    self.user_id = str(interaction.user.id)
    self.data = read_user_data(self.user_id)
    self.coins = self.data["coins"]
    self.point = None
    self.message = None
    self.amount = amount

  async def roll_dice(self):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return dice1, dice2

  async def on_timeout(self):
    self.clear_items()
    await self.message.edit(view=None)
    await self.interaction.response.send_message("Craps game timed out.")

  @nextcord.ui.button(label="Roll",
                      style=nextcord.ButtonStyle.primary,
                      custom_id="roll_dice")
  async def on_roll(self, button: nextcord.ui.Button,
                    interaction: nextcord.Interaction):
    if interaction.user.id != self.interaction.user.id:
      # Only the original user who initiated the game can interact with the buttons
      return

    if self.coins < self.amount:
      await interaction.response.send_message(
        "You do not have enough coins. Check your balance.")
      self.stop()
      return

    await interaction.response.defer()
    dice1, dice2 = await self.roll_dice()
    total = dice1 + dice2
    roll_message = f"You rolled: {self.dice_emojis[dice1]} {self.dice_emojis[dice2]} (Total: {total})"

    if not self.point:
      if total in [7, 11]:
        self.coins += self.amount
        result_message = "\nCongratulations! You win!"
      elif total in [2, 3, 12]:
        self.coins -= self.amount
        result_message = "\nCraps! You lose."
      else:
        self.point = total
        result_message = f"\nPoint is {self.point}. Click 'Roll' to roll the dice again."
      await self.message.edit(content=roll_message + result_message)
      if total in [7, 11, 2, 3, 12]:
        self.stop()
    else:
      if total == self.point:
        self.coins += self.amount
        result_message = "\nCongratulations! You win!"
      elif total == 7:
        self.coins -= self.amount
        result_message = "\nSeven out! You lose."
      else:
        result_message = f"\nPoint is {self.point}. Click 'Roll' to roll the dice again."
      await self.message.edit(content=roll_message + result_message)
      if total == self.point or total == 7:
        self.stop()

    self.data["coins"] = self.coins
    write_user_data(self.user_id, self.data)


@bot.slash_command(name="craps", description="Play a game of craps")
async def craps(interaction: nextcord.Interaction, amount: int):
  if amount <= 0:
    await interaction.response.send_message(
      "The amount must be a positive integer.")
    return

  view = CrapsView(interaction, amount)
  view.message = await interaction.response.send_message(
    "Let's play craps! Click 'Roll' to roll the dice.", view=view)


class RouletteView(nextcord.ui.View):

  def __init__(self, amount):
    super().__init__()
    self.amount = amount

  async def animate_roulette(self, message):
    emojis = ["🔴", "⚫", "🟢"]
    for _ in range(3):
      await asyncio.sleep(1)
      await message.edit(
        content=f"Spinning roulette... {random.choice(emojis)}")

  @nextcord.ui.button(label="🔴 Red", style=nextcord.ButtonStyle.primary)
  async def red(self, button: nextcord.ui.Button,
                interaction: nextcord.Interaction):
    user_id = str(interaction.user.id)
    data = read_user_data(user_id)
    coins = data["coins"]

    if coins >= self.amount:
      message = await interaction.response.send_message("Spinning roulette...")
      await self.animate_roulette(message)

      result = random.choices(["red", "black", "green"], weights=[45, 45,
                                                                  10])[0]
      if result == "red":
        new_coins = coins + self.amount
        data["coins"] = new_coins
        write_user_data(user_id, data)
        await message.edit(
          content=
          f"The roulette landed on 🔴 Red! You won **{self.amount}** {':coin:'} coins!"
        )
      else:
        new_coins = coins - self.amount
        data["coins"] = new_coins
        write_user_data(user_id, data)
        await message.edit(
          content=
          f"The roulette landed on ⚫ Black! You lost **{self.amount}** {':coin:'} coins."
        )
    else:
      await interaction.response.send_message(
        f"You do not have enough {':coin:'} coins. Check your balance. Place a lower bet or claim the daily reward!"
      )
    self.stop()

  @nextcord.ui.button(label="⚫ Black", style=nextcord.ButtonStyle.primary)
  async def black(self, button: nextcord.ui.Button,
                  interaction: nextcord.Interaction):
    user_id = str(interaction.user.id)
    data = read_user_data(user_id)
    coins = data["coins"]

    if coins >= self.amount:
      message = await interaction.response.send_message("Spinning roulette...")
      await self.animate_roulette(message)

      result = random.choices(["red", "black", "green"], weights=[45, 45,
                                                                  10])[0]
      if result == "black":
        new_coins = coins + self.amount
        data["coins"] = new_coins
        write_user_data(user_id, data)
        await message.edit(
          content=
          f"The roulette landed on ⚫ Black! You won **{self.amount}** {':coin:'} coins!"
        )
      else:
        new_coins = coins - self.amount
        data["coins"] = new_coins
        write_user_data(user_id, data)
        await message.edit(
          content=
          f"The roulette landed on 🔴 Red! You lost **{self.amount}** {':coin:'} coins."
        )
    else:
      await interaction.response.send_message(
        f"You do not have enough {':coin:'} coins. Check your balance. Place a lower bet or claim the daily reward!"
      )
    self.stop()

  @nextcord.ui.button(label="🟢 Green", style=nextcord.ButtonStyle.primary)
  async def green(self, button: nextcord.ui.Button,
                  interaction: nextcord.Interaction):
    user_id = str(interaction.user.id)
    data = read_user_data(user_id)
    coins = data["coins"]

    if coins >= self.amount:
      message = await interaction.response.send_message("Spinning roulette...")
      await self.animate_roulette(message)

      result = random.choices(["red", "black", "green"], weights=[45, 45,
                                                                  10])[0]
      if result == "green":
        new_coins = coins + self.amount * 2
        data["coins"] = new_coins
        write_user_data(user_id, data)
        await message.edit(
          content=
          f"The roulette landed on 🟢 Green! You won **{self.amount * 2}** {':coin:'} coins!"
        )
      else:
        new_coins = coins - self.amount
        data["coins"] = new_coins
        write_user_data(user_id, data)
        if result == "red":
          await message.edit(
            content=
            f"The roulette landed on 🔴 Red! You lost **{self.amount}** {':coin:'} coins."
          )
        else:
          await message.edit(
            content=
            f"The roulette landed on ⚫ Black! You lost **{self.amount}** {':coin:'} coins."
          )
    else:
      await interaction.response.send_message(
        f"You do not have enough {':coin:'} coins. Check your balance. Place a lower bet or claim the daily reward!"
      )
    self.stop()


@bot.slash_command(name="roulette", description="Play a roulette game")
async def roulette(interaction: nextcord.Interaction, amount: int):
  if amount <= 0:
    await interaction.response.send_message(
      "The amount must be a positive integer.")
    return

  view = RouletteView(amount)
  await interaction.response.send_message("Choose your bet:", view=view)


def read_user_data(user_id):
  with open("user_data.json", "r") as f:
    data = json.load(f)
  if str(user_id) in data:
    return data[str(user_id)]
  else:
    new_data = {"coins": 500, "last_collected": None}
    data[str(user_id)] = new_data
    write_user_data(user_id, new_data)
    return new_data


def write_user_data(user_id, data):
  with open("user_data.json", "r") as f:
    all_data = json.load(f)
  all_data[str(user_id)] = data
  with open("user_data.json", "w") as f:
    json.dump(all_data, f)


@bot.slash_command(name="balance",
                   description="Returns your current coin balance")
async def balance(interaction: nextcord.Interaction):
  user_id = interaction.user.id
  data = read_user_data(user_id)
  balance = data["coins"]
  await interaction.response.send_message(
    f"Your balance is **{balance}** :coin: coins!")


@bot.slash_command(
  name="coinflip",
  description=
  "Choose 'heads' or 'tails', wager an amount, and flip a coin to win big")
async def coinflip(interaction: nextcord.Interaction, choice: str,
                   amount: int):
  if amount <= 0:
    await interaction.response.send_message(
      "The amount must be a positive integer.")
    return

  user_id = str(interaction.user.id)
  choices = ["heads", "tails"]
  bot_choice = random.choice(choices)

  if choice.lower() not in choices:
    await interaction.response.send_message(
      "Invalid choice. Please choose either 'heads' or 'tails'.")
    return

  data = read_user_data(user_id)
  coins = data["coins"]

  if coins >= amount:
    if choice.lower() == bot_choice:
      new_coins = coins + amount
      data["coins"] = new_coins
      write_user_data(user_id, data)
      await interaction.response.send_message(
        f"The coin landed on {bot_choice} so you won **{amount}** {':coin:'} coins!"
      )
    else:
      new_coins = coins - amount
      data["coins"] = new_coins
      write_user_data(user_id, data)
      await interaction.response.send_message(
        f"The coin landed on {bot_choice} so you lost **{amount}** {':coin:'} coins."
      )
  else:
    await interaction.response.send_message(
      f"You do not have enough {':coin:'} coins. Check your balance. Place a lower bet or claim the daily reward!"
    )


@bot.slash_command(name='daily', description='Claims your daily coin rewards')
async def daily(interaction: nextcord.Interaction):
  user_id = str(interaction.user.id)
  data = read_user_data(user_id)
  now = datetime.datetime.now()
  last_collected = data["last_collected"]
  if last_collected is not None:
    last_collected = datetime.datetime.fromisoformat(last_collected)
    time_since_last_collected = now - last_collected
    if time_since_last_collected < datetime.timedelta(hours=24):
      remaining_time = datetime.timedelta(hours=24) - time_since_last_collected
      remaining_hours = remaining_time.seconds // 3600
      remaining_minutes = (remaining_time.seconds % 3600) // 60
      message = f"You must wait **{remaining_hours}hr {remaining_minutes}m** to collect your next daily reward."
      await interaction.response.send_message(message)
    else:
      data["last_collected"] = now.isoformat()
      if last_collected is None:
        data["coins"] = 1000
        message = f"You have collected your daily reward and earned **500** {':coin:'} coins!"
      else:
        data["coins"] += 500
        message = f"You have collected your daily reward and earned **500** {':coin:'} coins!"
      write_user_data(user_id, data)
      await interaction.response.send_message(message)
  else:
    data["last_collected"] = now.isoformat()
    data["coins"] = 1000
    write_user_data(user_id, data)
    await interaction.response.send_message(
      f"You have collected your daily reward and earned **500** {':coin:'} coins!"
    )


# slot machine emojis
display_emojis = ['🍇', '🍒', '🍊', '🍉', '🍓', '🍋', '🍑', '🍎', '🥝', '🍍']
emojis = ['🍇', '🍒', '🍊', '🍉', '🍓']


# helper function to generate a random slot machine result
def generate_result():
  if random.random() < .26:
    random_emoji = random.choice(emojis)
    if random_emoji == '🍇':
      multiplier = 2
      return ['🍇', '🍇', '🍇', multiplier]
    elif random_emoji == '🍒':
      multiplier = 3
      return ['🍒', '🍒', '🍒', multiplier]
    elif random_emoji == '🍊':
      multiplier = 4
      return ['🍊', '🍊', '🍊', multiplier]
    elif random_emoji == '🍉':
      multiplier = 5
      return ['🍉', '🍉', '🍉', multiplier]
    elif random_emoji == '🍓':
      multiplier = 6
      return ['🍓', '🍓', '🍓', multiplier]
  else:
    # losing result - emojis are randomly selected
    return [random.choice(display_emojis) for _ in range(3)]


# slash command for the slot machine game
@bot.slash_command(description="Play a slot machine game")
async def slots(interaction: nextcord.Interaction, amount: int):
  user_id = str(interaction.user.id)
  user_data = read_user_data(user_id)
  if amount <= 0:
    await interaction.response.send_message(
      "Your bet must be greater than zero!")
    return
  if user_data['coins'] < amount:
    await interaction.response.send_message(
      "You don't have enough coins to make this bet!")
    return

  # deduct the bet amount from the user's coins
  user_data['coins'] -= amount
  write_user_data(user_id, user_data)

  # generate the slot machine result
  result = generate_result()

  # check if the user won or lost
  if result[0] == result[1] == result[2]:
    winnings = amount + (amount * result[3])
    user_data['coins'] += winnings
    write_user_data(user_id, user_data)
    await interaction.response.send_message(
      f"The slot machine spins...\n\n{result[0]} {result[1]} {result[2]}\n**{result[3]}x  Multiplier**\n\nYou won **{amount * result[3]}** {':coin:'} coins!"
    )
  else:
    await interaction.response.send_message(
      f"The slot machine spins...\n\n{result[0]} {result[1]} {result[2]}\n\nYou lost **{amount}** {':coin:'} coins!"
    )


class HelpView(nextcord.ui.View):

  def __init__(self):
    super().__init__()
    self.embed = nextcord.Embed(title="Game Commands",
                                description=self.get_page_content(),
                                color=0x02F0FF)
    self.embed.set_footer(text="Page 1 of 1")

  def get_page_content(self):
    return (
      "**/daily**\nClaims your daily coin rewards.\n\n"
      "**/balance**\nReturns your current coin balance.\n\n"
      "**/coinflip [choice] [amount]**\nChoose 'heads' or tails', wager an amount, and flip a coin to win big!\n\n"
      "**/slots [amount]**\nWager an amount at a slot machine with a 25% chance to hit different multipliers!\n\n"
      "**/roulette [choice] [amount]**\nWager an amount and choose red, black or green. Green has the lowest odds but highest payout!\n\n"
      "**/craps [amount]**\nWager an amount and roll two dice. On the first roll, a 7 or 11 wins. A 2, 3, or 12 loses. Any other number sets a 'point'. After the point is set, roll the same number to win or lose by rolling a 7.\n\n"
    )

  async def on_timeout(self):
    self.clear_items()
    self.stop()


@bot.slash_command(
  name="help",
  description="Displays all the commands available to use with this bot")
async def help_command(interaction: nextcord.Interaction):
  view = HelpView()
  await interaction.response.send_message(embed=view.embed, view=view)
  await view.wait()


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  if message.content.startswith("!Monkey"):
    await message.channel.send("This is a test!")
  if message.content.startswith("!Help"):
    await message.channel.send("Helping")


host()
my_secret = os.environ['Token value']
bot.run(my_secret)
