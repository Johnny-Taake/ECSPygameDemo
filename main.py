from app import GameApp
from logger import setup_logging
from config import GameConfig

if __name__ == "__main__":
    setup_logging()

    app = GameApp(
        width=GameConfig.WINDOW_WIDTH,
        height=GameConfig.WINDOW_HEIGHT,
        fps=GameConfig.FPS,
    )
    app.run()
