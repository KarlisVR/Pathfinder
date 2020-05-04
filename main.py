""" 
	Pathfinder implements A* algorithm to find a path between two nodes.
	User can choose the start and end node, and create obstacales
	between them.
"""

import math
import pygame

# Node visual parameters
node_width = 20
node_height = 20
node_margin = 2

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
grey = (192, 192, 192)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
turquoise = (0, 255, 255)
purple = (255, 0, 255)

# Create a 2d array of 0s
grid_size = 30
grid = [[0 for x in range(grid_size)] for y in range(grid_size)]

# Position of Start and End
start_node_pos = {}
end_node_pos = {}

# Goes over the grid to find and delete one node value
def delete_node(value):
	for i in range(grid_size):
		for j in range(grid_size):
			if grid[i][j] == value:
				grid[i][j] = 0
				break

# Calculate the distance between two nodes
def distance(x1, y1, x2, y2):
	result = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2)) * 10
	return round(result)

# Sort nodes based on f_cost
def sort_f_cost(e):
	return e['f_cost']

# A* search algorithm
def pathfinding():
	open_nodes = []		# The set of nodes to be evaluated
	closed_nodes = []	# The set of nodes already evaluated

	# Parameters of Start node
	g_cost = 0
	h_cost = distance(
		start_node_pos['row'],
		start_node_pos['column'],
		end_node_pos['row'],
		end_node_pos['column'])
	f_cost = g_cost + h_cost
	parent = []

	# Adding the Start node to open_nodes
	open_nodes.append({
		'row': start_node_pos['row'],
		'column': start_node_pos['column'],
		'g_cost': g_cost,
		'h_cost': h_cost,
		'f_cost': f_cost,
		'parent': parent})
			
	running = True		
	while running:
		# If there is no path
		if not open_nodes:
			break

		# Sort open_nodes based on f_cost
		open_nodes.sort(key=sort_f_cost)

		# Take out node with lowest f_cost
		current_node = open_nodes.pop(0)

		# Add current_node to closed_nodes
		closed_nodes.append(current_node)

		# If current_node is end_node, exit loop
		if (current_node['row'] == end_node_pos['row'] and
			current_node['column'] == end_node_pos['column']):
			running = False

		# All the current_node neighbours postitions
		top_left_neighbour_pos = {
			'row': current_node['row'] - 1,
			'column': current_node['column'] - 1}
		top_center_neighbour_pos = {
			'row': current_node['row'] - 1,
			'column': current_node['column']}
		top_right_neighbour_pos = {
			'row': current_node['row'] - 1,
			'column': current_node['column'] + 1}

		middle_left_neighbour_pos = {
			'row': current_node['row'],
			'column': current_node['column'] - 1}
		middle_right_neighbour_pos = {
			'row': current_node['row'],
			'column': current_node['column'] + 1}

		bottom_left_neighbour_pos = {
			'row': current_node['row'] + 1,
			'column': current_node['column'] - 1}
		bottom_center_neighbour_pos = {
			'row': current_node['row'] + 1,
			'column': current_node['column']}
		bottom_right_neighbour_pos = {
			'row': current_node['row'] + 1,
			'column': current_node['column'] + 1}

		neighbours_pos = [
			top_left_neighbour_pos,
			top_center_neighbour_pos,
			top_right_neighbour_pos,
			middle_left_neighbour_pos,
			middle_right_neighbour_pos,
			bottom_left_neighbour_pos,
			bottom_center_neighbour_pos,
			bottom_right_neighbour_pos
		]

		for neighbour_pos in neighbours_pos:
			# Check if neighbour is in closed_nodes
			node_in_closed = False
			for node in closed_nodes:
				if (node['row'] == neighbour_pos['row'] and
					node['column'] == neighbour_pos['column']):
					node_in_closed = True
					break

			# Skip neighbour if it is outside the grid, 
			# or a wall, or in closed_nodes
			if (neighbour_pos['row'] < 0 or
				neighbour_pos['row'] > (grid_size - 1) or
				neighbour_pos['column'] < 0 or
				neighbour_pos['column'] > (grid_size - 1) or
				grid[neighbour_pos['row']][neighbour_pos['column']] == 1 or
				node_in_closed == True):
				continue

			# Neighbour node parameters
			g_cost = distance(
				neighbour_pos['row'],
				neighbour_pos['column'],
				current_node['row'],
				current_node['column'])
			h_cost = distance(
				neighbour_pos['row'],
				neighbour_pos['column'],
				end_node_pos['row'],
				end_node_pos['column'])
			f_cost = g_cost + h_cost
			parent = current_node

			neighbour = {
				'row': neighbour_pos['row'],
				'column': neighbour_pos['column'],
				'g_cost': g_cost,
				'h_cost': h_cost,
				'f_cost': f_cost,
				'parent': parent
			}

			# Check if neighbour is in open_nodes
			node_in_open = False
			for node in open_nodes:
				if (node['row'] == neighbour['row'] and
					node['column'] == neighbour['column']):
					node_in_open = True

					# Update node f_cost and parent if necessary
					if node['f_cost'] > neighbour['f_cost']:
						node['f_cost'] = neighbour['f_cost']
						node['parent'] = neighbour['parent']
					break

			# Add neighbour to open_nodes if it wasn't
			if node_in_open == False:
				open_nodes.append(neighbour)

	# Add open_nodes and closed_nodes to the grid
	for node in open_nodes:
		grid[node['row']][node['column']] = 4

	for node in closed_nodes:
		grid[node['row']][node['column']] = 5

	# Find shortest path from closed_nodes if there is a path
	if open_nodes:
		node = closed_nodes[-1]
		while node['parent'] != []:
			grid[node['row']][node['column']] = 6
			node = node['parent']
		grid[node['row']][node['column']] = 6

