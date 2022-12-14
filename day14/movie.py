import sys
from pathlib import Path
from subprocess import run

from main import INPUT_FILE, Game, Tile, parse
from PIL import Image
from tqdm import tqdm

PICS_DIR = Path(__file__).parent / "pics"
MOVIE_PATH = Path(__file__).parent / "vis.mp4"

MOVIE_LENGTH_SEC = 60
MOVIE_FPS = 60
TOTAL_FRAMES = MOVIE_LENGTH_SEC * MOVIE_FPS

H_BOUNDS = (327, 673)
GAME_STEPS = 3393691


def render(game: Game, frame: int):
    width, height = H_BOUNDS[1] - H_BOUNDS[0], game.height
    img = Image.new(size=(width, height), mode="RGB")
    pixels = img.load()

    for node, tile in game.nodes.items():
        match tile:
            case Tile.Sand:
                color = (255, 255, 0)
            case Tile.Rock:
                color = (255, 255, 255)
        pixels[node.x - width, node.y - height] = color

    img.save(PICS_DIR / f"{frame}.png")


def main():
    if not PICS_DIR.exists():
        PICS_DIR.mkdir()

    frame_step = GAME_STEPS // TOTAL_FRAMES
    game = Game(parse(INPUT_FILE.read_text()))

    print("Rendering frames...")
    for step in tqdm(range(GAME_STEPS)):
        if step % frame_step == 0:
            render(game, step // frame_step)
        try:
            game.tick()
        except RuntimeError:
            break

    print("Rendering video..")
    run(
        [
            "ffmpeg",
            "-framerate",
            str(MOVIE_FPS),
            "-i",
            f"{PICS_DIR.absolute()}/%d.png",
            "-vf",
            "scale='1080:-1'",
            str(MOVIE_PATH),
        ],
        stderr=sys.stderr,
        stdout=sys.stdout,
    )


if __name__ == "__main__":
    main()
