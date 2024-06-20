import sys
import os
import argparse
import json

from .llm import askLLM
from .history import History

# Add this when it is more extensible.
# from .config import Config

history_manager = History()

def run_commands(question, history):
    if question.lower() == "history":
        history = history_manager.get(1)
        if history:
            prev_answer = json.load(history[-1]["Answer"])
            for i, item in enumerate(history):
                print(str((i+1)) + ". " + "\'" + item["command"] + "\'" + " - " + "\'" + item["desc"] + "\'")
        else:
            print("No history found.")

        print()
        exit()

    
    #check if the question is an int or not
    try:
        index = int(question)
        history = history_manager.get(5)

        
