import tempfile
import json
import os

class History:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        self.history_file = os.path.join(self.temp_dir, "asker_history.json")
        self.max_history_length = 3

    def add(self, question, answer):
        history_item = {"Question": question, "Answer": answer}

        if not os.path.exists(self.history_file):
            with open(self.history_file, "w") as file:
                json.dump([history_item], file)
        else:
            try:
                with open(self.history_file, "r") as file:
                    history = json.load(file)
            except json.JSONDecodeError:
                history = []

            history.append(history_item)
            if len(history) > self.max_history_length:
                history = history[-self.max_history_length:]
                
            with open(self.history_file, "w") as file:
                json.dump(history, file)

    def get(self, n):
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, "r") as file:
                content = file.read().strip() #remove leading + trailing whitespace 
                if not content:  
                    return []
                history = json.loads(content)
            return history[-n:]
        except json.JSONDecodeError:
            # If the file contains invalid JSON, return an empty list
            return []
    
    def clear(self):
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
        else:
            #create the file if it doesnt exist.
            with open(self.history_file, "w") as file:
                pass
