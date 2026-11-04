from game_class import Game


while True:
    game=Game()
    game.Initialize()
    while game.mIsRunning:
        game.Loop()
    if not game.bContinue:
        break