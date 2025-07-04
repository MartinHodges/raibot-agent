import logging
from flags import DEBUG
from dotenv import load_dotenv
from pydantic import BaseModel
from strands import Agent
from strands.models.openai import OpenAIModel
from save_tool import save_to_txt, clear_file
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient
import json

load_dotenv()

# Quieten agent actions by setting higher log levels
logging.getLogger("strands").setLevel(logging.CRITICAL)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Sets the logging format and streams logs to stderr with minimal output
logging.basicConfig(
    level=logging.CRITICAL if not DEBUG else logging.DEBUG,
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

class RaibotResponse(BaseModel):
  last_location: str
  target_location: str
  status: str
  map:list[list[str]]

model = OpenAIModel(
    model_id="gpt-4o",
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)


prompt = """
    You are controlling a robot called Raibot, on a field made of a 5 by 5 grid.
    The left most column is A, the right most column is E.
    The bottom row is 1, the top row is 5.
    Use the raibot_simulator to control the robot but note that instead of using A to E it uses 1 to 5.
    The robot can move in four directions: up, down, left, and right.
    Given a command from your human operator, you will provide the one word directions only as instructions to the robot
    using the raibot tool. You can find out where the robot is at anytime with the tools you have access to.
    If the user has given the starting location, tell the tool what it is. Or  from the user's command If known, use the starting position from the Raibot or else use the human's starting position.
    The command may define a final target position expected from following the instructions.
    Do not move the robot if a problem occurs.
    Create a 5x5 array that shows you where you can go, where you cannot and where you have not yet been.
    Do not combine multiple move commands into one batch of instructions to the raibot_simulator tool.
    For each batch of instructions, once the raibot_simulator tool has finished moving the robot, save the result along with
    - the robot's starting position
    - the instructions you gave it
    - the final position of the robot
    - the status message from the raibot tool
    to a file called path.txt using the save_to_txt tool.
    When a session starts, reset the path.txt file to an empty file using the clear_file tool.
"""

streamable_http_mcp_client = MCPClient(lambda: streamablehttp_client("http://localhost:3001/mcp"))

# Create an agent with MCP tools
with streamable_http_mcp_client:
    # Get the tools from the MCP server
    tools = streamable_http_mcp_client.list_tools_sync()
    
    agent = Agent(model=model, tools=tools, system_prompt=prompt)

    continue_trip = True

    while continue_trip:
        command = input("Enter command for Raibot: ")

        response = agent(command)

        result = agent.structured_output(RaibotResponse, "Extract status of last robot movement")
        if DEBUG or True: print("\n\nResult:", result)

        continue_trip = result.last_location != result.target_location