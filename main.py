from app import GameApp

if __name__ == "__main__":
    app = GameApp(
        width=640,
        height=400,
        fps=60
    )
    app.run()
