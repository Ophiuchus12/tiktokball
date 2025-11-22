"""
Visual style and appearance management for the game.
Handles UI rendering, scores, and timers.
"""
import pygame
from config.constants import (
    FONT_PATH, DEFAULT_FONT_SIZE, TEXT_Y_POSITION, 
    SCORE_SPACING, SCORE_Y_OFFSET, TIMER_Y_OFFSET
)

pygame.font.init()
font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE)


class GameTimer:
    """Manages game timer with start/stop functionality."""
    
    def __init__(self):
        self.start_time = None
        self.paused = False
        self.pause_time = 0
    
    def start(self):
        """Start or resume the timer."""
        if self.start_time is None:
            self.start_time = pygame.time.get_ticks()
        self.paused = False
    
    def pause(self):
        """Pause the timer."""
        if not self.paused:
            self.pause_time = pygame.time.get_ticks()
            self.paused = True
    
    def reset(self):
        """Reset the timer."""
        self.start_time = pygame.time.get_ticks()
        self.paused = False
        self.pause_time = 0
    
    def get_elapsed(self):
        """Get elapsed time in seconds."""
        if self.start_time is None:
            return 0
        
        if self.paused:
            return (self.pause_time - self.start_time) / 1000
        
        return (pygame.time.get_ticks() - self.start_time) / 1000


# Global timer instance
game_timer = GameTimer()


def get_timer():
    """Get the global timer instance."""
    return game_timer


def chooseMode(screen, mode, countdown_duration, spacing=300, y_position=TEXT_Y_POSITION, 
               balles=[], visu=None, logo1=None, logo2=None, logo3=None, logo4=None, 
               logo_size=(120, 100)):
    """
    Render game mode UI including scores, timers, and logos.
    
    Args:
        screen: Pygame screen surface
        mode: Game mode string
        countdown_duration: Duration of countdown in seconds
        spacing: Spacing between UI elements
        y_position: Y position for main text
        balles: List of ball objects
        visu: Visualization mode
        logo1-4: Logo images for teams
        logo_size: Size tuple for logos
    """
    # Initialize timer if not started
    timer = get_timer()
    if timer.start_time is None:
        timer.start()
    
    if mode not in ["infini", "simpleCercleferme", "quadruple"]:
        # # Main title text
        # text = "Cool tiktok ball game​\n​ "
        # lines = text.split('\n')
        
        # max_width = 0
        # total_height = 0
        # rendered_lines = []

        # for line in lines:
        #     rendered = font.render(line, True, (0, 0, 0))
        #     rendered_lines.append(rendered)
        #     rect = rendered.get_rect()
        #     max_width = max(max_width, rect.width)
        #     total_height += rect.height

        # # Background rectangle
        # padding = 10
        # bg_rect = pygame.Rect(
        #     (screen.get_width() - max_width) // 2 - padding // 2,
        #     y_position - 200 - padding // 2,
        #     max_width + padding,
        #     total_height + padding
        # )

        # pygame.draw.rect(screen, (255, 0, 0), bg_rect, border_radius=15)

        # # Render lines
        # for i, rendered in enumerate(rendered_lines):
        #     rect = rendered.get_rect(
        #         center=(screen.get_width() // 2, 
        #                y_position - 150 + i * font.get_height())
        #     )
        #     screen.blit(rendered, rect)

        # Bottom text
        textBelow = "Like and subscribe ​​\n I follow back 💪​"
        linesBelow = textBelow.split('\n')
        for i, line in enumerate(linesBelow):
            rendered = font.render(line, True, (255, 255, 255))
            rect = rendered.get_rect(
                center=(screen.get_width() // 2, 
                       y_position + 1400 + i * font.get_height())
            )
            screen.blit(rendered, rect)
   
    # Mode-specific rendering
    if mode == "double":
        _render_double_mode(screen, balles, spacing, y_position, 
                           countdown_duration, logo1, logo2, logo_size)
    
    elif mode == "quadruple":
        _render_quadruple_mode(screen, balles, spacing, y_position, 
                              countdown_duration, logo1, logo2, logo3, logo4, logo_size)
    
    elif mode == "multi":
        _render_timer_only(screen, countdown_duration, y_position, (237, 187, 153))
    
    elif mode == "simple":
        if visu != "clean":
            _render_simple_mode(screen, balles, countdown_duration, y_position)
    
    elif mode == "simpleCercleferme":
        _render_timer_only(screen, countdown_duration, y_position, (174, 180, 159))


