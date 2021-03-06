from chatterbot import ChatBot
from chatterbot.comparisons import levenshtein_distance
from chatterbot.trainers import ChatterBotCorpusTrainer


bot = ChatBot(
    'MedBot',
    database='./MedBot.sqlite3',
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter",
    logic_adapters = [
                    {
                        'import_path': 'chatterbot.logic.BestMatch',
                        
                    },
                    {
                        'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                        'threshold': 0.65,
                        'default_response': 'Sorry this information is not available. We will get back to you in 1 day.'
                    }
    ],
    #statement_comparison_function=levenshtein_distance,
    read_only=False
)


bot.set_trainer(ChatterBotCorpusTrainer)

bot.train(
    "chatterbot.corpus.custom"
)
CONVERSATION_ID = bot.storage.create_conversation()

def get_feedback():

    text = input()

    if 'yes' in text.lower():
        return False
    elif 'no' in text.lower():
        return True
    else:
        print('Please type either "Yes" or "No"')
        return get_feedback()


print("Type something to begin...")
# The following loop will execute each time the user enters input
while True:
    try:
        input_statement = bot.input.process_input_statement()
        statement, response = bot.generate_response(input_statement, CONVERSATION_ID)

        bot.output.process_response(response)
        print('\n Is "{}" a correct response to "{}"? \n'.format(response, input_statement))
        if get_feedback():

            print("please input the correct one")
            response1 = bot.input.process_input_statement()
            bot.learn_response(response1, input_statement)
            bot.storage.add_to_conversation(CONVERSATION_ID, statement, response1)
            print("Response added to bot!")

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
