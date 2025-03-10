import pygame
import sys
import math
import random
import os

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Raid the Castle")
        # Game state
        self.cookies = 0
        self.cookie_per_click = 1
        self.cookies_per_second = 0
        # UI elements
        self.cookie = pygame.Rect(110, 120, 300, 300)
        self.cookie_color = "brown"
        self.upgradeBtn = pygame.Rect(10, 50, 120, 70)
        self.autoBtn = pygame.Rect(10, 140, 120, 70)
        # Separate costs for each upgrade type
        self.click_upgrade_cost = 5
        self.auto_upgrade_cost = 5
        # Font setup
        self.game_font = pygame.font.Font(None, 15)
        # State tracking
        self.last_update_time = pygame.time.get_ticks()
        self.last_click_time = pygame.time.get_ticks()
        # Shake animation variables
        self.shake_intensity = 0
        self.shake_duration = 0
        self.original_cookie_pos = [110, 120]  # Store original position
        # Load castle image
        self.castle_image = pygame.image.load(os.path.join('assets', 'castle.png')).convert_alpha()
        self.castle_image = pygame.transform.scale(self.castle_image, (300, 300))
        self.castle_rect = self.castle_image.get_rect()
        self.castle_rect.topleft = (110, 120)
        # Track highest achieved rank
        self.highest_rank = "Orc Weakling"

    def get_rank(self):
        """Return rank based on current coin count, never downgrading from highest achieved rank"""
        current_rank = "Orc Weakling"
        if self.cookies >= 1000:
            current_rank = "Orc King"
        elif self.cookies >= 700:
            current_rank = "Orc Warlord"
        elif self.cookies >= 500:
            current_rank = "Orc Champion"
        elif self.cookies >= 200:
            current_rank = "Orc Nob"
        
        # Update highest rank if current rank is higher
        if self.rank_order(current_rank) > self.rank_order(self.highest_rank):
            self.highest_rank = current_rank
        
        return self.highest_rank

    def rank_order(self, rank):
        """Helper method to determine rank order for comparison"""
        order = {
            "Orc Weakling": 0,
            "Orc Nob": 1,
            "Orc Champion": 2,
            "Orc Warlord": 3,
            "Orc King": 4
        }
        return order.get(rank, 0)

    def handle_events(self):
        """Process all events including mouse clicks"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos, event.button)
        return True

    def handle_mouse_click(self, pos, button):
        """Handle mouse click events"""
        if button == 1:  # Left mouse button
            if self.castle_rect.collidepoint(pos):
                current_time = pygame.time.get_ticks()
                if current_time - self.last_click_time > 200:  # Debounce clicks
                    self.cookies += self.cookie_per_click
                    self.last_click_time = current_time
                    # Start shake animation
                    self.shake_intensity = 5 # Adjust this value to change shake intensity
                    self.shake_duration = 10 # Number of frames to shake
            elif self.upgradeBtn.collidepoint(pos):
                if self.cookies >= self.click_upgrade_cost:
                    self.cookies -= self.click_upgrade_cost
                    self.click_upgrade_cost *= 2
                    self.cookie_per_click += 5
            elif self.autoBtn.collidepoint(pos):
                if self.cookies >= self.auto_upgrade_cost:
                    self.cookies -= self.auto_upgrade_cost
                    self.auto_upgrade_cost *= 2
                    self.cookies_per_second += 5

    def update_shake(self):
        """Update shake animation"""
        if self.shake_duration > 0:
            # Generate random offset within shake_intensity range
            x_offset = random.uniform(-self.shake_intensity, self.shake_intensity)
            y_offset = random.uniform(-self.shake_intensity, self.shake_intensity)
            # Update castle position temporarily
            self.castle_rect.x = self.original_cookie_pos[0] + x_offset
            self.castle_rect.y = self.original_cookie_pos[1] + y_offset
            # Decrease duration until shake ends
            self.shake_duration -= 1
        else:
            # Reset castle position when shake ends
            self.castle_rect.x = self.original_cookie_pos[0]
            self.castle_rect.y = self.original_cookie_pos[1]

    def update_cookies(self):
        """Update cookies based on time passed"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= 1000:  # Update every second
            self.cookies += self.cookies_per_second
            self.last_update_time = current_time

    def draw_score(self):
        """Draw the current cookie count"""
        self.display_cookies = self.game_font.render(f"Coins: {str(int(self.cookies))}", True, "black")
        self.screen.blit(self.display_cookies, (0, 450))
        # Show auto-cookie generation rate
        if self.cookies_per_second > 0:
            self.auto_text = self.game_font.render(f"+{self.cookies_per_second}/sec", True, "black")
            self.screen.blit(self.auto_text, (0, 470))

    def draw_upgrades(self):
        """Draw both upgrade buttons and information"""
        # Click upgrade button
        pygame.draw.rect(self.screen, "grey", self.upgradeBtn, border_radius=15)
        self.upgrade1_description = self.game_font.render( f"Upgrade Weapon\n+{self.cookie_per_click} coin per click", True, "black")
        self.screen.blit(self.upgrade1_description, (15, 55))
        self.click_cost_text = self.game_font.render(f"Cost:{str(self.click_upgrade_cost)}", True, "black")
        self.screen.blit(self.click_cost_text, (15, 85))
        # Auto-click upgrade button
        pygame.draw.rect(self.screen, "grey", self.autoBtn, border_radius=15)
        self.auto_description = self.game_font.render(f"Hire Orc\n +1 coin/sec", True, "black")
        self.screen.blit(self.auto_description, (15, 145))
        self.auto_cost_text = self.game_font.render(f"Cost:{str(self.auto_upgrade_cost)}", True, "black")
        self.screen.blit(self.auto_cost_text, (15, 175))

    def draw_rank(self):
        """Draw the player's current rank at the bottom of the screen"""
        # Create rank text surface
        rank_text = self.game_font.render(f"Rank: {self.get_rank()}", True, "black")
        # Position slightly above the score text
        self.screen.blit(rank_text, (0, 430))

    def render(self):
        """Render all game elements"""
        # Update shake animation
        self.update_shake()
        # Draw castle
        self.screen.blit(self.castle_image, self.castle_rect)
        self.update_cookies()
        self.draw_score()
        self.draw_upgrades()
        self.draw_rank()

    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True
        while running:
            self.screen.fill('dark grey')
            running = self.handle_events()
            self.render()
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()