import io
import telegram
import openai
from pydub import AudioSegment

# Set the path to ffmpeg executable
# Replace "/path/to/ffmpeg" with the actual path to ffmpeg on your system
AudioSegment.ffmpeg = "C:\Users\DELL\Downloads\ffmpeg-snapshot.tar.bz2"

# set the API token for the Telegram bot
TELEGRAM_TOKEN = "5831281159:AAEQhWy3J15NNQZtBGoXlnzXK66DDwcXzwg"

# initialize the Telegram API client
bot = telegram.Bot(TELEGRAM_TOKEN)

# initialize the OpenAI API client
openai.api_key = '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'

# function for handling incoming bot requests


def handle_message(update, context):
    try:
        # get the user's text request
        text = update.message.text

        # check if the text is not empty
        if not text:
            update.message.reply_text("Please provide a valid text request.")
            return

        # use the text generation model to create text
        generated_text = openai.Completion.create(
            engine='text-davinci-002',
            prompt=text,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text

        # use text-to-speech synthesis to create an audio file based on the generated text
        response_audio = openai.TtsVocoder.create(
            text=generated_text,
            voice='en-US-Wavenet-C',
            speed=1,
            format='mp3',
        ).audio

        # create an AudioSegment object from the audio byte array
        audio_segment = AudioSegment.from_file(
            io.BytesIO(response_audio), format='mp3')

        # send the audio file back to the user via Telegram
        bot.send_voice(chat_id=update.message.chat_id, voice=audio_segment)

    except Exception as e:
        # handle any errors that occur during message handling
        update.message.reply_text(
            "An error occurred while processing your request.")
        print(str(e))


# run the bot
if __name__ == "__main__":
    updater = telegram.ext.Updater(token=TELEGRAM_TOKEN, use_context=True)
    updater.dispatcher.add_handler(telegram.ext.MessageHandler(
        telegram.ext.Filters.text, handle_message))
    updater.start_polling()
    updater.idle()
