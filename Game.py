import time
import pygame
pygame.init()
pygame.display.set_mode((1, 1))

from BaseModule import *
from Constants import *
from LocationModule import *
from TechnicalModule import *
from EntityModule import *
from MagicModule import *
from Instances import *



class Game:
    def __init__(self): 
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN | pygame.SRCALPHA)

        self.main_player = None
        self.main_drawer = None
        self.main_event_handler = None
        self.main_gui = None

        self.gui_state = False

        self.current_location = None
        
    def get_size(self):
        return self.size

    def get_screen(self):
        return self.screen

    def get_location(self):
        return self.current_location

    def get_objects(self):
        return self.current_location.get_objects()

    def get_environment_objects(self):
        return self.current_location.get_environment_objects()

    def set_main_player(self, player):
        self.main_player = player

    def set_main_drawer(self, drawer):
        self.main_drawer = drawer

    def set_main_event_handler(self, event_handler):
        self.main_event_handler = event_handler

    def set_main_gui(self, gui):
        self.main_gui = gui

    def set_main_music_module(self, music_module):
        self.main_music_module = music_module

    def get_main_player(self):
        return self.main_player

    def get_main_drawer(self):
        return self.main_drawer

    def get_main_event_handler(self):
        return self.main_event_handler

    def get_main_gui(self):
        return self.main_gui

    def get_main_music_module(self):
        return self.main_music_module

    def load_location(self, location):
        self.current_location = location
        self.size = self.current_location.get_pixel_size()
        self.main_drawer.set_location()
        self.main_gui.add_info(location.name, 120)

    def spawn_object(self, obj):
        self.current_location.spawn_object(obj)

    def spawn_environment_object(self, obj):
        self.current_location.spawn_ecvironment_object(obj)

    def draw(self):
        self.main_drawer.draw()

    def set_gui_state(self, state):
        self.gui_state = state

    def toggle_gui(self):
        self.gui_state = not self.gui_state

    def get_gui_state(self):
        return self.gui_state

    def close(self):
        pygame.quit()

    def update(self):
        self.main_event_handler.process_events()
        self.main_drawer.update_drawdeltas()
        self.current_location.update()

    def delete_object(self, obj):
        self.current_location.remove_object(obj)

clock = pygame.time.Clock()

UGame = Game()
pygame.display.update()

GameDrawer = Drawer(UGame)
UGame.set_main_drawer(GameDrawer)

GameEventHandler = EventHandler(UGame)
UGame.set_main_event_handler(GameEventHandler)

GameGUI = GUI(UGame)
UGame.set_main_gui(GameGUI)

UMusicModule = MusicModule(UGame)
UGame.set_main_music_module(UMusicModule)

#GameGUI.die()

player = Player(100, 100, UGame)
UGame.set_main_player(player)


SS = Weapon(150, lambda obj: obj.change_health(-10))
SS.set_name("Короткий меч")
SS.load_icon(load_image("textures/items/weapon/short_sword.png"))

LS = Weapon(150, lambda obj: obj.change_health(-20))
LS.set_name("Длинный меч")
LS.load_icon(load_image("textures/items/weapon/long_sword.png"))

HS = Weapon(150, lambda obj: obj.change_health(-30))
HS.set_name("Стальной меч")
HS.load_icon(load_image("textures/items/weapon/hard_sword.png"))


StartLocation = Location(UGame)
StartLocation.load(f"{locations_path}/Start.loc")
StartLocation.set_name("Начало")

GreenFieldsLocation = Location(UGame)
GreenFieldsLocation.load(f"{locations_path}/GreenFields.loc")
GreenFieldsLocation.set_name("Зеленые поля")

CatacombsLocation = Location(UGame)
CatacombsLocation.load(f"{locations_path}/Catacombs.loc")
CatacombsLocation.set_name("Катакомбы")

TheDarkCorridorLocation = Location(UGame)
TheDarkCorridorLocation.load(f"{locations_path}/TheDarkCorridor.loc")
TheDarkCorridorLocation.set_name("Темный коридор")

OldFortressLocation = Location(UGame)
OldFortressLocation.load(f"{locations_path}/OldFortress.loc")
OldFortressLocation.set_name("Старая крепость")

