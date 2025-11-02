from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from storage import StorageAPI
from plugin import PluginManager

app = FastAPI()
app.mount("/webadmin", StaticFiles(directory="webadmin"), name="webadmin")

storage = StorageAPI('data/database.db')
plugins = PluginManager('plugins', storage)

ADMIN_USER_ID = 7142531263
ADMIN_USERNAME = "KAHDOW"

@app.get("/api/ping")
async def ping():
    return {"status": "ok"}

@app.post("/api/check_admin")
async def check_admin(request: Request):
    data = await request.json()
    user_id = int(data.get("user_id", 0))
    username = str(data.get("username", ""))
    is_admin = (user_id == ADMIN_USER_ID or username.lower() == ADMIN_USERNAME.lower())
    return {"admin": is_admin}

@app.get("/api/stats")
async def get_stats():
    stats = await storage.get_all_stats()
    return {"stats": stats}

@app.get("/api/users")
async def get_users():
    users = await storage.get_users()
    return {"users": [
        {"id": u[0], "nickname": u[1], "rank": u[2], "blocked": u[3]}
        for u in users
    ]}

@app.post("/api/set_user_rank")
async def set_user_rank(request: Request):
    data = await request.json()
    await storage.set_user_rank(data["user_id"], data["rank"])
    return {"status": "ok"}

@app.post("/api/block_user")
async def block_user(request: Request):
    data = await request.json()
    await storage.block_user(data["user_id"])
    return {"status": "ok"}

@app.post("/api/unblock_user")
async def unblock_user(request: Request):
    data = await request.json()
    await storage.unblock_user(data["user_id"])
    return {"status": "ok"}

@app.get("/api/groups")
async def get_groups():
    groups = await storage.get_groups()
    return {"groups": [
        {"id": g[0], "title": g[1], "blocked": g[2]}
        for g in groups
    ]}

@app.post("/api/block_group")
async def block_group(request: Request):
    data = await request.json()
    await storage.block_group(data["group_id"])
    return {"status": "ok"}

@app.post("/api/unblock_group")
async def unblock_group(request: Request):
    data = await request.json()
    await storage.unblock_group(data["group_id"])
    return {"status": "ok"}

@app.get("/api/help")
async def get_help():
    h = await storage.get_help_text()
    return {"help": h}

@app.post("/api/set_help")
async def set_help(request: Request):
    data = await request.json()
    await storage.set_help_text(data["text"])
    return {"status": "ok"}

@app.get("/api/plugins")
async def get_plugins():
    plist = plugins.get_plugins_list()
    return {"plugins": plist}

@app.post("/api/toggle_plugin")
async def toggle_plugin(request: Request):
    data = await request.json()
    await storage.set_plugin_status(data["name"], data["enabled"])
    return {"status": "ok"}

@app.post("/api/restart")
async def restart(request: Request):
    os._exit(1)
    return {"status": "restarting"}

@app.post("/api/leave_group")
async def leave_group(request: Request):
    # TODO: реализовать через main.py (бота)
    return {"status": "not_implemented"}