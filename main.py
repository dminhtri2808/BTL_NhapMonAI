import pygame
from tkinter import messagebox, Tk
import sys
from heapq import *
from Config import *
from GenMaze import *


pygame.init()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Path Finding Algorithms")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri", 24)


class Cell:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.start = False
		self.wall = False
		self.target = False
		self.queue = False
		self.visited = False
		self.neighbors = []
		self.prior = None

	# Draw self cell
	def draw(self, screen, color):
		pygame.draw.rect(screen, color, (self.x*GAP, self.y*GAP, GAP-2, GAP-2))

	# Get all cell neighbors of self
	def set_neighbors(self):
		if x > 0:
			self.neighbors.append(grid[y][x-1]) # Right
		if x < cols - 1:
			self.neighbors.append(grid[y][x+1]) # Left
		if y > 0:
			self.neighbors.append(grid[y-1][x]) # Up 
		if y < rows - 1:
			self.neighbors.append(grid[y+1][x]) # Down
	def set_default(self):
		self.start = False
		self.wall = False
		self.target = False
		self.queue = False
		self.visited = False
		self.prior = None
		self.flag = False


def heuristic(point1, point2):
	return abs(point1.x - point2.x) + abs(point1.y - point2.y)


grid = []
# Create grid (dimension = rows * cols)
for y in range(rows):
	arr = []
	for x in range(cols):
		arr.append(Cell(x,y)) # One arr have items = numbers column
	grid.append(arr)
# Set all neighbors for each point
for y in range(rows):
	for x in range(cols):
		grid[y][x].set_neighbors()