TheLabyrinthLocation = Location(UGame)
TheLabyrinthLocation.load(f"{locations_path}/TheLabyrinth.loc")
TheLabyrinthLocation.set_name("Лабиринт")

TheHellCorridorLocation = Location(UGame)
TheHellCorridorLocation.load(f"{locations_path}/TheHellCorridor.loc")
TheHellCorridorLocation.set_name("Дорога в ад")

TheHellLocation = Location(UGame)
TheHellLocation.load(f"{locations_path}/TheHell.loc")
TheHellLocation.set_name("Ад")


StartLocation.spawn_object(Door(550, 468, UGame, GreenFieldsLocation, (100, 100)))
GreenFieldsLocation.spawn_object(Door(0, 96, UGame, StartLocation, (500, 460)))
GreenFieldsLocation.spawn_object(Door(1025, 732, UGame, CatacombsLocation, (100, 100)))
CatacombsLocation.spawn_object(Door(0, 100, UGame, GreenFieldsLocation, (900, 732)))
CatacombsLocation.spawn_object(Door(2104, 950, UGame, TheDarkCorridorLocation, (100, 70)))
TheDarkCorridorLocation.spawn_object(Door(64, -12, UGame, CatacombsLocation, (2104, 850)))
TheDarkCorridorLocation.spawn_object(Door(2240, 242, UGame, OldFortressLocation, (100, 100)))
OldFortressLocation.spawn_object(Door(64, -12, UGame, TheDarkCorridorLocation, (2240, 150)))
OldFortressLocation.spawn_object(Door(1985, 627, UGame, TheLabyrinthLocation, (100, 100)))
TheLabyrinthLocation.spawn_object(Door(832, 1025, UGame, TheHellCorridorLocation, (64, 130)))
TheHellCorridorLocation.spawn_object(HellDoor(64, 243, UGame, TheLabyrinthLocation, (832, 1100)))
TheHellCorridorLocation.spawn_object(HellDoor(2304, 148, UGame, TheHellLocation, (100, 100)))
GreenFieldsLocation.spawn_object(Drop(200, 200, UGame, SS))


Z1 = Zombie(700, 500, UGame)
Z1.get_item(HealthUpPotion())
Z2 = Zombie(610, 680, UGame)
Z2.get_item(SpeedUpPotion())
Z3 = Zombie(290, 700, UGame)
Z3.get_item(StrengthUpPotion())
Z4 = Zombie(800, 700, UGame)
Z4.get_item(IntelligenceUpPotion())
GreenFieldsLocation.spawn_object(Z1)
GreenFieldsLocation.spawn_object(Z2)
GreenFieldsLocation.spawn_object(Z3)
GreenFieldsLocation.spawn_object(Z4)

Z = Zombie(200, 500, UGame)
CatacombsLocation.spawn_object(Z)
Z = Zombie(700, 800, UGame)
CatacombsLocation.spawn_object(Z)
Z = Zombie(500, 200, UGame)
CatacombsLocation.spawn_object(Z)
Z.get_item(HealthUpPotion())
Z = Zombie(1300, 600, UGame)
CatacombsLocation.spawn_object(Z)
Z = Zombie(1900, 100, UGame)
CatacombsLocation.spawn_object(Z)
Z = Zombie(400, 600, UGame)
CatacombsLocation.spawn_object(Z)
Z = Zombie(700, 600, UGame)
Z.get_item(HealthUpPotion())
CatacombsLocation.spawn_object(Z)
Z = Zombie(1700, 200, UGame)
CatacombsLocation.spawn_object(Z)
Z = Zombie(1800, 200, UGame)
CatacombsLocation.spawn_object(Z)
Z.get_item(MagicUpPotion())
Z = Zombie(1800, 600, UGame)
Z.get_item(HealthUpPotion())
CatacombsLocation.spawn_object(Z)

TheDarkCorridorLocation.spawn_object(MagicDrop(500, 140, UGame, FireballMagic()))
TheDarkCorridorLocation.spawn_object(Zombie(1600, 120, UGame))
TheDarkCorridorLocation.spawn_object(Zombie(1550, 110, UGame))
TheDarkCorridorLocation.spawn_object(Zombie(1570, 130, UGame))
TheDarkCorridorLocation.spawn_object(Zombie(1630, 110, UGame))
TheDarkCorridorLocation.spawn_object(Zombie(1620, 125, UGame))

