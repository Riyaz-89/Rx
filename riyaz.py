import os
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome! Please upload a `.c` file, and I will compile it for you."
    )

# Function to handle uploaded files
def handle_file(update: Update, context: CallbackContext) -> None:
    file = update.message.document

    # Check if the uploaded file is a `.c` file
    if not file.file_name.endswith(".c"):
        update.message.reply_text("Please upload a valid `.c` file.")
        return

    # Create a directory for downloads if it doesn't exist
    os.makedirs("downloads", exist_ok=True)
    file_path = f"downloads/{file.file_name}"

    # Download the file
    file.get_file().download(file_path)

    update.message.reply_text(
        f"File `{file.file_name}` received. Compiling..."
    )

    # Compile the file using gcc
    output_file = file.file_name.replace(".c", "")
    compile_command = f"gcc {file_path} -o downloads/{output_file} -lz -lpthread -static"
    try:
        result = subprocess.run(
            compile_command, shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            update.message.reply_text(
                "Compilation successful! Sending the compiled file."
            )
            update.message.reply_document(document=open(f"downloads/{output_file}", "rb"))
        else:
            update.message.reply_text(f"Compilation failed:\n{result.stderr}")
    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)}")

# Function to handle errors
def error(update: Update, context: CallbackContext) -> None:
    print(f"Update {update} caused error {context.error}")

def main() -> None:
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    updater = Updater("7882806571:AAFa-R6wXrrUj3u9eGmlnBqZiCs82jvD-Oo")
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))

    # File upload handler
    dispatcher.add_handler(MessageHandler(Filters.document, handle_file))

    # Error handler
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
