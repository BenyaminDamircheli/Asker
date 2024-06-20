from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import platform
import re
from .history import History


load_dotenv()



class LLM:
    def __init__(self, client):
        self.client = client
    
    def generating(self):
        print(f"Asker using {self.client}")

class OpenAI(LLM):
    def __init__(self):
        super().__init__("OpenAI")
        self.api_key = os.getenv("OPEN_AI_API_KEY")

    def generate(self, messages):
        self.generating()
        client = OpenAI(api_key=self.api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages
        )
        return {"response": response.choices[0].message.content}


def parse_response(response):
    format = r'\[\s*\{\s*"command"\s*:\s*"(.*?)"\s*,\s*"desc"\s*:\s*"(.*?)"\s*\}\s*(?:,\s*\{\s*"command"\s*:\s*"(.*?)"\s*,\s*"desc"\s*:\s*"(.*?)"\s*\}\s*)*\]'
    matches = re.findall(format, response, re.DOTALL)
    commands = []

    for match in matches:
        for i in range(0, len(matches), 2):
            if match[i] and match[i+1]:
                commands.append({"command": match[i], "desc": match[i+1]})
    return commands

def askLLM(q, client_type):
    messages = []
    history_manager = History() 

    #sytem prompt
    messages.append({
        "role": "system", "content": """Lets play a game of knowledge and formatting. We are playing a command line knowledge game. You are a command line utility that answers questions quickly and briefly in JSON format. If there were a few commands you could have given, show them all. Remember that you print to a console, so make it easy to read when possible. The user is on the operating system: """ + platform.system() + """. Bias towards short answers always, each row should fit in one unwrapped line of the terminal, less than 40 characters! Only 3 rows maximum. Always follow this format:\n[\n{"command": <command string>:, "desc": <description string>},\n]\nIts extremely important to follow this response structure."""
    })

    #fake exmaples given to system so it knows exactly what to output.
    messages.extend([
        {"role": "user", "content": "How do I convert image size in ffmpeg"},
        {"role": "assistant", "content":"""[
            {"command": "ffmpeg -i input.jpg -filter:v scale=h=1024 output.jpg", "desc": "Resizes the image to a height of 1024 pixels."},
            {"command": "ffmpeg -i input.jpg -filter:v scale=w:h=1:1 output.jpg", "desc": "Resizes image to width and height that are equal"},
            {"command": "ffmpeg -i input.jpg -filter:v scale=force_original output.jpg", "desc": "Preserving original aspect ratio."}
        ]"""},

        {"role": "user", "content": "List items in dir by date"},
        {"role": "assistant", "content":"""[
            {"command": "ls -lt", "desc": "List items sorted by date (newest first)."},
            {"command": "ls -ltr", "desc": "Added 'r' sorts by oldest first."}
        ]"""},

        {"role": "user", "content": "How do I make a new docker to run a fresh ubuntu to test on"},
        {"role": "assistant", "content":"""[
            {"command": "docker run -it ubuntu", "desc": "Runs a new Docker container with Ubuntu."},
            {"command": "docker run -it ubuntu bash", "desc": "also opens a bash shell."}
        ]"""},
    ])

    # Retrieve and add history
    history = history_manager.get(5)  ##TODO
    if history:
        for entry in history:
            messages.extend([
                {"role": "user", "content": entry["Question"]},
                {"role": "assistant", "content": entry["Answer"]}
            ])
        
    
    messages.append({"role": "user", "content": q + "\n\n Please submit your response for grading in JSON format."})
    
    #This is here because i want to make this extensible in the future when models all catch up and become better.
    client = {
        "OpenAI": OpenAI(),
    }[client_type]

    response = client.generate(messages)

    if not client:
        raise ValueError(f"Invalid client type: {client_type}")

    try:
        commands = parse_response(response["response"])
        if not commands:
            raise ValueError(f"No commands found in response from: {client_type}, please check if your query is correct.")
        for i, command in enumerate(commands):
            print(f"{i+1}. {command['command']} - {command['desc']}")
    except:
        print(response["response"])
        print(f"hmm... something went wrong... maybe try again later?? or double check your API key and OpenAI account balance.")
        exit()
    
    print()
    print()

        
