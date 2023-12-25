from fastapi import FastAPI, Response, HTTPException, Request
import logging
import json

app = FastAPI()


@app.get("/get-emote/")
async def get_emote(id: str = None, mid: str = None):
    try:
        with open('biliEmote.json') as f:
            emotes = json.load(f)
        for emote in emotes['data']['all_packages']:
            if id == emote['id'] or mid == emote['meta']['item_id']:
                return emote
        raise Exception('emote not found.')
    except:
        raise HTTPException(status_code=406, detail="n/a")


@app.get("/")
async def root():
    return {"message": "noxbackup is available"}
