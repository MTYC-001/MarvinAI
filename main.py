# uvicorn main:app
# uvicorn main:app --reload

# Main imports


from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai
from functions.database import store_messages, reset_messages
from functions.openai_request import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech
app = FastAPI()
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
]

# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Check health
@app.get("/health")
async def check_health():
    return {"message": "healthy"}


@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "conversation reset"}

#get
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):

    #get saved audio
    #audio_input = open("sample6.mp3", "rb")

    # save file from frontend
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    #decode audio
    message_decoded = convert_audio_to_text(audio_input)
    
    #Guard to ensure message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio")
    
    chat_response = get_chat_response(message_decoded)

    #Guard to ensure message decoded
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to get response")

    #store messages
    store_messages(message_decoded,chat_response)

    #convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)

        #Guard to ensure message decoded
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get elevenlabs audio response audio")
    
    #create a generator that yields chunks of data
    def iterfile():
        yield audio_output
    
    #return audio file
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

    print(chat_response)
 
    return "Done"

# Post bot response
# Note: not playing in browser when using post request
#@app.post("/post-audio/")
#async def post_audio(file: UploadFile = File(...)):

#    print("hello")