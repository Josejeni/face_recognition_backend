from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import threading

app = FastAPI()

# Flag to control the while loop
running = False

# Function to start the while loop in a separate thread
def start_loop1():
    global running
    while running:
        # Your while loop logic here
        print("jo")
        # pass

@app.post('/start_loop')
async def start_loop():
    global running
    if not running:
        running = True
        
        # Start the while loop in a separate thread
        threading.Thread(target=start_loop1).start()
        return {'message': 'Loop started successfully'}
    else:
        return {'message': 'Loop is already running'}

@app.post('/stop_loop')
async def stop_loop():
    global running
    running = False
    return {'message': 'Loop stopped successfully'}
