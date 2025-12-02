from app import GameApp
from config import GameConfig

if __name__ == "__main__":
    app = GameApp(
        width=GameConfig.WINDOW_WIDTH,
        height=GameConfig.WINDOW_HEIGHT,
        fps=GameConfig.FPS
    )
    app.run()
