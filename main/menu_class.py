import pygame
from main_config import *
import sys
# from game_class import game
from world.game_screen_classes import MapScreen
import time

class Menu:
    def __init__(self):
        self.font_path = "assets/main_menu/PressStart2P-Regular.ttf"
        self.title_font = pygame.font.Font(self.font_path, 40)
        self.option_font = pygame.font.Font(self.font_path, 30)
        self.click_sound = pygame.mixer.Sound("assets/main_menu/click.mp3")
        self.start_sound = pygame.mixer.Sound("assets/main_menu/starts.mp3")
        self.menu_options = ["Start Game", "High Scores", "Quit"]
        self.menu_background = pygame.image.load("assets/main_menu/thesisquest.png").convert()
        self.selected_option = 0
        # new variable to contain the menu game stated that will be used to update the main game loop
        # always reset back to its own menu
        self.next_game_state = "Main Menu"

    def setup_music(self):
        pygame.mixer.music.load("assets/main_menu/lofi1.mp3")
        pygame.mixer.music.play(-1)

    def display(self, display):
        display.blit(self.menu_background, (0, 0))
        title_text = self.title_font.render("Main Menu", True, WHITE)
        display.blit(
            title_text,
            (
                SCREEN_WIDTH // 2 - title_text.get_width() // 2,
                120,
            ),
        )

        for i, option in enumerate(self.menu_options):
            color = PURPLE if i == self.selected_option else WHITE
            option_text = self.option_font.render(option, True, color)
            display.blit(
                option_text,
                (
                    SCREEN_WIDTH // 2 - option_text.get_width() // 2,
                    180 + i * 45,
                ),
            )

        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.click_sound.play()
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_UP:
                    self.click_sound.play()
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    self.start_sound.play()
                    self.select_option()
                    print("enter key pressed")

    def select_option(self):
        if self.selected_option == 0:  # Start Game
            print(f"selected option: {self.selected_option}")
            self.next_game_state = "Map"
            print(f"The next game state is {self.next_game_state}")
            pygame.mixer.music.load("assets/main_menu/mapmusic.mp3")
            pygame.mixer.music.play(-1)
        elif self.selected_option == 1:  # High Scores
            print(f"selected option: {self.selected_option}")
            self.next_game_state = "High Scores"
        elif self.selected_option == 2:  # Quit
            pygame.quit()
            sys.exit()

