import sys
import pygame
from debugger import debug
from settings import *
from level import Level

# Represents overall game
class Game:
    # Initializes pygame, clock, window, and level
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TestGame")
        self.level = Level()

# Handles all the events within the games
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.level.run():
                pygame.display.update()
                self.clock.tick(FPS)
            else:
                if self.play_again():
                    self.level = Level()


    def play_again(self):
        while True:
            self.draw_text('GAME OVER, Press any key to play again')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    return True

    def draw_text(self, text):
        text_holder = pygame.Surface((WIDTH, 50))
        my_font = pygame.font.SysFont('Helvetica', 30)
        my_font.set_bold(True)
        text = my_font.render(text, False, (255, 255, 255))
        text_holder.blit(text, (WIDTH / 3, 10,))
        self.screen.blit(text_holder, (0, 0))
        pygame.display.update()

     def start_screen(self):
         pass

if __name__ == '__main__':
    game = Game()
    game.run()
