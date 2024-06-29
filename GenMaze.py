from Config import *
import random

def break_wall(current, new, grid):
	if current.y == new.y:
		if current.x > new.x:
			grid[current.y][current.x-1].wall = False
		else:
			grid[current.y][current.x+1].wall = False
	else:
		if current.y > new.y:
			grid[current.y-1][current.x].wall = False
		else:
			grid[current.y+1][current.x].wall = False

def genMaze(grid):

	for y in range(rows):
		for x in range(cols):
			grid[y][x].wall = True

	for y in range(0,rows,2):
		for x in range(0,cols,2):
			grid[y][x].wall = False

	begin = grid[0][0]
	open_set = []
	visited = []
	open_set.append(begin)
	visited.append(open_set)

	while len(open_set) > 0:
		move = []

		#Right
		if begin.x + 2 < cols:
			neighbor = grid[begin.y][begin.x+2]
			if neighbor not in visited and neighbor.wall == False:
				move.append(neighbor)
		
		#Left
		if begin.x - 2 >= 0:
			neighbor = grid[begin.y][begin.x-2]
			if neighbor not in visited and neighbor.wall == False:
				move.append(neighbor)

		#Up
		if begin.y - 2 >= 0:
			neighbor = grid[begin.y-2][begin.x]
			if neighbor not in visited and neighbor.wall == False:
				move.append(neighbor)

		#Down	
		if begin.y + 2 < rows:
			neighbor = grid[begin.y+2][begin.x]
			if neighbor not in visited and neighbor.wall == False:
				move.append(neighbor)
		
		if len(move) > 0:
			new = random.choice(move)
			break_wall(begin, new, grid)
			begin = new
			visited.append(begin)
			open_set.append(begin)
		else:
			begin = open_set.pop()
			if begin != grid[0][0]:
				begin.wall = False