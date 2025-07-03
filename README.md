# raibot-agent
This project provides a python agent that allows a simulated robot to be controlled
via prompts from the user

***Note that these instructions are for a Mac OS machine. You will find equivalent instructions for a Windows machine on the Internet.***

## setup
Once cloned, enter the folder created and set up a virtual python environment:
```
python3 -m venv venv
source venv/bin/activate
```

After creating the virtual environment, install dependencies with the following from the project root:
```
pip install -r requirements.txt
```

You will need to create an Open AI account and retrieve an API key. This then needs to be put in a file called `src/.env` as follows:
```
OPENAI_API_KEY = "<your Open API key>"
ANTHROPIC_API_KEY = "<your Anthropic API key (or leave blank)>" 
```

The code includes an option to use `Claude` im place of `ChatGPT` but this has been found to be unreliable.

## Running
To run, from the `src/` folder, run the following:
```
python3 agent
```
At the prompt `Enter command for Raibot:` enter prompts such as:
```
go from A1 to E5
Starting at A3 go to E1
Start at E5
Go left
Go up
```

## Notes
The grid has no-go areas. See `raibot_tool.py`.
The path taken should be recorded in the path.txt file.
