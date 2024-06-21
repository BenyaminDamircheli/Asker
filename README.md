# Asker

As someone who is relatively new to programming, I always forget certain commands that I need in my projects. That's why I built Asker.

Asker is the best way to get command related questions, straight in your terminal/command line.  

Currently, you have to set this up with your own API keys, and the only model provider that is supported is OpenAI. However it is very easy to add more. Just clone this repository, and add the new model provider clients/classes to the llm.py file, following what I have done with the OpenAI client. These should show up in the config, but you'll have to double check this.

However, this means that this tool unfortunately costs money, but it is still useful and you'll only be charged a small fraction of a cent per question (depending on the model you use).

# How to use

Asker is super simple to use, just invoke it from the command line and ask a question as follows:

```
>>> ask how to create a python virtual environment
Asker using OpenAI
1. python3 -m venv myenv - Creates a new virtual environment named 'myenv'.
2. source myenv/bin/activate - Activates the virtual environment.
3. deactivate - Deactivates the virtual environment.
```

Here are a couple more examples:

```
>>> ask how to convert video to audio using ffmpeg
Asker using OpenAI
1. ffmpeg -i input.mp4 output.mp3 - Converts video file to audio file.
```

```
>>> ask How do I convert image size in ffmpeg
Asker using OpenAI
1. ffmpeg -i input.jpg -filter:v scale=h=1024 output.jpg - Resizes the image to a height of 1024 pixels.
2. ffmpeg -i input.jpg -filter:v scale=w:h=1:1 output.jpg - Resizes image to width and height that are equal
3. ffmpeg -i input.jpg -filter:v scale=force_original output.jpg - Preserving original aspect ratio.
```

# Commands

## Built in commands

- prev: Shows the results from the previous question.
- --clear: Clears the history
- --version: Shows Asker version
- --model: Shows the model being used (for now always OpenAI)
- --help: Shows this help message

## Running commands

Commands can be run by entering the number of the command you want to run. For example:

```
>>> ask How do I convert image size in ffmpeg
Asker using OpenAI
1. ffmpeg -i input.jpg -filter:v scale=h=1024 output.jpg - Resizes the image to a height of 1024 pixels.
2. ffmpeg -i input.jpg -filter:v scale=w:h=1:1 output.jpg - Resizes image to width and height that are equal
3. ffmpeg -i input.jpg -filter:v scale=force_original output.jpg - Preserving original aspect ratio.

>>> ask 2
Running command: ffmpeg -i input.jpg -filter:v scale=w:h=1:1 output.jpg
<result shows up here if there is one>
```

# Things I may add in the future

- [ ] Add more model providers (you could do this yourself)
- [ ] Add favourites - saved commands you'd want to use and can invoke, similar to running commands regularly.

I also think that the next evolution of something like this is a way to get LLMs to control your computer and automate much of this stuff for you based on prompts. For example, you could ask a sytsem: "can you convert the word documents in my writing folder into pdfs?" Obviously this is very different to what asker is, but it would be something cool to look into in the future. For now Asker is just fine.

The closest thing I have found to what I described is this: https://github.com/OpenInterpreter/open-interpreter

