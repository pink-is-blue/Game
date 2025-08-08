
import os, sys, pygame
from engine.player import Player
from rooms.main_room import MainRoom
from rooms.burger_room import BurgerRoom
from rooms.plane_room import PlaneRoom
from rooms.book_room import BookRoom
pygame.init()
try: pygame.mixer.init()
except Exception: pass
W, H = 1280, 720
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Loomian Legacy — Fan Scene (Pygame)")
clock = pygame.time.Clock()
class Game:
    def __init__(self):
        self.state = "start"
        self.font_big = pygame.font.Font(None, 86)
        self.font = pygame.font.Font(None, 42)
        self.player = Player(100, int(H*0.7)-64)
        self.main_room = MainRoom(screen)
        self.burger_room = BurgerRoom(screen)
        self.plane_room = PlaneRoom(screen)
        self.book_room = BookRoom(screen)
        self.current_room = "main"; self.pause = False
    def draw_start(self):
        screen.fill((8,10,12))
        t = self.font_big.render("Loomian Legacy — Fan Scene", True, (230, 220, 210))
        screen.blit(t, (W//2 - t.get_width()//2, H//2 - 120))
        s = self.font.render("Press Enter to Start", True, (210, 205, 195))
        screen.blit(s, (W//2 - s.get_width()//2, H//2))
    def draw(self):
        if self.state == "start": self.draw_start(); return
        if self.current_room == "main": self.main_room.draw(self.player)
        elif self.current_room == "burger": self.burger_room.draw(self.player)
        elif self.current_room == "plane": self.plane_room.draw()
        elif self.current_room == "books": self.book_room.draw()
        if self.pause:
            overlay = pygame.Surface((W, H), pygame.SRCALPHA); overlay.fill((0,0,0,180)); screen.blit(overlay, (0,0))
            ptxt = self.font.render("Paused — Press ESC to resume", True, (240,240,240)); screen.blit(ptxt, (W//2 - ptxt.get_width()//2, H//2 - 20))
    def update(self, dt, keys):
        if self.state == "start" or self.pause: return
        if self.current_room == "main":
            self.book_room.stop_music(); self.main_room.update(self.player, keys)
        elif self.current_room == "burger":
            self.book_room.stop_music(); self.burger_room.update(self.player, keys)
        elif self.current_room == "plane":
            self.book_room.stop_music(); self.plane_room.update(dt)
        elif self.current_room == "books":
            self.book_room.ensure_music()
    def on_click(self, pos):
        if self.current_room == "burger": self.burger_room.click(pos)
        elif self.current_room == "books": self.book_room.click(pos)
    def interact(self):
        if self.current_room == "main":
            target = self.main_room.handle_interact(self.player)
            if target:
                self.current_room = target; self.player.rect.topleft = (100, int(H*0.7)-64)
        elif self.current_room == "plane":
            self.plane_room.interact(self.player.rect)
        elif self.current_room == "books":
            self.book_room.interact(self.player.rect)
    def go_back(self): self.current_room = "main"
def run():
    game = Game(); running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN:
                if game.state == "start" and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER): game.state = "playing"
                elif event.key == pygame.K_ESCAPE:
                    if game.state == "start": running = False
                    else:
                        if game.pause: game.pause = False
                        elif game.current_room != "main": game.go_back()
                        else: game.pause = True
                elif event.key == pygame.K_e: game.interact()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: game.on_click(event.pos)
        keys = pygame.key.get_pressed(); game.update(dt, keys); game.draw(); pygame.display.flip()
    pygame.quit()
if __name__ == "__main__": run()
