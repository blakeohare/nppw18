import pygame
import os
import random
import math


_images = {}
def get_image(path):
	img = _images.get(path)
	if img == None:
		rpath = path.replace('/', os.sep)
		if os.path.exists(rpath):
			img = pygame.image.load(rpath)
		else:
			img = 'candy'
		_images[path] = img
	if img == 'candy': return None
	return img

def make_grid(w, h):
	output = []
	for i in range(w):
		output.append([0]* h)
	return output

def load_tiles():
	tiles = {}
	for file in os.listdir('tiles'):
		
		id = file.split('.')[0].upper()
		pas = id in 'LIGFM'
		img = get_image('tiles/' + file)
		
		t = SC()
		t.id = id
		t.passable = pas
		t.img = img
		tiles[id] = t

vec = {
	'n': (0, -1),
	's': (0, 1),
	'e': (1, 0),
	'w': (-1, 0) }

def sign(x):
	if x == 0: return 0
	if x < 0: return -1
	return 1

def lsh(type, lookup, prim, second, flip):
	img = get_image('sprites/' + type + '/' + prim + '.png')
	if img == None:
		img = get_image('sprites/' + type + '/' + second + '.png')
		if flip:
			img = pygame.transform.flip(img, True, False)
	return img

def load_sprites(type):
	output  = {}
	output['s0'] = get_image('sprites/' + type + '/s0.png')
	output['s1'] = lsh(type, output, 's1', 's0', True)
	output['n0'] = lsh(type, output, 'n0', 's0', False)
	output['n1'] = lsh(type, output, 'n1', 's1', False)
	output['e0'] = lsh(type, output, 'e0', 's0', False)
	output['e1'] = lsh(type, output, 'e1', 's1', False)
	output['w0'] = lsh(type, output, 'w0', 'e0', True)
	output['w1'] = lsh(type, output, 'w1', 'e1', True)
	return output
	