pygame.init()

# Grid and text box dimensions
text_box_height = 50
grid_length = grid_size * (node_width + node_margin) + node_margin

# Screen dimensions
screen_width = grid_length
screen_height = grid_length + text_box_height
screen = pygame.display.set_mode((screen_width, screen_height))

# Caption and Icon
pygame.display.set_caption('Pathfinder')
icon = pygame.image.load('small_angry.png')
pygame.display.set_icon(icon)

# Manage how fast the screen updates
clock = pygame.time.Clock()

# Text that describes the controls
font = pygame.font.Font('freesansbold.ttf', 14)

text_1 = font.render('Left mouse button draws a wall', True, black, white)
text_2 = font.render('Right mouse button erases', True, black, white)
text_3 = font.render('S key draws the Start', True, black, white)
text_4 = font.render('E key draws the End', True, black, white)
text_5 = font.render('Space key finds the path', True, black, white)
text_6 = font.render('C key clears the grid', True, black, white)

# Game Loop
running = True
while running:
	# Main event loop
	for event in pygame.event.get():
		# Get the mouse position
		position = pygame.mouse.get_pos()
		column = position[0] // (node_width + node_margin)
		row = position[1] // (node_height + node_margin)

		# Make sure that mouse is inside the grid
		in_grid = True
		if (row < 0 or row > (grid_size - 1) or
			column < 0 or column > (grid_size - 1)):
			in_grid = False

		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEMOTION:
			# On left mouse button movement draw, on right delete
			if in_grid:
				if event.buttons[0] == 1:
					grid[row][column] = 1
				elif event.buttons[2] == 1:
					grid[row][column] = 0
		elif event.type == pygame.MOUSEBUTTONDOWN:
			# On left mouse button click draw, on right delete
			if in_grid:
				if event.button == 1:
					grid[row][column] = 1
				elif event.button == 3:
					grid[row][column] = 0
		elif event.type == pygame.KEYDOWN:
			# On s key create the start node, 
			if event.key == pygame.K_s:
				if in_grid:
					delete_node(2)
					grid[row][column] = 2
					start_node_pos = {'row': row, 'column': column}
			# On e key create the end node
			elif event.key == pygame.K_e:
				if in_grid:
					delete_node(3)
					grid[row][column] = 3
					end_node_pos = {'row': row, 'column': column}
			# On space key run A* algorithm
			elif event.key == pygame.K_SPACE:
				if start_node_pos != {} and end_node_pos != {}:
					pathfinding()
			# On c key clear the grid
			elif event.key == pygame.K_c:
				grid = [[0 for x in range(grid_size)] 
					for y in range(grid_size)]
						
	# Set background color
	screen.fill(grey)
 
	# Draw the grid
	for row in range(grid_size):
		for column in range(grid_size):
			# Color each node based on grid value
			color = white
			if grid[row][column] == 1:
				color = black
			elif grid[row][column] == 2:
				color = turquoise
			elif grid[row][column] == 3:
				color = purple
			elif grid[row][column] == 4:
				color = green
			elif grid[row][column] == 5:
				color = red
			elif grid[row][column] == 6:
				color = blue

			pygame.draw.rect(
				screen,
				color,
				(column * (node_width + node_margin) + node_margin,
				row * (node_height + node_margin) + node_margin,
				node_width,
				node_height))

	# Info about the controls
	pygame.draw.rect(
		screen,
		white,
		(0,
		grid_length,
		screen_width,
		text_box_height))

	screen.blit(text_1, (5, grid_length + 5))
	screen.blit(text_2, (5, grid_length + 25))

	screen.blit(text_3, (250, grid_length + 5))
	screen.blit(text_4, (250, grid_length + 25))

	screen.blit(text_5, (450, grid_length + 5))
	screen.blit(text_6, (450, grid_length + 25))

	# Updates screen with what is drawn
	pygame.display.update()

	# Limit to 60 frames per second
	clock.tick(60)