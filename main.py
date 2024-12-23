from fastapi import FastAPI, HTTPException
import json

app = FastAPI()
with open('biliEmote.json') as f:
    emotes = json.load(f)


@app.get("/get-emote/")
async def get_emote(eid: int = None, mid: int = None):
    try:
        for emote in emotes['data']['all_packages']:
            try:
                if eid == emote['id'] or mid == emote['meta']['item_id']:
                    return emote
            except KeyError:
                # TODO: item_id doesnt exist?
                pass
        raise Exception('emote not found.')
    except Exception as e:
        raise HTTPException(status_code=406, detail=str(e))


@app.get("/")
async def root():
    return {"message": "noxbackup is available"}
