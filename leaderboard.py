import json
import os
import time
from datetime import datetime
from pathlib import Path

import requests

SESSION = os.environ["SESSION"]  # aoc session cookie
LEADERBOARD_ID = os.environ["LEADERBOARD_ID"]
LEADERBOARD_URL = (
    f"https://adventofcode.com/2022/leaderboard/private/view/{LEADERBOARD_ID}.json"
)
REFRESH_DELAY_MIN = 15  # as specified in API rules

CACHE_PATH = Path(__file__).parent / ".cache.json"


def get_data() -> dict:
    if (
        not CACHE_PATH.exists()
        or (time.time() - CACHE_PATH.stat().st_mtime) > REFRESH_DELAY_MIN * 60
    ):
        print("Downloading new data...")
        r = requests.get(LEADERBOARD_URL, cookies={"session": SESSION})
        if r.ok:
            CACHE_PATH.write_text(json.dumps(r.json(), indent=4))
        else:
            print(f"Unable to make a request: {r.status_code} {r.text}")
            exit(1)
    return json.loads(CACHE_PATH.read_text())


def timestamp_to_str(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%H:%M:%S %d %b %Y")


def completion(data: dict):
    members = data["members"].values()

    for day in range(1, 25):
        completions = {
            m["name"]: m["completion_day_level"].get(str(day)) for m in members
        }
        if not any(completions.values()):
            return

        print(f"Day {day}")
        for part in ("1", "2"):
            print(f"  Part {part}")
            print_sorted(
                {
                    k: v[part]["get_star_ts"] if v and part in v else None
                    for k, v in completions.items()
                }
            )
        print()


def print_sorted(stars: dict[str, int]):
    s = sorted(stars.items(), key=lambda kv: kv[1] if kv[1] else 99999999999999999)
    for i, (name, timestamp) in enumerate(s, start=1):
        comp_time = timestamp_to_str(timestamp) if timestamp else "None"
        print(f"    {i}. {name:<20} {comp_time}")


if __name__ == "__main__":
    completion(get_data())
