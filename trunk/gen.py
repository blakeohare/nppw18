for y in range(1, 7):
	for x in range(1, 11):
		t = 'X' * 16 + '\r\n'
		m = 'X' + 'I' * 14 + 'X\r\n'
		data = t + m * 12 + t
		data = data[:-2]
		
		if not (y > 4 or x == 4 or (y == 4 and x < 6)):
			music = 'd'
			
		else:
			music = 'o'
			data = data.replace('X', 'R').replace('I', 'L')
		
		c = open('maps\\' + str(x) + '-' + str(y) + '-' + music + '.txt', 'wb')
		c.write(data)
		c.close()