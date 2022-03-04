from cmath import log
from re import X
from fastapi import FastAPI
from enum import Enum
import uvicorn
import logging

################### Logging ###################
# Write into log file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='../log/playground.log', 
    filemode='w'
)

logger = logging.getLogger(__name__)

# Print to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)


################### Fastapi ###################
app = FastAPI()

################### GET Basics ###################
items = {
    'item_1' : {'title': 'Title One', 'author': 'Author One'},
    'item_2' : {'title': 'Title Two', 'author': 'Author Two'},
    'item_3' : {'title': 'Title Three', 'author': 'Author Three'},
    'item_4' : {'title': 'Title Four', 'author': 'Author Four'},
    'item_5' : {'title': 'Title Five', 'author': 'Author Five'},
}

@app.get("/")
async def my_api():
    return {"message": "hahadao"}

@app.get("/items")
async def get_all_items():
    logger.info("All items getting called")
    return items

@app.get("/items/id/{item_id}")
async def get_item_by_id(item_id: int):
    return {"message": item_id}


################### GET: Enumeration Path Params ###################
class DirectionName(str, Enum):
    north = 'North'
    south = 'South'
    east = 'East'
    west = 'West'

@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction": direction_name, "sub": "Up"}
    elif direction_name == DirectionName.south:
        return {"Direction": direction_name, "sub": "Down"}
    else: 
        return {"Direction": "whatever", "sub": "blabla"}


################### GET: Enhance Path Params ###################
@app.get("/items/name/{item_name}")
async def get_item(item_name: str):
    return items[item_name]


################### GET: Query Params ###################
@app.get("/items/skip/")
async def get_all_items_except(skip_item_name: str):
    temp_items = items.copy()
    del temp_items[skip_item_name]
    return temp_items

if __name__ == "__main__":
    uvicorn.run("playground:app", host="0.0.0.0", port=8000, reload=True)


################### POST Basics ###################
@app.post("/")
async def create_item(item_title, item_author):
    current_last_item = 0
    if len(items) > 0:
        for item in items:
            num = int(item.split('_')[-1])
            if num > current_last_item:
                current_last_item = num
    items[f'item_{current_last_item + 1}'] = {'title': item_title, 'author': item_author}
    return items[f'item_{current_last_item + 1}']


################### PUT Basics ###################