OldFortressLocation.spawn_object(Drop(325, 500, UGame, LS))
OldFortressLocation.spawn_object(BurningMan(1300, 100, UGame))
OldFortressLocation.spawn_object(BurningMan(1500, 200, UGame))
OldFortressLocation.spawn_object(BurningMan(1700, 150, UGame))
D = DistortedMan(2000, 500, UGame)
D.get_item(HealthUpPotion())
D.get_item(IntelligenceUpPotion())
D.get_item(MagicUpPotion())
D.get_item(MagicUpPotion())
OldFortressLocation.spawn_object(D)

Z = Zombie(300, 80, UGame)
TheLabyrinthLocation.spawn_object(Z)
Z = Zombie(600, 80, UGame)
TheLabyrinthLocation.spawn_object(Z)
Z = Zombie(900, 80, UGame)
TheLabyrinthLocation.spawn_object(Z)
Z = Zombie(1200, 80, UGame)
TheLabyrinthLocation.spawn_object(Z)
Z = Zombie(1500, 80, UGame)
TheLabyrinthLocation.spawn_object(Z)
D = DistortedMan(1800, 500, UGame)
TheLabyrinthLocation.spawn_object(D)
Z = Zombie(1800, 800, UGame)
TheLabyrinthLocation.spawn_object(Z)
D = DistortedMan(1800, 1100, UGame)
TheLabyrinthLocation.spawn_object(D)
Z = Zombie(1800, 1400, UGame)
TheLabyrinthLocation.spawn_object(Z)
D = DistortedMan(1800, 1700, UGame)
TheLabyrinthLocation.spawn_object(D)
B = BurningMan(1700, 1860, UGame)
TheLabyrinthLocation.spawn_object(B)
G = GreyDistortedMan(1400, 1860, UGame)
TheLabyrinthLocation.spawn_object(G)
Z = Zombie(1100, 1860, UGame)
TheLabyrinthLocation.spawn_object(Z)
D = DistortedMan(800, 1860, UGame)
TheLabyrinthLocation.spawn_object(D)
Z = Zombie(500, 1860, UGame)
TheLabyrinthLocation.spawn_object(Z)
Z = Zombie(500, 1860, UGame)
TheLabyrinthLocation.spawn_object(Z)
Z = Zombie(100, 1860, UGame)
TheLabyrinthLocation.spawn_object(Z)
Z = Zombie(100, 1560, UGame)
TheLabyrinthLocation.spawn_object(Z)
Z = Zombie(100, 1260, UGame)
TheLabyrinthLocation.spawn_object(Z)
Z = Zombie(100, 960, UGame)
TheLabyrinthLocation.spawn_object(Z)
B = BurningMan(100, 560, UGame)
TheLabyrinthLocation.spawn_object(B)
D = Drop(300, 300, UGame, HealthUpPotion())
TheLabyrinthLocation.spawn_object(D)
D = Drop(500, 300, UGame, SpeedUpPotion())
TheLabyrinthLocation.spawn_object(D)
D = Drop(700, 300, UGame, MagicUpPotion())
TheLabyrinthLocation.spawn_object(D)
D = Drop(900, 300, UGame, HealthUpPotion())
TheLabyrinthLocation.spawn_object(D)
D = Drop(1100, 300, UGame, StrengthUpPotion())
TheLabyrinthLocation.spawn_object(D)
D = Drop(1300, 300, UGame, HealthUpPotion())
TheLabyrinthLocation.spawn_object(D)
Z = Zombie(1600, 300, UGame)
TheLabyrinthLocation.spawn_object(Z)
Z = Zombie(1600, 800, UGame)
TheLabyrinthLocation.spawn_object(Z)
Z = Zombie(1600, 1300, UGame)
TheLabyrinthLocation.spawn_object(Z)
B = BurningMan(400, 1660, UGame)
TheLabyrinthLocation.spawn_object(B)
Z = Zombie(300, 800, UGame)
TheLabyrinthLocation.spawn_object(Z)
Z = Zombie(300, 1200, UGame)
TheLabyrinthLocation.spawn_object(Z)
B = BurningMan(300, 500, UGame)
TheLabyrinthLocation.spawn_object(B)
D = Drop(1100, 500, UGame, HealthUpPotion())
TheLabyrinthLocation.spawn_object(D)
D = Drop(500, 500, UGame, SpeedUpPotion())
TheLabyrinthLocation.spawn_object(D)
D = Drop(700, 500, UGame, MagicUpPotion())
TheLabyrinthLocation.spawn_object(D)
D = Drop(900, 500, UGame, HealthUpPotion())
TheLabyrinthLocation.spawn_object(D)
TheLabyrinthLocation.spawn_object(D)
B = BurningMan(1470, 1480, UGame)
TheLabyrinthLocation.spawn_object(B)
B = BurningMan(490, 1460, UGame)
TheLabyrinthLocation.spawn_object(B)
B = BurningMan(490, 700, UGame)
TheLabyrinthLocation.spawn_object(B)
B = BurningMan(1300, 700, UGame)
TheLabyrinthLocation.spawn_object(B)

