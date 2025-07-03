from pydantic import BaseModel
from strands import tool
from flags import DEBUG

class RaibotInstructions(BaseModel):
    start: str
    instructions: list[str]

class RaibotResponse(BaseModel):
    status: str
    status_message: str
    last_location: str

class RaibotMoveResult(BaseModel):
    x: int
    y: int
    status: str

robot_column = 0
robot_row = 0

GRID = [
    "+++++", #5
    "+++++", #4
    "+++X+", #3
    "+++++", #2
    "+++++", #1
    #ABCDE
    ]

#D2 = 3,4

def goto(delta_x: int, delta_y: int, error: str) -> RaibotMoveResult:
    global robot_column, robot_row

    if error:
        return RaibotMoveResult(x=robot_column, y=robot_row, status=error)

    x = robot_column + delta_x
    y = robot_row + delta_y

    if x < 1:
       return RaibotMoveResult(x=robot_column, y=robot_row, status="error: Raibot cannot move left, already at the left edge.")
    if x > 5:
       return RaibotMoveResult(x=robot_column, y=robot_row, status="error: Raibot cannot move right, already at the right edge.")
    if y < 1:
       return RaibotMoveResult(x=robot_column, y=robot_row, status="error: Raibot cannot move down, already at the bottom edge.")
    if y > 5:
       return RaibotMoveResult(x=robot_column, y=robot_row, status="error: Raibot cannot move up, already at the top edge.")

    if GRID[4-(y-1)][x-1] == 'X':
        return RaibotMoveResult(x=robot_column, y=robot_row, status=f"error: Raibot cannot move to an obstacle at {column_to_letter(x)}{y}.")

    robot_column = x
    robot_row = y

    return RaibotMoveResult(x=x, y=y, status="success")

def column_to_letter(column: int) -> str:
    if 1 <= column <= 5:
        return chr(ord('A') + column - 1)
    return 0

@tool
def raibot(start: str, instructions: list[str]) -> RaibotResponse:
    global robot_column, robot_row

    if not robot_column:
        robot_column = ord(start[0].upper()) - ord('A') + 1
    if not robot_row:
        robot_row = int(start[1])

    if DEBUG: print(f"Raibot starting at: {column_to_letter(robot_column)}{robot_row}")
    if DEBUG:print(f"Raibot instructions: {instructions}")

    error = ""

    for instruction in instructions:
        if DEBUG: print(f"Processing instruction: {instruction}")
        delta_x = 0
        delta_y = 0

        if instruction == "up":
            delta_y = 1
        elif instruction == "down":
            delta_y = -1
        elif instruction == "left":
            delta_x = -1
        elif instruction == "right":
            delta_x = 1
        else:
            error = f"Invalid instruction: {instruction}"
        moveResult = goto(delta_x, delta_y, error)
        if moveResult.status != "success":
            if DEBUG: print(f"Error encountered: {moveResult.status}")
            return RaibotResponse(
                status="error",
                status_message=moveResult.status,
                new_location=f"{column_to_letter(robot_column)}{robot_row}"
            )
        else:
            robot_column = moveResult.x
            robot_row = moveResult.y
        if DEBUG:print(f"Raibot now at: {column_to_letter(robot_column)}{robot_row}")

    if DEBUG: print(f"Raibot new position: {column_to_letter(robot_column)}{robot_row}")

    return RaibotResponse(
        status="success",
        status_message=f"Raibot received instruction: start at: {start} and then follow these instructions: {instructions}",
        last_location=f"{column_to_letter(robot_column)}{robot_row}"
    )