def main():
	global queue, path, best_path, cost
	queue = []
	path = []
	best_path = []
	cost = float("inf")

	#Setting basic
	begin_search = False
	searching = True
	start_point_set = False
	target_point_set = False
	target_point = None
	start_point = None
	g_score = {}
	

	BFS = False
	ASTAR = False
	BNB = False


	while True:
		for event in pygame.event.get():
			
			# Event Quit Window
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			# Event control mouse
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# Event click mouse left
				if event.button == 1:
					mouse_x, mouse_y = pygame.mouse.get_pos()
					x = mouse_x//GAP
					y = mouse_y//GAP
					# While start_point has't been initialized yet
					if not start_point_set and not grid[y][x].wall:
						# Setting start point
						start_point = grid[y][x]
						start_point.start = True
						start_point.visited = True
						queue.append(start_point)
						start_point_set = True
				# Event click mouse right
				elif event.button == 3:
					mouse_x, mouse_y = pygame.mouse.get_pos()
					x = mouse_x//GAP
					y = mouse_y//GAP
					# While target_point has't been initialized
					if not target_point_set and not grid[y][x].wall:
						# Setting target point
						if (start_point != None):
							if x == start_point.x and y == start_point.y:
								continue
						target_point = grid[y][x]

						target_point.target = True
						target_point_set = True				

			elif event.type == pygame.MOUSEMOTION:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				# Draw wall
				if event.buttons[0]:
					x = mouse_x//GAP
					y = mouse_y//GAP
					if grid[y][x].start != True and grid[y][x].target != True:
						grid[y][x].wall = True
			
			#Star algorithms
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c and target_point_set and start_point_set:
					BFS = True
					begin_search = True
				elif event.key == pygame.K_a and target_point_set and start_point_set:
					ASTAR = True
					begin_search = True
					queue = []
					for y in range(rows):
						for x in range(cols):
							g_score[(x,y)] = float("inf")
					queue.append((0,start_point))
					point = (start_point.x, start_point.y)
					g_score[point] = 0

				elif event.key == pygame.K_b and target_point_set and start_point_set:
					BNB = True
					begin_search = True
					queue = []
					for y in range(rows):
						for x in range(cols):
							g_score[(x,y)] = float("inf")

					queue.append((heuristic(start_point, target_point),start_point))
					point = (start_point.x, start_point.y)
					g_score[point] = 0
				elif event.key == pygame.K_r:
					BFS = False
					ASTAR = False
					BNB = False
					queue = []
					path = []
					best_path = []
					cost = float("inf")

					#Setting basic
					begin_search = False
					searching = True
					start_point_set = False
					target_point_set = False
					target_point = None
					start_point = None
					g_score = {}
					for y in range(rows):
						for x in range(cols):
							grid[y][x].set_default()
					continue
				elif event.key == pygame.K_m:
					genMaze(grid)
					continue

		if begin_search:

			# While queue don't empty
			if len(queue) > 0 and searching:
				if BFS: 
					cur_point = queue.pop(0)
					cur_point.visited = True
					if cur_point == target_point:
						searching = False
						while cur_point.prior != start_point:
							path.append(cur_point.prior)
							cur_point = cur_point.prior
					else:
						for neighbor in cur_point.neighbors:
							if not neighbor.queue and not neighbor.wall:
								queue.append(neighbor) 
								neighbor.queue = True
								neighbor.prior = cur_point
				elif ASTAR:
					f_cur, cur_point = queue.pop(0)
					cur_point.visited = True
					if cur_point == target_point:
						searching = False
						while cur_point.prior != start_point:
							path.append(cur_point.prior)
							cur_point = cur_point.prior
					else:
						for neighbor in cur_point.neighbors:
							point_cur = (cur_point.x, cur_point.y)
							temp_gScore = g_score[point_cur] + 1
							point_neighbor = (neighbor.x, neighbor.y)
							if not neighbor.queue and not neighbor.wall and temp_gScore < g_score[point_neighbor]:
								g_score[point_neighbor] = temp_gScore
								f_score = g_score[point_neighbor] + heuristic(neighbor, target_point)
								queue.append((f_score, neighbor))
								queue = sorted(queue, key=lambda x: x[0])
								neighbor.queue = True
								neighbor.prior = cur_point
				elif BNB:
					if len(queue) > 0:
						f_cur, cur_point = queue.pop(0)
						cur_point.visited = True
						if cur_point == target_point:
							point_cur = (cur_point.x, cur_point.y)
							if g_score[point_cur] <= cost:
								cost = g_score[point_cur]
								while cur_point.prior != start_point:
									path.append(cur_point.prior)
									cur_point = cur_point.prior
								best_path = path
								path = []
						else:
							if f_cur > cost:
								continue
							temp = []
							for neighbor in cur_point.neighbors:
								point_cur = (cur_point.x, cur_point.y)
								temp_gScore = g_score[point_cur] + 1
								point_neighbor = (neighbor.x, neighbor.y)
								if not neighbor.queue and not neighbor.wall and temp_gScore < g_score[point_neighbor]:
									g_score[point_neighbor] = temp_gScore
									f_score = g_score[point_neighbor] + heuristic(neighbor, target_point)
									temp.append((f_score, neighbor))
									neighbor.queue = True
									neighbor.prior = cur_point
							temp = sorted(temp, key=lambda x: x[0])
							queue = temp + queue
						
			else:
				if searching:
					if BFS or ASTAR:
						Tk().wm_withdraw()
						messagebox.showinfo("No Solution", "There is no solution!")
						searching = False
					elif BNB:
						path = best_path
						searching = False
					
						while cur_point.prior != start_point:
							path.append(cur_point.prior)
							cur_point = cur_point.prior
			

			sc.fill((0,0,0))


		for y in range(rows):
			for x in range(cols):
				cell = grid[y][x]
				cell.draw(sc, COLOR_PATH)

				if cell.queue:
					cell.draw(sc, COLOR_QUEUE)
				if cell.visited:
					cell.draw(sc, COLOR_VISITED)
				if cell in path:
					cell.draw(sc, COLOR_BEST_PATH)

				if cell.start:
					cell.draw(sc, COLOR_START)
				if cell.wall:
					cell.draw(sc, COLOR_WALL)
				if cell.target:
					cell.draw(sc, COLOR_TARGET)


				# Render instructions text
			instructions = [
				"Instructions:",
				"1. Left click to set start",
				"2. Left click and hold to draw walls",
				"3. Right click to set target",
				"4. Click A run A star",
				"5. Click B run BNB",
				"6. Click C run BFS",
				"7. Click R to restart",
				"8. Click M to generate Maze"
			]
			for i, instruction in enumerate(instructions):
				text_surface = font.render(instruction, True, (255, 255, 255))
				sc.blit(text_surface, (0, WIN_HEIGHT - (len(instructions) - i) * 20 - 10))


		pygame.display.flip()
		clock.tick(144)

main()