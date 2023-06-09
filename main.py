import sys
import pygame
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
        self.timer = pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.score = 1
        self.leaderboard = []

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
                elif event.type == pygame.USEREVENT:
                    self.score += 1
            if self.level.run():
                self.draw_text(f"Score: {self.score}", (170, 50), (0, HEIGHT - 100),
                               background=(128, 191, 64), text_color=0, fade=False)
                pygame.display.update()
                self.clock.tick(FPS)
            else:
                if self.play_again():
                    self.score = 0
                    self.level = Level()

    def play_again(self):
        self.leaderboard_sorting()
        while True:
            self.draw_text("GAME OVER, Press R to play again", (WIDTH, 250), (0, 0))
            self.draw_text("LEADERBOARD", (WIDTH / 3, 50), (WIDTH / 3, 250),
                           text_color='black', background='White')
            self.print_leaderboard()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif pygame.key.get_pressed()[pygame.K_r]:
                    return True

    def print_leaderboard(self):
        for index, score in enumerate(self.leaderboard):
            self.draw_text(f"{index + 1}: {score} seconds", (WIDTH/3, 50),(WIDTH/3, 250 + (index+1) * 50),
                           text_color='black', background='White')

    def leaderboard_sorting(self):
        self.leaderboard.append(self.score)
        self.leaderboard.sort()
        self.leaderboard.reverse()
        del self.leaderboard[10:]

    def start_screen(self):
        while True:
            self.draw_text("Use W, A, S, D or the arrow keys to move", (WIDTH, 50), (0, 0))
            self.draw_text("Dodge the spikes and orange orbs", (WIDTH, 50), (0, 50))
            self.draw_text("Press H for this to show up again", (WIDTH, 50), (0, 100))
            self.draw_text("Press enter/return to continue", (WIDTH, 50), (0, 150))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif pygame.key.get_pressed()[pygame.K_RETURN]:
                    return
            pygame.display.update()

    def draw_text(self, string, background_size, screen_pos, text_color=(255, 255, 255), font_size=30,
                  font='Arial', bolded=False, background=(200, 0, 50), fade=True):

        text_holder = pygame.Surface(background_size)
        text_holder.fill(background)
        if fade:
            text_holder.set_alpha(12)
        center = text_holder.get_size()
        center = (center[0] / 2, center[1] / 2)

        my_font = pygame.font.SysFont(font, font_size)
        my_font.set_bold(bolded)
        text = my_font.render(string, False, text_color)
        text_center = text.get_rect(center=center)
        text_holder.blit(text, text_center)

        self.screen.blit(text_holder, screen_pos)
        pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
