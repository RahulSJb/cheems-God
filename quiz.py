import json
import telebot

bot = telebot.TeleBot("6676043211:AAGNkf2FS086azR0iaN9UTlnbvuJQp6hBNI")

def load_poll_data():
    try:
        with open('poll_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"questions": []}

def save_poll_data(data):
    with open('poll_data.json', 'w') as file:
        json.dump(data, file, indent=4)

@bot.message_handler(content_types=['poll'])
def process_poll(message):
    try:
        if message.poll is not None:
            question = message.poll.question.split('] ', 1)[-1]  # Remove the question number if present
            options = [option.text for option in message.poll.options]
            correct_option_id = getattr(message.poll, 'correct_option_id', None)

            poll_data = {
                "question": question,
                "options": options,
                "correct_option_id": correct_option_id
            }

            # Load existing poll data
            poll_data_json = load_poll_data()
            questions_list = poll_data_json["questions"]

            # Add new question data to the list
            questions_list.append(poll_data)
            
            # Update poll data JSON file
            save_poll_data(poll_data_json)

            # Send success message
            bot.send_message(message.chat.id, "Poll data saved successfully")
        else:
            print("This message does not contain a poll.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error:{e}")

@bot.message_handler(commands=['db'])
def send_database(message):
    try:
        with open('poll_data.json', 'rb') as file:
            bot.send_document(message.chat.id, file)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error:{e}")
        print("Error:", e)

bot.polling()
