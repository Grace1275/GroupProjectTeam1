from character_class import Character
from main_config import FPS, game_state
from world.game_over_screen import GameOverScreen
from world.game_screen_classes import MapScreen
import pygame
from menu_class import Menu
import sys
from world.high_scores_screen import HighScoreScreen
from utilities.timer import Timer
from utilities.bars_classes import StressBar, GamesBar
from prototypes.ines_duarte.random_useful_code import hitbox_visible_square
from utilities.intro_bubble import IntroBubble
from quizgame import QuizGame
from typing_game import TypingGame
from wellbeing_room import WellbeingGame
from maze import MazeGame
from fightgame import FoodFight
from world.victory_screen_screen import VictoryScreen
# from win_class import VictoryScreen

class Game:
    def __init__(self):
        # self.manager = manager
        self.map_screen = MapScreen()
        self.menu = Menu()
        self.player = Character(self.map_screen.screen, "assets/sprites/girl_sprite.png", 2, "#ff00d6", 64, 64)
        self.clock = pygame.time.Clock()
        self.dt = 0
        # instantiating Bar Class and giving coordinates
        self.stress_bar = StressBar(900, 23, 70, 16, 10)
        self.games_bar = GamesBar(510, 23, 70, 16, 1)
        # instantiating Timer and passing timer duration
        self.timer = Timer(1800)
        # creating a pygame for to set how often timer updates, every second
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.intro_text = IntroBubble(self.map_screen.screen, 125, 30, '')
        self.high_scores = HighScoreScreen()
        self.game_over = GameOverScreen()
        self.library = QuizGame()
        self.classroom = TypingGame(self.map_screen.screen)
        self.counselling_office = WellbeingGame()
        self.it_dept = MazeGame()
        self.cafeteria = FoodFight()
        self.victory_screen = VictoryScreen()
        self.state = "Playing"
        self.running = True
        self.games_won = {
        "library": "Not won",
        "cafeteria": "Not won",
        "counselling_office": "Not won",
        "classroom": "Not won",
        "it_dept": "Not won"
    }

    def update_game_status(self, building_name):
        if building_name == "library" and self.games_won["library"] != self.library.victory_status:
            self.games_won["library"] = self.library.victory_status
            if self.library.victory_status == "Won":
                self.games_bar.wins += 1
                self.victory_condition()
            elif self.library.victory_status == "Lost":
                self.stress_bar.update(1)
        elif building_name == "cafeteria" and self.games_won["cafeteria"] != self.cafeteria.victory_status:
            self.games_won["cafeteria"] = self.cafeteria.victory_status
            if self.cafeteria.victory_status == "Won":
                self.games_bar.wins += 1
                self.victory_condition()
            elif self.cafeteria.victory_status == "Lost":
                self.stress_bar.update(1)
        elif building_name == "classroom" and self.games_won["classroom"] != self.classroom.victory_status:
            self.games_won["classroom"] = self.classroom.victory_status
            if self.classroom.victory_status == "Won":
                self.games_bar.wins += 1
                self.victory_condition()
            elif self.classroom.victory_status == "Lost":
                self.stress_bar.update(1)
        elif building_name == "it_dept" and self.games_won["it_dept"] != self.it_dept.victory_status:
            self.games_won["it_dept"] = self.it_dept.victory_status
            if self.it_dept.victory_status == "Won":
                self.games_bar.wins += 1
                self.victory_condition()

            elif self.it_dept.victory_status == "Lost":
                self.stress_bar.update(1)


    def victory_condition(self):
        if self.games_bar.wins == self.games_bar.max_wins:
            global game_state
            game_state = "Victory"

    def game_over_condition(self):
        if self.timer.timer_duration <= 0 or self.stress_bar.stress == self.stress_bar.max_stress:
            global game_state
            game_state = "Game Over"

    def star_score(self):
        if self.timer.timer_duration >= (self.timer.initial_duration * 2 // 3):
            return "5 Stars"
        elif self.timer.timer_duration >= (self.timer.initial_duration // 3):
            return "4 Stars"
        else:
            return "3 Stars"


    def loop(self):
        while self.running:
            global game_state

            self.dt = self.clock.tick(FPS)/1000


            if game_state != "Main Menu" and game_state != "High Scores" and game_state != self.player.character_location:
                print(f"Game state updated to: {self.player.character_location}")
                game_state = self.player.character_location
                if self.player.character_location != "Map":
                    self.player.character_location = "Map"

            # Victory status logic
            self.update_game_status("library")
            self.update_game_status("cafeteria")
            self.update_game_status("classroom")
            self.update_game_status("it_dept")

            self.game_over_condition()
            # main game_state engine
            if game_state == "Main Menu":
                print(f"In Main Menu state.")
                self.menu.display(self.map_screen.screen)
                self.menu.handle_input()
                # So this is where if checks if the game_state is diferent than the menu specifc variable and if so updates
                if game_state != self.menu.next_game_state:
                    print(f"Game state updated to: {self.menu.next_game_state}")
                    game_state = self.menu.next_game_state
                    # the set the menu variable back to default
                    self.menu.next_game_state = "Main Menu"


            elif game_state == "High Scores":
                print(f"In High Scores state.")
                self.high_scores.draw()
                self.high_scores.handler()
                if game_state != self.high_scores.menu:
                    print(f"Game state updated to: {self.high_scores.menu}")
                    game_state = self.high_scores.menu
                    self.high_scores.menu = "High Scores"

            elif game_state == "Map":
                self.dt = self.clock.tick(FPS) / 1000
                # print(f"In Map state.")
                self.map_screen.draw()
                self.player.animate(self.map_screen.screen)
                self.player.move(400, self.dt)
                # drawing the bars and timers and the matching texts
                # stress bars
                self.stress_bar.draw(self.map_screen.screen)
                self.stress_bar.draw_text(self.map_screen.screen)
                # Challenge wins
                self.games_bar.draw(self.map_screen.screen)
                self.games_bar.draw_text(self.map_screen.screen)
                # timer
                self.timer.countdown(self.map_screen.screen)
                self.intro_text.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.intro_text.enter_pressed = True
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                    if event.type == pygame.USEREVENT:
                        self.timer.timer_duration -= 1

                # checks if the game state matches building and is not won
            elif game_state == "library" and self.games_won["library"] == "Not won":
                # this is meant to update the stress bar every time you go there, not finished
                    self.stress_bar.update()
                    print(f"In library state.")
                    # call the minigame
                    self.library.main()
                    # this is checking if the mini game variable that holds the game state which is called player location is set to map
                    # and if so, changes game state to map and
                    if self.library.player_location == "Map":
                        print("Transitioning to Map...")
                        # this moves player down when going back to map so its not auto triggering the entrance and get stuck in a loop
                        self.player.player_position.y += 10
                        self.player.character_rect.topleft = self.player.player_position
                        print(f"Game state updated to: {self.library.player_location}")
                        game_state = "Map"

            elif game_state == "classroom" and self.games_won["classroom"] == "Not won":
                self.stress_bar.update()
                print(f"In classroom state.")
                self.classroom.run()
                if self.classroom.player_location == "Map":
                     self.player.player_position.y += 10
                     self.player.character_rect.topleft = self.player.player_position
                     print(f"Game state updated to: {self.classroom.player_location}")
                     game_state = "Map"

            elif game_state == "counselling_office":
                print(f"In counselling office state.")
                self.counselling_office.game_loop()
                if self.counselling_office.player_location == "Map":
                     self.player.player_position.y += 10
                     self.player.character_rect.topleft = self.player.player_position
                     print(f"Game state updated to: {self.counselling_office.player_location}")
                     game_state = "Map"

            elif game_state == "it_dept" and self.games_won["it_dept"] == "Not won":
                self.stress_bar.update()
                print(f"In it_dept state.")
                self.it_dept.run_game()
                if self.it_dept.player_location == "Map":
                     self.player.player_position.y += 20
                     self.player.character_rect.topleft = self.player.player_position
                     print(f"Game state updated to: {self.it_dept.player_location}")
                     game_state = "Map"

            elif game_state == "cafeteria" and self.games_won["cafeteria"] == "Not won":
                self.stress_bar.update()
                print(f"In cafeteria state.")
                self.cafeteria.fight_loop()
                if self.cafeteria.player_location == "Map":
                     self.player.player_position.y += 20
                     self.player.character_rect.topleft = self.player.player_position
                     print(f"Game state updated to: {self.cafeteria.player_location}")
                     game_state = "Map"

            elif game_state == "Victory":
                print("Games won. In victory state.")
                self.victory_screen.stars = self.victory_screen.star_calculator(self.timer.timer_duration, self.timer.initial_duration)
                self.victory_screen.victory_loop(self.timer.get_time_taken(), self.star_score())

            elif game_state == "Game Over":
                print(f"In Game over state state.")
                self.game_over.draw()
                self.game_over.handler()

            pygame.display.flip()



if __name__ == "__main__":
    game = Game()
    game.loop()