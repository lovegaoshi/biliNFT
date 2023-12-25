from fastapi import FastAPI, Response, HTTPException, Request
import logging
import json

app = FastAPI()
with open('biliEmote.json') as f:
    emotes = json.load(f)


@app.get("/get-emote/")
async def get_emote(eid: str = None, mid: str = None):
    try:
        for emote in emotes['data']['all_packages']:
            if eid == emote['id'] or mid == emote['meta']['item_id']:
                return emote
        raise Exception('emote not found.')
    except Exception as e:
        raise HTTPException(status_code=406, detail=str(e))


@app.get("/")
async def root():
    return {"message": "noxbackup is available"}
