import pygame

pygame.init()

screen = pygame.display.set_mode((640, 640))

snek_img = pygame.image.load('snek.png').convert()
snek_img = pygame.transform.scale(snek_img, (snek_img.get_width() * 1.5, snek_img.get_height() * 1.5))
#ignores (specified by values) color
snek_img.set_colorkey((255,255,255))

sneks = pygame.Surface((64,64), pygame.SRCALPHA)
sneks.blit(snek_img,(0,0))
sneks.blit(snek_img,(20,0))
sneks.blit(snek_img, (10,10))

running = True
x=0
clock = pygame.time.Clock()

delta_time = 0.1
#for text
font = pygame.font.Font(None,size=30)

while running:
    #makes background white
    #screen.fill((255,255,255))
    #put snake on screen at coordinates x=x, y=0
    screen.blit(snek_img, (x, 10))
    x += 50 * delta_time

    hitbox = pygame.Rect(x,10,snek_img.get_width(),snek_img.get_height())

    target = pygame.Rect(300, 0, 160, 280)
    collision = hitbox.colliderect(target)
    pygame.draw.rect(screen,(255*collision,255,0),target)

    text = font.render('Hell Snek!', True, (255,255,255))
    screen.blit(text, (200,600))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    delta_time = clock.tick(60)/1000
    #the lower bound limit is only necessary if tick() is called with no arguments for an uncapped framerate.
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()