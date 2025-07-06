import time
import pygame

pygame.font.init()
font = pygame.font.Font("font/symbola/Symbola.ttf", 60)

countdown_start = time.time()

## param
##screen 
##mode String
##balles []
##countdown_duration int 


def chooseMode(screen, mode, countdown_duration, spacing=300, y_position=300, balles=[], visu = None,  logo1=None, logo2=None, logo3= None, logo4= None, logo_size = (120, 100 )):
   
    if mode != "infini" and mode != "simpleCercleferme" and mode !="quadruple":

        # if capture_image:# Positionner la capture horizontale centrée en X, et juste au-dessus du cercle
        #     circle_image_x = screen.get_width() // 2 - (capture_image.get_width()/2)
        #     circle_image_y =  y_position + 10  # à ajuster selon ton cercle


        #     screen.blit(capture_image, (circle_image_x, circle_image_y))

        text = "Full pink​ edit​\n​ "
        lines = text.split('\n')
        

        max_width = 0
        total_height = 0
        rendered_lines = []

        for i, line in enumerate(lines):
            rendered = font.render(line, True, (255, 255, 255))
            rendered_lines.append(rendered)
            rect = rendered.get_rect()
            max_width = max(max_width, rect.width)
            total_height += rect.height

        # Coordonnées du fond
        padding = 10
        bg_rect = pygame.Rect(
            (screen.get_width() - max_width) // 2 - padding // 2,
            y_position - 200 - padding // 2,
            max_width + padding,
            total_height + padding
        )

        # Dessine le fond blanc
        pygame.draw.rect(screen, (255, 113, 255), bg_rect, border_radius=15)

        # Affiche les lignes par-dessus
        for i, rendered in enumerate(rendered_lines):
            rect = rendered.get_rect(center=(screen.get_width() // 2, y_position - 150 + i * font.get_height()))
            screen.blit(rendered, rect)

        textBelow = "Like and subscribe ​​\n I follow back 💪​"
        linesBelow = textBelow.split('\n')
        for i, line in enumerate(linesBelow):
            rendered = font.render(line, True, ( 255, 255, 255 ))
            rect = rendered.get_rect(center=(screen.get_width() // 2, y_position + 1400 + i * font.get_height()))
            screen.blit(rendered, rect)
   
    match mode :
        case "double":
            total_width = (len(balles)-1) * spacing
            start_x = ((screen.get_width() - total_width) // 2) 

            score_y_position = y_position + 1250  

            for idx, balle in enumerate(balles):
                if balle.cage != 0:
                    score_text = font.render(f"Score: {balle.score}", True, balle.color)
                    text_rect = score_text.get_rect()
                    text_rect.topleft = (start_x + idx * spacing, score_y_position)
                    screen.blit(score_text, text_rect)

            # Positionnement des images
            if logo1 and logo2:
                logo_y = score_y_position  # même ligne que les scores

                ball1 = balles[0]
                ball2 = balles[1]

                # Trouve les indexes de ball1 et ball2
                ball1_index = balles.index(ball1)
                ball2_index = balles.index(ball2)

                logo1_x = start_x + ball1_index * spacing - logo_size[0] - 10
                logo2_x = start_x + ball2_index * spacing + 250  # décalage à droite du score

                screen.blit(logo1, (logo1_x, logo_y))
                screen.blit(logo2, (logo2_x, logo_y))

            elapsed = time.time() - countdown_start
            remaining = max(0, countdown_duration - int(elapsed))  # jamais négatif
            minutes = remaining // 60
            seconds = remaining % 60
            timer_text_str = f"Timer: {minutes:02d}:{seconds:02d}"
            timer_text = font.render(timer_text_str, True, (  255, 255, 255 ))
            timer_rect = timer_text.get_rect(center=(screen.get_width() // 2, y_position+30))
            screen.blit(timer_text, timer_rect)

        case "quadruple":
            cols = 2
            rows = 2
            spacing_x = 300  # Espace horizontal entre colonnes
            spacing_y = 100  # Espace vertical entre lignes
            start_x = (screen.get_width() - (cols - 1) * spacing_x) // 2
            score_y_position = y_position + 1250

            # Logos associés à balles[1] à balles[4]
            logos = [logo1, logo2, logo3, logo4]

            offset_x = -80

            for display_idx, balle_idx in enumerate(range(1, 5)):  # de balle[1] à balle[4]
                balle = balles[balle_idx]
                logo = logos[display_idx]

                if balle.cage != 0:
                    col = display_idx % cols
                    row = display_idx // cols
                    x = start_x + col * spacing_x + offset_x
                    y = score_y_position + row * spacing_y

                    # Créer le texte du score
                    score_text = font.render(f"Score: {balle.score}", True, balle.color)
                    text_rect = score_text.get_rect()

                    if col == 0:
                        # Logo à gauche
                        logo_x = x - logo_size[0] - 10
                        text_rect.topleft = (x, y)
                        screen.blit(score_text, text_rect)
                        if logo:
                            screen.blit(logo, (logo_x, y))
                    else:
                        # Logo à droite
                        text_rect.topleft = (x, y)
                        screen.blit(score_text, text_rect)
                        logo_x = x + text_rect.width + 10
                        if logo:
                            screen.blit(logo, (logo_x, y))



            text = "Formula 1 Grand Prix of Canada​​​ \n\n Tell me your prediction in the comments"
            lines = text.split('\n')
            

            for i, line in enumerate(lines):
                rendered = font.render(line, True, ( 34, 201, 168 ))
                rect = rendered.get_rect(center=(screen.get_width() // 2, y_position - 200 + i * font.get_height()))
                screen.blit(rendered, rect)

            elapsed = time.time() - countdown_start
            remaining = max(0, countdown_duration - int(elapsed))  # jamais négatif
            minutes = remaining // 60
            seconds = remaining % 60
            timer_text_str = f"Timer: {minutes:02d}:{seconds:02d}"
            timer_text = font.render(timer_text_str, True, (  255, 255, 255 ))
            timer_rect = timer_text.get_rect(center=(screen.get_width() // 2, y_position+30))
            screen.blit(timer_text, timer_rect)

        case "multi" : 
            elapsed = time.time() - countdown_start
            remaining = max(0, countdown_duration - int(elapsed))  # jamais négatif
            minutes = remaining // 60
            seconds = remaining % 60
            timer_text_str = f"Timer: {minutes:02d}:{seconds:02d}"

            timer_text = font.render(timer_text_str, True, (  237, 187, 153 ))
            timer_rect = timer_text.get_rect(center=(screen.get_width() // 2, y_position))
            screen.blit(timer_text, timer_rect)

        case "simple" :
            nbBalles = 1
            if visu != "clean":
                balle = balles[0]
                score_text = font.render(f"Score: {nbBalles}", True, ( 214, 234, 248  ))
                text_rect = score_text.get_rect(center=(screen.get_width() // 2, y_position))
                screen.blit(score_text, text_rect)

                elapsed = time.time() - countdown_start
                remaining = max(0, countdown_duration - int(elapsed))  # jamais négatif
                minutes = remaining // 60
                seconds = remaining % 60
                timer_text_str = f"Timer: {minutes:02d}:{seconds:02d}"

                timer_text = font.render(timer_text_str, True, (  174, 180, 159 ))
                timer_rect = timer_text.get_rect(center=(screen.get_width() // 2, y_position+50))
                screen.blit(timer_text, timer_rect)

        case "infini" :
            shadow = font.render(f"{current_start_index}", True, (255,255,255))
            shadow_rect = shadow.get_rect(center=(screen.get_width() // 2 + 2, screen.get_height() // 2 + 2))
            screen.blit(shadow, shadow_rect)
            passed_text = font.render(f"{current_start_index}", True, (255, 151, 0))
            passed_rect = passed_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(passed_text, passed_rect)          

        case "simpleCercleferme":
            elapsed = time.time() - countdown_start
            remaining = max(0, countdown_duration - int(elapsed))  # jamais négatif
            minutes = remaining // 60
            seconds = remaining % 60
            timer_text_str = f"Timer: {minutes:02d}:{seconds:02d}"
            timer_text = font.render(timer_text_str, True, (  174, 180, 159 ))
            timer_rect = timer_text.get_rect(center=(screen.get_width() // 2, y_position+50))
            screen.blit(timer_text, timer_rect)