import os

PASSABLE_TILES = 'LIGFM'
ALL_TILES = 'LIGFMXWARDBHTUE123'
SPRITE_IDS = '!@#$%&^*{}?'


def make_grid(w, h):
	output = []
	for i in range(w):
		output.append([None] * h)
	return output

def get_col(tiles, x):
	if tiles == None: return []
	output = []
	for y in range(14):
		output.append(tiles[x][y])
	return output

def get_row(tiles, y):
	if tiles == None: return []
	output = []
	for x in range(16):
		output.append(tiles[x][y])
	return output

def passability(tiles):
	output = []
	for tile in tiles:
		output.append('1' if tile[1] else '0')
	return output

def verify_maps():
	maps = make_grid(10, 6)
	size_failure = False
	file_lookup = make_grid(10, 6)
	for file in os.listdir('maps'):
		path = 'maps' + os.sep + file
		c = open(path, 'rt')
		lines = c.read().strip().split('\n')
		c.close()
		
		col, row, music = file.split('.')[0].split('-')
		col = int(col) - 1
		row = int(row) - 1
		
		file_lookup[col][row] = file
		
		tiles = make_grid(16, 14)
		if len(lines) != 14:
			print( file + " does not have 14 lines")
			size_failure = True
			continue
		
		for y in range(14):
			if len(lines[y]) != 16:
				print (file + " has a row that is not 16 characters")
				size_failure = True
				break
		
		if size_failure:
			continue
		
		for y in range(14):
			for x in range(16):
				id = lines[y][x].upper()
				if id in SPRITE_IDS:
					id = 'I'
					if x in (0, 15) or y in (0, 13):
						print( file + " has a sprite on the edge (" + str(x) + ", " + str(y) + ")")
				if not (id in ALL_TILES):
					print( file + " has unrecognized tile ID (" + str(x) + ", " + str(y) + "): " + id)
				tiles[x][y] = (id, id in PASSABLE_TILES)
		maps[col][row] = tiles
	if size_failure:
		print ("Size check failed. Skipping rest of verification.")
		return
	
	for col in range(10):
		for row in range(6):
			if maps[col][row] == None:
				print (str(col + 1) + '-' + str(row + 1) + '-?.txt is MISSING!!!!!!!!!!!!!!!!!!!!!!!!!!')
			else:
				if col > 0:
					# verify left column matches map to the left's right column
					if passability(get_col(maps[col][row], 0)) != passability(get_col(maps[col - 1][row], 15)):
						print( file_lookup[col][row], "left column doesn't match right column of", file_lookup[col - 1][row])
				if row > 0:
					# verify top row matches bottom row of map above it
					if passability(get_row(maps[col][row], 0)) != passability(get_row(maps[col][row - 1], 13)):
						print( file_lookup[col][row], "top row doesn't match bottom row of", file_lookup[col][row - 1])
				tiles = maps[col][row]
				closed = True
				for x in range(16):
					for y in (0, 13):
						if tiles[x][y][1]:
							closed = False
				for y in range(14):
					for x in (0, 15):
						if tiles[x][y][1]:
							closed = False
				if closed:
					print (file_lookup[col][row], "is completely walled off.")

verify_maps()