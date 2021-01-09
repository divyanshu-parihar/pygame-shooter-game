import pygame
import os
pygame.init()
pygame.font.init()
pygame.mixer.init()


WIDTH,HEIGHT = 900,500
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
FPS = 60

YELLOW_HIT  = pygame.USEREVENT + 1
RED_HIT  = pygame.USEREVENT + 2 

# font
HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

# sound
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))

MAX_BULLETS = 3 
BULLET_VEL = 8
SPACESHIP_WIDHT = 55
SPACESHIP_HEIGHT = 40
VEL = 5
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Shooter Game!')

YELLOW_FIRESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_FIRESHIP_IMAGE,(SPACESHIP_WIDHT,SPACESHIP_HEIGHT)),-90)
SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))

RED_FIRESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_FIRESHIP_IMAGE,(SPACESHIP_WIDHT,SPACESHIP_HEIGHT)),90)


def make_center_line():
	rect = pygame.Rect(WIDTH//2-5,0,10,HEIGHT)
	pygame.draw.rect(WIN,BLACK,rect)


def draw_winner(winner):
	winner_text=WINNER_FONT.render(winner,1,WHITE)
	WIN.blit(winner_text,(WIDTH/2 - winner_text.get_width()/2,HEIGHT/2 - winner_text.get_height()/2))
	pygame.display.update()
	pygame.time.delay(5000)

def yellow_handle_movement(keys,yellow):
	if(keys[pygame.K_UP]) and yellow.x>WIDTH/2+5:
		yellow.x -=VEL
	elif keys[pygame.K_DOWN] and yellow.x < WIDTH - SPACESHIP_HEIGHT:
		yellow.x +=VEL
	elif keys[pygame.K_LEFT] and yellow.y<HEIGHT-SPACESHIP_WIDHT:
		yellow.y +=VEL
	elif keys[pygame.K_RIGHT] and yellow.y >0:
		yellow.y -=VEL

def red_handle_movement(keys,red):
	if(keys[pygame.K_w]) and red.x<((WIDTH/2) - SPACESHIP_HEIGHT-5):
		red.x +=VEL
	elif keys[pygame.K_s] and red.x>0:
		red.x -=VEL
	elif keys[pygame.K_a] and red.y>0:
		red.y -=VEL
	elif keys[pygame.K_d] and red.y< HEIGHT - SPACESHIP_WIDHT:
		red.y +=VEL


def update_display(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
	WIN.blit(SPACE_BACKGROUND,(0,0))
	make_center_line()
	red_health_text = HEALTH_FONT.render('HEALTH : '+str(red_health),1,WHITE)
	yellow_health_text = HEALTH_FONT.render('HEALTH : '+str(yellow_health),1,WHITE)

	WIN.blit(red_health_text,(10,10))
	WIN.blit(yellow_health_text,(WIDTH-yellow_health_text.get_width()-10,10))

	WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
	WIN.blit(RED_SPACESHIP,(red.x,red.y))

	for bullet in red_bullets:
		pygame.draw.rect(WIN,RED,bullet)
	for bullet in yellow_bullets:
		pygame.draw.rect(WIN,YELLOW,bullet)

	pygame.display.update()

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
	for bullet in red_bullets:
		bullet.x += BULLET_VEL
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(YELLOW_HIT))
			red_bullets.remove(bullet)
		if bullet.x>WIDTH:
			yellow_bullets.remove(bullet)

	for bullet in yellow_bullets:
		bullet.x -= BULLET_VEL
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT))
			yellow_bullets.remove(bullet)
		if bullet.x>WIDTH:
			yellow_bullets.remove(bullet)


def main():
	red  = pygame.Rect(100,200,SPACESHIP_WIDHT,SPACESHIP_HEIGHT)
	yellow = pygame.Rect(700,200,SPACESHIP_WIDHT,SPACESHIP_HEIGHT)
	clock = pygame.time.Clock()
	run = True
	red_health = 10
	yellow_health = 10
	red_bullets = []
	yellow_bullets = []
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LCTRL and len(red_bullets)<MAX_BULLETS:
					bullet = pygame.Rect(red.x+red.width,red.y+red.height//2,10,5)
					red_bullets.append(bullet)
					BULLET_FIRE_SOUND.play()
				if event.key == pygame.K_RCTRL and len(yellow_bullets)<MAX_BULLETS:
					bullet = pygame.Rect(yellow.x,yellow.y+yellow.height//2,10,5)
					yellow_bullets.append(bullet)
					BULLET_FIRE_SOUND.play()
			if event.type == RED_HIT:
				red_health -= 1
				BULLET_HIT_SOUND.play()
			if event.type == YELLOW_HIT:
				yellow_health -= 1
				BULLET_HIT_SOUND.play()

		winner_text = ''
		if(red_health<=0):
			winner_text = 'YELLOW WON! '
		if(yellow_health<=0):
			winner_text = 'RED WON!'
		if(winner_text!=''):
			draw_winner(winner_text)
			break

		handle_bullets(yellow_bullets,red_bullets,yellow,red)
		keys = pygame.key.get_pressed()
		red_handle_movement(keys,red)
		yellow_handle_movement(keys,yellow)
		update_display(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)

	main()

if __name__ == '__main__':
	main()