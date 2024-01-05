from collections import deque
import discord
import asyncio

DISCORD_TOKEN = "###############################################" # insert bot token

CHANNEL_ID = 0 #insert channel id

prev_timestamp = ""
file_path = r"####################" # insert file path to latest.log folder

intents = discord.Intents.default()
intents.messages = True  
client = discord.Client(intents=intents)

async def send_message_to_channel(channel_id, message):
    channel = client.get_channel(channel_id)

    if channel:
        await channel.send(message)
    else:
        print(f"Channel with ID {channel_id} not found.")


async def monitor_file():
    global prev_timestamp

    while not client.is_closed():
        with open(file_path, 'r') as input_file:
            last_lines = deque(maxlen=100)

            for line in input_file:
                last_lines.append(line.rstrip())

            for line in last_lines:
                # Vote Party
                if(line.rstrip()[11:] == "[Render thread/INFO]: [System] [CHAT] Vote » Thank you for voting! You can claim an entry in the next 5 minutes 0 seconds with /entry"):
                    timestamp = line[:10]
                
                    if prev_timestamp != timestamp:
                        prev_timestamp = timestamp
                        await send_message_to_channel(CHANNEL_ID, "@here Vote party is starting")

                # KOTH
                if(line.rstrip()[11:] == "[Render thread/INFO]: [System] [CHAT] Info » KOTH is starting in 5 minutes."):
                    timestamp = line[:10]
                
                    if prev_timestamp != timestamp:
                        prev_timestamp = timestamp
                        await send_message_to_channel(CHANNEL_ID, "@here KOTH is starting in 5 minutes")

                # Airdrop
                if(line.rstrip()[11:] == "[Render thread/INFO]: [System] [CHAT] Info » There is an airdrop happening in 10m, 0s."):
                    timestamp = line[:10]
                
                    if prev_timestamp != timestamp:
                        prev_timestamp = timestamp
                        await send_message_to_channel(CHANNEL_ID, "@here Airdrop is starting in 10 minutes")

                # Parkour
                if(line.rstrip()[11:] == "[Render thread/INFO]: [System] [CHAT] Info » Parkour just started. Type /parkour to join"):
                    timestamp = line[:10]
                
                    if prev_timestamp != timestamp:
                        prev_timestamp = timestamp
                        await send_message_to_channel(CHANNEL_ID, "@here Parkour is starting")     

                # Fishing
                if(line.rstrip()[11:] == "[Render thread/INFO]: [System] [CHAT] Info » A fishing contest for the largest fish has started."):
                    timestamp = line[:10]
                
                    if prev_timestamp != timestamp:
                        prev_timestamp = timestamp
                        await send_message_to_channel(CHANNEL_ID, "@here Fishing contest is starting")   

    # Remove comments if you want to see log messages
        # for line in last_lines:
        #     print(line.rstrip()[11:])

        input_file.close()

        # Run every 30 seconds
        await asyncio.sleep(30)


try:
    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user.name}')

        client.loop.create_task(monitor_file())

    client.run(DISCORD_TOKEN)

except FileNotFoundError:
    print(f"Error opening the file: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
