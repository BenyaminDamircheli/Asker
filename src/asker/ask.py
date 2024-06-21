import sys
import os
import argparse
import json

from .llm import askLLM
from .history import History
from .config import Config

config_manager = Config()
history_manager = History()

#checks if user is asking for previous commands, runs previous commands and shows prev answer.
def run_commands(question, history):
    if question.lower() == "prev":
        if history:
            print("Your Asker history:")
            prev_answer = history[-1]["Answer"]
            if isinstance(prev_answer, str):
                prev_answer = json.loads(prev_answer)
            for i, item in enumerate(prev_answer):
                print(f"{i+1}. '{item['command']}' - {item['desc']}")
        else:
            print("No history found.")
        print()
        return

    try:
        index = int(question) - 1
        history = history_manager.get(5)

        if history:
            latest_answer = json.loads(history[-1]["Answer"])

            if 0 <= index < len(latest_answer):
                command = latest_answer[index]["command"]
                print("Running command: " + command)
                os.system(command)
            else:
                print(f"Invalid index. Please choose a number between 1 and {len(latest_answer)}")
        else:
            print("No history found.")
    except (ValueError, json.JSONDecodeError, KeyError, IndexError) as e:
        # If it's not a valid command index, we'll treat it as a question
        pass

def main():

    parser = argparse.ArgumentParser(
        description='Asker is the best way to get answers right in your command line.',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '--version',
        action='version',
        version='0.1.0'
    )

    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear your Asker history'
    )

    parser.add_argument(
        'question',
        nargs='*',
        help='Ask a question to the LLM'
    )

    parser.add_argument(
        '--model',
        type=str,
        choices=['OpenAI'],
        nargs='?',  
        const='OpenAI',  
        help='The model to use for asking the question. For now it is just OpenAI but I may add more in the future.'
    )

    args = parser.parse_args()

    #if user only inputs >>>ask
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        exit()

    if args.clear:
        history_manager.clear()
        print("Asker history cleared.")
        exit()

    try:
        config = config_manager.load_config()  
        model = config['model']
    except:
        config = {'model': 'OpenAI'} 
        config_manager.save_config(config)
    
    if args.model:
        config['model'] = args.model
        config_manager.save_config(config)
        print(f"Asker model set to: {args.model}")
        exit()

    question = ''.join(args.question)
    history = history_manager.get(5)
    run_commands(question, history)

    if question.lower() != "prev" and not question.isdigit():
        askLLM(question, config['model'])


if __name__ == "__main__":
    main()
    



