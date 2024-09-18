import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random
import time

# File to store the commands and responses
commands_file = 'commands.json'

# Load commands from file if available
def load_commands():
    try:
        with open(commands_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save commands to file
def save_commands(commands):
    with open(commands_file, 'w') as f:
        json.dump(commands, f, indent=4)

# Initially load the commands from the file
commands = load_commands()

# Function to handle the /teach command to teach the bot multiple responses for a command
def teach_command(update, context):
    user = update.message.from_user
    if len(context.args) < 2:
        update.message.reply_text("Usage: /teach <command> <response>")
        return

    command = context.args[0].lower()  # The command word
    response = ' '.join(context.args[1:])  # The response

    # Save multiple responses for the same command
    if command in commands:
        commands[command].append(response)  # Add the new response to the existing list
    else:
        commands[command] = [response]  # Create a new list if it's a new command
    
    save_commands(commands)
    
    # Show typing action before replying
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    time.sleep(2)  # Simulate typing for 2 seconds

    update.message.reply_text(f"Got it, {user.first_name}! I will now respond to '{command}' with one of the following responses: {commands[command]}")

# Function to handle the /forget command to delete a learned command
def forget_command(update, context):
    user = update.message.from_user
    if len(context.args) < 1:
        update.message.reply_text("Usage: /forget <command>")
        return

    command = context.args[0].lower()

    # Check if the command exists and delete it
    if command in commands:
        del commands[command]
        save_commands(commands)
        
        # Show typing action before replying
        context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        time.sleep(2)  # Simulate typing for 2 seconds
        
        update.message.reply_text(f"Alright, {user.first_name}. I have forgotten the command '{command}'.")
    else:
        update.message.reply_text(f"I don't know the command '{command}' to forget it.")

# Function to handle any text messages and check if they match a learned command
def handle_message(update, context):
    message_text = update.message.text.lower()

    # Check if the message matches a command the bot has learned
    if message_text in commands:
        # Show typing action before sending the response
        context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        time.sleep(2)  # Simulate typing delay
        
        # Get a random response from the list of responses for this command
        response = random.choice(commands[message_text])
        update.message.reply_text(response)
    else:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        time.sleep(5)  # Simulate typing delay
        update.message.reply_text("Sorry, but let response wait 1 or 2 hours, then try sending the message again.")

def main():
    # Replace this with your bot's API token
    token = "6737814588:AAFTgdxC_DjfJGJ6d9svHQn04TR3aiMeC7k"

    # Create the Updater and pass it your bot's token
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Command to teach the bot new responses
    dp.add_handler(CommandHandler("teach", teach_command))

    # Command to forget a learned response
    dp.add_handler(CommandHandler("forget", forget_command))

    # Handle all messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
    
