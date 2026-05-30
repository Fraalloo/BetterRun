import pygame as pg
import random
import math
from src.config.config import WIDTH, HEIGHT, FPS
from src.config.colors import BLUE, RED, GREEN, WHITE, YELLOW

class Player:
    def __init__(self):
        self.radius = 20
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.color = BLUE
        self.is_jumping = False
        self.jump_timer = 0
        self.jump_cooldown = 0
        self.shoot_cooldown = 0

    def update(self, target_x, target_y, jumping):
        self.x = max(self.radius, min(WIDTH - self.radius, target_x))
        self.y = max(self.radius, min(HEIGHT - self.radius, target_y))

        if jumping and self.jump_timer == 0 and self.jump_cooldown == 0:
            self.is_jumping = True
            self.jump_timer = FPS
            self.jump_cooldown = FPS * 4
        
        if self.jump_timer > 0:
            self.jump_timer -= 1
            if self.jump_timer == 0:
                self.is_jumping = False

        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self, surface):
        if self.is_jumping:
            pg.draw.circle(surface, (100, 100, 100), (int(self.x), int(self.y) + 20), self.radius, 2) # Ombra
            pg.draw.circle(surface, YELLOW, (int(self.x), int(self.y) - 10), self.radius + 5)
        else:
            pg.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

class Enemy:
    def __init__(self):
        self.radius = 15
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = -50 # Nasce fuori dallo schermo in alto
        self.base_speed = random.uniform(3.0, 6.0)

    def update(self, speed_multiplier):
        self.y += self.base_speed * speed_multiplier

    def draw(self, surface):
        pg.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)

class Projectile:
    def __init__(self, x, y):
        self.radius = 5
        self.x = x
        self.y = y
        self.speed = 10

    def update(self):
        self.y -= self.speed

    def draw(self, surface):
        pg.draw.circle(surface, GREEN, (int(self.x), int(self.y)), self.radius)

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Test Fase 3: Meccaniche di Gioco")
    clock = pg.time.Clock()

    player = Player()
    enemies = []
    projectiles = []
    
    score = 0
    simulated_voice_volume = 0.5 # Mezza velocità
    
    running = True
    while running:
        is_jumping = False
        is_attacking = False
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    is_jumping = True

        # Simulazione audio e video
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            simulated_voice_volume = min(1.0, simulated_voice_volume + 0.02)
        if keys[pg.K_s]:
            simulated_voice_volume = max(0.0, simulated_voice_volume - 0.02)
            
        mouse_buttons = pg.mouse.get_pressed()
        if mouse_buttons[0]: # Clic sinistro
            is_attacking = True

        mouse_x, mouse_y = pg.mouse.get_pos()
        player.update(mouse_x, mouse_y, is_jumping)
        
        # Sparo con cooldown
        if is_attacking and player.shoot_cooldown == 0:
            projectiles.append(Projectile(player.x, player.y))
            player.shoot_cooldown = FPS / 6

        # Generazione nemici
        spawn_chance = 0.02 + (0.05 * simulated_voice_volume)
        if random.random() < spawn_chance and simulated_voice_volume > 0.1:
            enemies.append(Enemy())

        # Aggiorna proiettili
        for p in projectiles[:]:
            p.update()
            if p.y < -10:
                projectiles.remove(p)

        # Aggiorna nemici
        for e in enemies[:]:
            e.update(simulated_voice_volume)
            if e.y > HEIGHT + 50:
                enemies.remove(e)
                score += 1
        
        score += simulated_voice_volume * 0.1

        # Collisioni proiettile
        for p in projectiles[:]:
            for e in enemies[:]:
                dist = math.hypot(p.x - e.x, p.y - e.y)
                if dist < p.radius + e.radius:
                    if p in projectiles: projectiles.remove(p)
                    if e in enemies: enemies.remove(e)
                    score += 5
                    break

        # Collisioni giocatore
        if not player.is_jumping:
            for e in enemies:
                dist = math.hypot(player.x - e.x, player.y - e.y)
                if dist < player.radius + e.radius - 5:
                    print(f"GAME OVER! Punteggio Finale: {int(score)}")
                    running = False

        # Render
        bg_color = (int(30 * simulated_voice_volume), int(30 * simulated_voice_volume), int(40 * simulated_voice_volume))
        screen.fill(bg_color)

        for p in projectiles: p.draw(screen)
        for e in enemies: e.draw(screen)
        player.draw(screen)

        font = pg.font.SysFont(None, 36)
        score_text = font.render(f"Punti: {int(score)}", True, WHITE)
        speed_text = font.render(f"Velocita' (Voce): {int(simulated_voice_volume * 100)}%", True, WHITE)
        
        screen.blit(score_text, (10, 10))
        screen.blit(speed_text, (10, 40))

        if player.is_jumping:
            jump_text = font.render("SALTO!", True, YELLOW)
            screen.blit(jump_text, (WIDTH // 2 - 40, 10))
        elif player.jump_cooldown > 0:
            cooldown = math.ceil(player.jump_cooldown / FPS)
            jump_text = font.render(f"Salto in ricarica: {cooldown}s", True, YELLOW)
            screen.blit(jump_text, (WIDTH // 2 - 120, 10))

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()

if __name__ == "__main__":
    main()