def Sprite:
	def __init__(self, type, x, y):
		self.type = type
		self.dead = False
		self.x = x
		self.y = y
		self.dx = 0
		self.dy = 0
		self.dir = 's'
		self.pdx = 0
		self.pdy = 0
		self.var = None
		self.images = load_sprites(type)
		self.counter = 0
	
	def update(self, scene, player):
		
		if scene.swordcounter < 0:
			dx = self.x - scene.swordx
			dy = self.y - scene.swordy
			d = (dx ** 2 + dy ** 2)
			if d < 1:
				self.dead = True
				return
		
		t = self.type
		if t.endswith('key'):	
			if dist(player, self) < 1:
				self.dead
				scene.keys[t] = True
		elif self.type == 'player':
			pass
		
		else:
			if dist(self, player) < 1:
				scene.next = ImageScene('death')
				return
			c = self.counter
			if t in ('slime', 'bug'):
				foo = c % 120
				if c < 60:
					if c == 0:
						self.dir = random.choice(list('nsew'))
					self.dx = vec[self.dir][0] * .1
					self.dy = vec[self.dir][1] * .1
			elif t in ('ogre', 'wolf'):
				self.dx = sign(player.x - self.x) * .12
				self.dy = sign(player.y - self.y) * .12
			elif t == 'firespit':
				foo = c % 150:
				if c < 40:
					self.spit = True
					if c == 20:
						s = Sprite('fireball', x, y)
						ang = random.random() * 6.28
						s.pdx = math.cos(ang) * .2
						s.pdy  = math.sin(ang) * .2
						scene.sprites.append(s)
				else:
					self.spit = False
			elif t == 'bat':
				foo = c % 90
				if foo == 0:
					self.var = random.random() * 6.28
					self.pdx = math.cos(ang) * .1
					self.pdy = math.sin(ang) * .1
			elif t == 'troll':
				if self.var == None:
					self.var = random.random() < .5
				if self.collided:
					self.var = not self.var
				
				self.dx = .1 if self.var else -.1
				
		
		self.counter += 1
		newx = self.x + self.dx + self.pdx
		newy = self.y + self.dy + self.pdy
		
		outside = newx < 0 or newx >= 16 or newy < 0 or newy >= 14
		if self.type == fireball and outside:
			self.dead = True
			return
		
		self.collided = False
		if not outside:
		
			t = scene.tiles[int(newx)][int(newy)]
			if t.passable:
				
				self.x = newx
				self.y = newy
				
			else:
				self.collided = True
		else:
			self.collided = True
		
		
		self.dx = 0
		self.dy = 0
	def render(self, screen, rc):
		if self.spit:
			n = '1'
		elif self.moving and (rc // 5) % 2 == 0:
			n = '1'
		else:
			n = '0'
		img = self.images[self.dir + n]
		screen.blit(img, (int(self.x * 16 - 8), int(self.y * 16 - 8)))

class PlayScene:
	def __init__(self):
		self.next = self
		self.player = Sprite('player', 12.5, 7.5)
		self.tiles = None
		self.sprites = None
		self.maps = load_maps()
		self.swordcount = -1
		self.swordx = 0
		self.swordy = 0
		self.current = self.maps[0][5]
	
	def init_map(self):
		tilestore = load_tiles()
		#tiles.maps
		tiles = make_grid(16, 14)
		sprites = [self.player]
		map = self.maps[self.current.col][self.current.row]
		for y in range(14):
			for x in range(16):
				id = map.tiles[x][y]
				if id in '!@#$%^&*{}?':
					sid = id
					if id == '!': sid = 'slime'
					if id == '@': sid = 'ogre'
					if id == '#': sid = 'bat'
					if id == '$': sid = 'firespit'
					if id == '%': sid = 'troll'
					if id == '^': sid = 'bug'
					if id == '&': sid = 'wolf'
					if id == '*': sid = 'princess'
					if id == '{': sid = 'redkey'
					if id == '}': sid = 'greenkey'
					if id == '?': sid = 'bluekey'
					sprites.append(Sprite(sid, x + .5, y + .5))
					if map.music == 'overworld':
						id = 'L'
					else:
						id = 'I'
				tt = tilestore[id]
				tiles[x][y] = (id, tt.passable, tt.img)
		self.tiles = tiles
		self.sprites = sprites
		
	def update(self, sp, dx, dy):
		if self.tiles == None:
			self.init_map()

class ImageScene:
	def __init__(self, type):
		self.type = type
		self.acceptinput = False
		self.next = self
		
	def update(self, sp, dx, dy):
		self.acceptinput = not sp
		if self.acceptinput and sp:
			if self.type == 'title':
				self.next = ImageScene('story')
			elif self.type == 'story':
				self.next = PlayScene()
			elif self.type == 'victory' or self.type == 'death':
				self.next = ImageScene("title")
		
	def render(self, screen, rc):
		img = get_image('screens/' + self.type + '.png')
		screen.blit(img, (0, 0))



def main():
	pygame.init()
	rs = pygame.display.set_mode((256 * 3, 224 * 3))
	vs = pygame.Surface((256, 224))
	clk = pygame.time.Clock()
	scene = ImageScene('title')
	rc = 0
	while True:
		
		pr =pygame.key.get_pressed()
		for ev in pygame.event.get():
			if ev.type == pygame.QUIT:
				return
			if ev.type == pygame.KEYDOWN:
				if ev.key == pygame.K_F4 and (pr[pygame.K_LALT] or pr[pygame.K_RALT]):
					return
		
		sp = pr[pygame.K_SPACE] or pr[pygame.K_RETURN]
		dx = -1 if pr[pygame.K_LEFT] else (1 if pr[pygame.K_RIGHT] else 0)
		dy = -1 if pr[pygame.K_UP] else (1 if pr[pygame.K_DOWN] else 0)
		
		rc += 1
		
		scene= scene.next
		scene.update(sp, dx, dy)
		scene.render(vs, rc)
		
		scene = scene.next
		
		pygame.transform.scale(vs, rs.get_size(), rs)
		
		pygame.display.flip()
		
		clk.tick(30)