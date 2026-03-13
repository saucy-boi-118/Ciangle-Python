# imports
import pygame
import random
import math


# functions
def drawTriangle(position:pygame.Vector2, size:int, outline:bool, color:str):
    if (outline == False):
        pygame.draw.polygon(screen, color, [
        (position.x + size, position.y + size), 
        (position.x - size, position.y + size), 
        (position.x, position.y - size)])
    else:
        # actual shape
        pygame.draw.polygon(screen, color, [
        (position.x + size, position.y + size), 
        (position.x - size, position.y + size), 
        (position.x, position.y - size)])
        # outline
        pygame.draw.polygon(screen, "black", [
        (position.x + size, position.y + size), 
        (position.x - size, position.y + size), 
        (position.x, position.y - size)], width = 5)

def findDistance(pos1:pygame.Vector2, pos2:pygame.Vector2):
    return math.sqrt(math.pow((pos2.x - pos1.x), 2) + math.pow((pos2.y - pos1.y), 2))



# setup
pygame.init()
pygame.display.set_caption("CIANGLE", "cool")
pygame.display.set_icon(pygame.image.load("cat.jpg"))
screen = pygame.display.set_mode((1024,512))
clock = pygame.time.Clock()
running = True # for the "for" loop 
dt = 0 # delta times // frame rate independence

# game variables
player_pos = pygame.Vector2(100, screen.get_height() / 2)

# obstacle
obst1_pos = pygame.Vector2(1150, 375)
obst2_pos = pygame.Vector2(3500, 350)
obst_speed = 15
obst1_size = 25
obst2_size = 50


# gravity
gravity = 0.25
velocityY = 0
grounded = False

# movement
keys = pygame.key.get_pressed()

# text
font = pygame.font.Font(None, 100)
gText = font.render("Ciangle", True, "black")

font = pygame.font.Font(None, 50)
sText = font.render("Press 'S' to Start", True, "black")
font = pygame.font.Font(None, 100)
eText = font.render("Click 'S' to Play Again", True, "black")
font = pygame.font.Font(None, 125)
score = 0
scoreT = font.render(f"{score}", True, "#ADABA5")

# bool start
start = True

# logo
logo_pos = pygame.Vector2(screen.get_width()/2, 150)

# game loop
isDeath = True


# loop
while (running):
    # if you press x
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

    # fill the screen with desert color
    screen.fill("#FEEFCE")
    
    # game code here


    # before the start
    if (keys[pygame.K_s] and isDeath == True):
        isDeath = False
        start = False
        obst2_pos.x = 3500

    if (isDeath == True): # player lost

        # background stuff
        obst2_pos.x -= 10
        drawTriangle(obst2_pos, 50, True, "red")
        if (obst2_pos.x < -80):
            obst2_pos.x = screen.get_width() + 80

        # ground outline
        pygame.draw.rect(screen, "#AE6020", pygame.Rect(0, 400, 1024, 500))
        pygame.draw.line(screen, "black", pygame.Vector2(0, 400), pygame.Vector2(1024, 400), 5)

        # logo
        pygame.draw.circle(screen, "#4188B1", logo_pos, 100)
        pygame.draw.circle(screen, "black", logo_pos, 100, width = 5)
        # triangle
        drawTriangle(logo_pos, 65, True, "red")
        
        # game text
        screen.blit(gText, pygame.Vector2((logo_pos.x - gText.get_width()/2, logo_pos.y)))

        # start text
        if start == True:
            screen.blit(sText, pygame.Vector2((logo_pos.x - sText.get_width()/2, 250)))
        else:
            screen.blit(eText, pygame.Vector2((logo_pos.x - eText.get_width()/2, 275)))

    

    




    # after the start
    if (isDeath == False):
        # player controls / gravity
        velocityY += gravity * dt
        player_pos.y += velocityY 

        # clamp gravity
        if player_pos.y >= 375:
            player_pos.y = 375
            velocityY = 0
            grounded = True
        
        # player jumping
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and grounded == True:
            velocityY = -50
            grounded = False


        # draw the player
        pygame.draw.circle(screen, "#4188B1", player_pos, 25)
        pygame.draw.circle(screen, "black", player_pos, 25, width = 5)

        # ground / ground outline
        pygame.draw.rect(screen, "#AE6020", pygame.Rect(0, 400, 1024, 500))
        pygame.draw.line(screen, "black", pygame.Vector2(0, 400), pygame.Vector2(1024, 400), 5)

        # obstacles
        obst1_pos.x -= obst_speed # moving obstacle 1
        
        if obst1_pos.x < -20: # leaving screen obstacle 1
            obst1_pos.x = 2174
            obst_speed = random.randint(15, 20)
            obst1_size = random.randint(25, 65)
            obst1_pos.y = 400
            obst1_pos.y -= obst1_size
            score += 1 # update score
        
        obst2_pos.x -= obst_speed # moveing obstacle 2
        
        if obst2_pos.x < -20: # leaving screen obstacle 2
            obst2_pos.x = 3500
            obst_speed = random.randint(15, 20)
            # random size
            obst2_size = random.randint(25, 65)
            obst2_pos.y = 400
            obst2_pos.y -= obst2_size
            score += 1 # update score


        # make sure its possible
        if findDistance(obst1_pos, obst2_pos) < 350:
            obst2_pos.x += 250

        
        drawTriangle(obst1_pos, obst1_size, True, "red") # small one
        drawTriangle(obst2_pos, obst2_size, True, "red") # big spike (mostly)

        # score
        scoreT = font.render(f"{score}", True, "#ADABA5")
        screen.blit(scoreT, pygame.Vector2((screen.get_width()/2) - (scoreT.get_width()/2), 225))

        if (
        pygame.Rect.colliderect(pygame.Rect(obst1_pos.x + obst1_size, obst1_pos.y + obst1_size, obst1_pos.x - obst1_size, obst1_pos.y - obst1_size), # obstacle 1
        pygame.Rect(player_pos.x - 15, player_pos.y - 15, player_pos.x + 15, player_pos.y + 15)) # player
        or 
        pygame.Rect.colliderect(pygame.Rect(obst2_pos.x + obst2_size, obst2_pos.y + obst2_size, obst2_pos.x - obst2_size, obst2_pos.y - obst2_size), # obstacle 2
        pygame.Rect(player_pos.x - 15, player_pos.y - 15, player_pos.x + 15, player_pos.y + 15))): # player
            isDeath = True
            # reseting stuff
            obst2_size = 25
            obst2_pos.y = 400
            obst2_pos.y -= obst2_size
            obst1_pos.x = 1150
            obst2_pos.x = 3500
            score = 0



    # flip display to put it on screen
    pygame.display.flip()

    dt = clock.tick(60) # limit fps to 60

pygame.quit()