D = Drop(900, 1100, UGame, HealthUpPotion())
TheLabyrinthLocation.spawn_object(D)
D = Drop(900, 900, UGame, SpeedUpPotion())
TheLabyrinthLocation.spawn_object(D)
D = Drop(1100, 850, UGame, MagicUpPotion())
TheLabyrinthLocation.spawn_object(D)
D = Drop(1300, 850, UGame, HealthUpPotion())


TheHellCorridorLocation.spawn_object(MagicDrop(1400, 140, UGame, FrozenballMagic()))
TheHellCorridorLocation.spawn_object(MagicDrop(1700, 140, UGame, HealMagic()))
TheHellCorridorLocation.spawn_object(Drop(600, 120, UGame, HS))

D = DarkBurningMan(1000, 100, UGame)
D.get_item(HealthUpPotion())
TheHellLocation.spawn_object(D)
D = DarkBurningMan(1050, 200, UGame)
D.get_item(MagicUpPotion())
TheHellLocation.spawn_object(D)
D = DarkBurningMan(1100, 300, UGame)
D.get_item(HealthUpPotion())
TheHellLocation.spawn_object(D)
D = DarkBurningMan(1150, 400, UGame)
D.get_item(MagicUpPotion())
TheHellLocation.spawn_object(D)
D = DarkBurningMan(1200, 500, UGame)
D.get_item(HealthUpPotion())
TheHellLocation.spawn_object(D)
D = DarkBurningMan(1250, 600, UGame)
D.get_item(MagicUpPotion())
TheHellLocation.spawn_object(D)
D = DarkBurningMan(1200, 700, UGame)
D.get_item(HealthUpPotion())
TheHellLocation.spawn_object(D)
D = DarkBurningMan(1150, 800, UGame)
D.get_item(MagicUpPotion())
TheHellLocation.spawn_object(D)
D = DarkBurningMan(1100, 900, UGame)
D.get_item(MagicUpPotion())
D.get_item(HealthUpPotion())
TheHellLocation.spawn_object(D)
D = DarkBurningMan(1050, 1000, UGame)
D.get_item(MagicUpPotion())
TheHellLocation.spawn_object(D)
D = DarkBurningMan(1000, 1100, UGame)
D.get_item(MagicUpPotion())
TheHellLocation.spawn_object(D)

Boss = VioletEye(1500, 550, UGame)
TheHellLocation.spawn_object(Boss)

UGame.load_location(StartLocation)
UGame.spawn_object(UGame.get_main_player())

GameGUI.redraw_all()
cur_time = time.time()


UMenu = MainMenu()

while True:
    try:
        UGame.get_main_gui().update()
        UGame.get_main_event_handler().process_events()
        UGame.get_main_music_module().update()
        
        if not UGame.get_gui_state():
            UGame.update()
    
        UGame.draw()

        new_time = time.time()
        try:
            dif = int(1 / (new_time - cur_time))
        except Exception as e:
            pass
        fps_pixmap = MagicFont.render(str(dif), False, (0, 255, 0))
        UGame.screen.blit(fps_pixmap, (1920 - 30 - fps_pixmap.get_rect().width, 30))
        
        pygame.display.flip()
        pygame.event.pump()
        clock.tick(FPS)
        cur_time = new_time
    except pygame.error as e:
        break

pygame.quit()
    
