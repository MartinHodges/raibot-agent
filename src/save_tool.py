from strands import tool
from datetime import datetime
from flags import DEBUG

@tool
def clear_file(filename: str) -> str:
    if not filename:
        return "No filename provided for saving."
    
    if not filename.endswith(".txt"):
        filename += ".txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("New file created.\n")
    
    return f"File {filename} created successfully."

@tool
def save_to_txt(filename: str, start: str, instructions: list[str], final: str, target: str, status_message: str) -> str:

    if not filename:
        return "No filename provided for saving."

    if not start or not instructions:
        return "No data provided for saving."
    
    if not filename.endswith(".txt"):
        filename += ".txt"

    if not target:
        target = "No target specified"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Instruction Output ---\nTimestamp: {timestamp}\nStart: {start}\nInstructions: {instructions}\nStatus Message: {status_message}\nFinal Location: {final}\nTarget: {target}\n--- End of Instruction Output ---\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"