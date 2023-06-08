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
        self.level.run()
        self.start_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif pygame.key.get_pressed()[pygame.K_h]:
                    self.start_screen()
            if self.level.run():
                pygame.display.update()
                self.clock.tick(FPS)
            else:
                if self.play_again():
                    self.level = Level()

    def play_again(self):
        while True:
            self.draw_text('GAME OVER, Press r to play again', (255, 255, 255), (WIDTH, 50), (0, HEIGHT - 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif pygame.key.get_pressed()[pygame.K_r]:
                    return True

    def draw_text(self, text, color, size, pos):
        text_holder = pygame.Surface(size)
        my_font = pygame.font.SysFont('Helvetica', 30)
        my_font.set_bold(True)
        text = my_font.render(text, False, color)
        text_holder.blit(text, (WIDTH / 3, 10,))
        self.screen.blit(text_holder, pos)
        pygame.display.update()

    def start_screen(self):
        while True:
            self.draw_text("Use W, A, S, D or the arrow keys to move", (255, 255, 255), (WIDTH, 50), (0, 0))
            self.draw_text("Dodge the spikes and orange orbs", (255, 255, 255), (WIDTH, 50), (0, 50))
            self.draw_text("Press h for this to show up again", (255, 255, 255), (WIDTH, 50), (0, 100))
            self.draw_text("Press enter/return to continue", (255, 255, 255), (WIDTH, 50), (0, 150))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif pygame.key.get_pressed()[pygame.K_RETURN]:
                    return
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