def _render_double_mode(screen, balles, spacing, y_position, countdown_duration, 
                        logo1, logo2, logo_size):
    """Render double mode with two teams."""
    total_width = (len(balles) - 1) * spacing
    start_x = ((screen.get_width() - total_width) // 2)
    score_y_position = y_position + SCORE_Y_OFFSET

    for idx, balle in enumerate(balles):
        if balle.cage != 0:
            score_text = font.render(f"Score: {balle.score}", True, balle.color)
            text_rect = score_text.get_rect()
            text_rect.topleft = (start_x + idx * spacing, score_y_position)
            screen.blit(score_text, text_rect)

    # Position logos
    if logo1 and logo2:
        logo_y = score_y_position
        ball1, ball2 = balles[0], balles[1]
        
        ball1_index = balles.index(ball1)
        ball2_index = balles.index(ball2)

        logo1_x = start_x + ball1_index * spacing - logo_size[0] - 10
        logo2_x = start_x + ball2_index * spacing + 250

        screen.blit(logo1, (logo1_x, logo_y))
        screen.blit(logo2, (logo2_x, logo_y))

    _render_countdown(screen, countdown_duration, y_position + TIMER_Y_OFFSET, (255, 255, 255))


def _render_quadruple_mode(screen, balles, spacing, y_position, countdown_duration, 
                           logo1, logo2, logo3, logo4, logo_size):
    """Render quadruple mode with four teams."""
    cols = 2
    rows = 2
    spacing_x = 300
    spacing_y = 100
    start_x = (screen.get_width() - (cols - 1) * spacing_x) // 2
    score_y_position = y_position + SCORE_Y_OFFSET

    logos = [logo1, logo2, logo3, logo4]
    offset_x = -80

    for display_idx, balle_idx in enumerate(range(1, 5)):
        balle = balles[balle_idx]
        logo = logos[display_idx]

        if balle.cage != 0:
            col = display_idx % cols
            row = display_idx // cols
            x = start_x + col * spacing_x + offset_x
            y = score_y_position + row * spacing_y

            score_text = font.render(f"Score: {balle.score}", True, balle.color)
            text_rect = score_text.get_rect()

            if col == 0:
                # Logo on left
                logo_x = x - logo_size[0] - 10
                text_rect.topleft = (x, y)
                screen.blit(score_text, text_rect)
                if logo:
                    screen.blit(logo, (logo_x, y))
            else:
                # Logo on right
                text_rect.topleft = (x, y)
                screen.blit(score_text, text_rect)
                logo_x = x + text_rect.width + 10
                if logo:
                    screen.blit(logo, (logo_x, y))

    text = "Formula 1 Grand Prix of Canada​​​ \n\n Tell me your prediction in the comments"
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        rendered = font.render(line, True, (34, 201, 168))
        rect = rendered.get_rect(
            center=(screen.get_width() // 2, 
                   y_position - 200 + i * font.get_height())
        )
        screen.blit(rendered, rect)

    _render_countdown(screen, countdown_duration, y_position + TIMER_Y_OFFSET, (255, 255, 255))


def _render_simple_mode(screen, balles, countdown_duration, y_position):
    """Render simple mode with score and timer."""
    nbBalles = 1
    balle = balles[0] if balles else None
    
    if balle:
        score_text = font.render(f"Score: {nbBalles}", True, (214, 234, 248))
        text_rect = score_text.get_rect(center=(screen.get_width() // 2, y_position))
        screen.blit(score_text, text_rect)

    _render_countdown(screen, countdown_duration, y_position + 50, (174, 180, 159))


def _render_timer_only(screen, countdown_duration, y_position, color):
    """Render just the countdown timer."""
    _render_countdown(screen, countdown_duration, y_position, color)


def _render_countdown(screen, countdown_duration, y_position, color):
    """Render countdown timer."""
    timer = get_timer()
    elapsed = timer.get_elapsed()
    remaining = max(0, countdown_duration - int(elapsed))
    
    minutes = remaining // 60
    seconds = remaining % 60
    timer_text_str = f"Timer: {minutes:02d}:{seconds:02d}"
    
    timer_text = font.render(timer_text_str, True, color)
    timer_rect = timer_text.get_rect(center=(screen.get_width() // 2, y_position))
    screen.blit(timer_text, timer_rect)