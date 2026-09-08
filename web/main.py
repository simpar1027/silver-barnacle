from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="StandClick Beta")

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"

app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


# =========================
# ИГРОКИ В ПАМЯТИ
# =========================

players = {}

next_player_id = 1000000


def create_player(telegram_id: int, username: str = "Player"):
    global next_player_id

    player_id = next_player_id
    next_player_id += 1

    players[telegram_id] = {
        "id": player_id,
        "username": username,
        "gold": 0,
        "skins": [],
        "equipped": []
    }

    return players[telegram_id]


def get_or_create_player(
    telegram_id: int,
    username: str = "Player"
):
    if telegram_id not in players:
        return create_player(telegram_id, username)

    return players[telegram_id]


# =========================
# WEB
# =========================

@app.get("/")
async def index():
    return FileResponse(WEB_DIR / "index.html")


@app.get("/api/status")
async def status():
    return {
        "game": "StandClick",
        "version": "Beta",
        "players": len(players)
    }


@app.get("/api/players")
async def get_players():
    result = []

    for player in players.values():
        result.append({
            "id": player["id"],
            "username": player["username"],
            "gold": player["gold"],
            "skins": len(player["skins"]),
            "equipped": len(player["equipped"])
        })

    return {
        "players": result,
        "total": len(result)
    }
