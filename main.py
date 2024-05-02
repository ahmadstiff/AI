# Mengimpor modul Tk dan messagebox dari tkinter
from tkinter import Tk, messagebox
# Mengimpor modul pygame
import pygame
# Mengimpor kelas PriorityQueue dari modul queue
from queue import PriorityQueue

WIDTH = 450 # Lebar dari papan permainan
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm")

# Warna-warna dalam game
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

num = 0

#Class for the indiviual square drawn on the grid
class Node:
  def __init__(self, row, col, width, total_rows): #inital attributes
    self.row = row
    self.col = col
    self.x = row * width # x-coordinate
    self.y = col * width # y-coordinate
    self.colour = WHITE
    self.neighbours = []
    self.width = width
    self.total_rows = total_rows

  def get_position(self): #gets the position of the node
    return self.row, self.col

  def is_closed(self): #checks to see of the position if not considered for the shortest path and part of the closed set
    return self.colour == RED

  def is_open(self): #checks of the node is in the open set
    return self.colour == GREEN

  def is_border(self): #checks for the borders
    return self.colour == BLACK

  def is_start(self): #checks for the start
    return self.colour == ORANGE

  def is_end(self): #checks for the end
    return self.colour == TURQUOISE

  def reset(self): #RESET
    self.colour = WHITE

  def make_closed(self): 
    self.colour = RED

  def make_open(self): 
    self.colour = GREEN

  def make_border(self): 
    self.colour = BLACK

  def make_start(self): 
    self.colour = ORANGE

  def make_end(self): 
    self.colour = TURQUOISE 

  def make_path(self):
    self.colour = PURPLE

  def draw(self, win): #draws node within the defined window
    pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

  def update_neighbours(self, grid):
    self.neighbours = []
    if self.row < self.total_rows -1 and not grid[self.row + 1][self.col].is_border(): #checks the neighbours in the down direction
      self.neighbours.append(grid[self.row + 1][self.col])

    if self.row > 0 and not grid[self.row - 1][self.col].is_border(): #checks the neighbours in the up direction
      self.neighbours.append(grid[self.row - 1][self.col])

    if self.col < self.total_rows -1 and not grid[self.row][self.col + 1].is_border(): #checks the neighbours in the right direction
      self.neighbours.append(grid[self.row][self.col + 1])

    if self.col > 0 and not grid[self.row][self.col - 1].is_border(): #checks the neighbours in the right direction
      self.neighbours.append(grid[self.row][self.col - 1])

  def __lt__(self, other):
    return False

#Using Manhattan distance to find the distnace between the start and end
def h(p1, p2): 
  x1, y1 = p1
  x2, y2 = p2
  return abs(x1 - x2) + abs(y1 - y2) #Manhattan distance formula

#Draws the path from the start and end nodes
def draw_path(came_from, current, draw): 
  global num

  while current in came_from:
    current = came_from[current]
    current.make_path()
    num += 1
    draw()

#Algorith to find the shortest path between the start and end nodes
def algorithm(draw, grid, start, end):
  count = 0
  open_set = PriorityQueue()
  open_set.put((0, count, start))
  came_from = {} #node that was previously visited
  g_score = {node: float("inf") for row in grid for node in row} #current shortest distance from start to end node, default value of infi
  g_score[start] = 0
  f_score = {node: float("inf") for row in grid for node in row} #predicted distance from start to end node, default value of infi
  f_score[start] = h(start.get_position(), end.get_position())

  open_set_hash = {start} #Keeps track of the priority queue

  while not open_set.empty():
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return
    
    current = open_set.get()[2] #gets the minimum node value
    open_set_hash.remove(current)

    if current == end:
      draw_path(came_from, end, draw)
      end.make_end()
      return True

    for neighbour in current.neighbours:
      temp_g_score = g_score[current] + 1

      if temp_g_score < g_score[neighbour]: #compare the g_scores to select the shorter distance and update
        came_from[neighbour] = current
        g_score[neighbour] = temp_g_score
        f_score[neighbour] = temp_g_score + h(neighbour.get_position(), end.get_position()) #calculates the f score
        if neighbour not in open_set_hash:
          count += 1
          open_set.put((f_score[neighbour], count, neighbour))
          open_set_hash.add(neighbour)
          neighbour.make_open()
    draw()

    if current != start:
      current.make_closed()

  return False

#Creates the grid to draw each node
def create_grid(rows, width): 
  grid = []
  grid_pixel_width = width // rows #integer division, also know as floor division
  for i in range(rows):
    grid.append([]) #creates a 2D grid
    for j in range(rows):
      node = Node(i, j, grid_pixel_width, rows)
      grid[i].append(node) #Stores the nodes within the 2D grid
  
  return grid

#Draws grid lines
def draw_grid(win, rows, width): 
  grid_pixel_width = width // rows
  for i in range(rows):
    pygame.draw.line(win, GREY, (0, i * grid_pixel_width), (width, i * grid_pixel_width)) #draws  horizontal lines
    for j in range(rows):
      pygame.draw.line(win, GREY, (j * grid_pixel_width, 0), (j * grid_pixel_width, width)) #draws vertical lines

#Draws the grid
def draw(win, grid, rows, width):
  win.fill(WHITE)
  
  for row in grid:
      for node in row:
          node.draw(win)
    
  draw_grid(win, rows, width)
  pygame.display.update()

#Gets the position of the squares on the grid
def get_position(pos, rows, width):
  grid_pixel_width = width // rows
  y, x = pos

  row = y // grid_pixel_width
  col = x // grid_pixel_width

  return row, col

def main(win, width):
  ROWS = 50 #Dimensions of the grid
  grid = create_grid(ROWS, width)

  set_start = False
  set_end = False

  #Game rules
  Tk().wm_withdraw()
  messagebox.showinfo('Game info', ('1. Letakkan awal dan akhir node\n2. Gambar penghalang pada grid\n3. Tekan spasi untuk memulai\n\n \n Klik kiri untuk menempatkan node \n Klik kanan untuk menghapus node\n Tekan C untuk menghapus grid\n Tekan Q untuk keluar'))

  #Game states
  running = True
  started = False
  done = False

  while running:
    draw(win, grid, ROWS, width)

    for event in pygame.event.get():
      if event.type == pygame.QUIT: #changes state to false after closing game
        running = False

      if started:
        continue

      if pygame.mouse.get_pressed()[0]: #Left click
        pos = pygame.mouse.get_pos() #gets the poistion of the pygame mouse 
        row, col = get_position(pos, ROWS, width) #gets the the value of the row and coloum
        node = grid[row][col]
        if set_start == False and node != set_end: #set the node as the start node 
          set_start = node
          set_start.make_start()
          print(f'Start Position({row},{col})')

        elif set_end == False and node != set_start: #set the node as the end node 
          set_end = node
          set_end.make_end()
          print(f'End Position({row},{col})')

        elif node != set_end and node != set_start: #set the node a barrier node 
          node.make_border()
          print(f'Border Position({row},{col})')

      elif pygame.mouse.get_pressed()[2]: #Right click
        pos = pygame.mouse.get_pos() #gets the poistion of the pygame mouse 
        row, col = get_position(pos, ROWS, width) #gets the the value of the row and coloum
        node = grid[row][col]
        node.reset() #sets the colour to white
        print(f'Removed Position({row},{col})')
        if node == set_start:
          set_start = False
        elif node == set_end:
          set_end = False   

      #Runs the algorithm to find the shortest distance between the start and end node
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and set_end and set_start:
          for row in grid:
            for node in row:
              node.update_neighbours(grid)

          algorithm(lambda: draw(win, grid, ROWS, width), grid, set_start, set_end)

          #Exit message box
          Tk().wm_withdraw()

          #Checks if user surrounds the end node with borders making it impossible to find the shortest distance
          if num != 0:
            result = messagebox.askyesno('Exit', ('Jarak Paling Pendek Dari Node Awal Ke Node Akhir Adalah ' + str(num) + ' blok.\n\nApakah anda ingin keluar?'))
          else: 
            result = messagebox.askyesno('Exit', ('Saya mohon maaf karena tidak bisa menemukan jarak terdekat. Saya merekomendasikan menghindari jalur yang mengelilingi node akhir untuk meningkatkan hasil.\n\nApakah anda ingin keluar?'))

          if result == True: #Quits the application 
              running = False
          else: #Clears the grid  
              set_start = False
              set_end = False
              grid = create_grid(ROWS, width)   
          
          if num == 0:
            print(f"ISaya mohon maaf karena tidak bisa menemukan jarak terdekat. Saya merekomendasikan menghindari jalur yang mengelilingi node akhir untuk meningkatkan hasil.")
          else:
            print(f"Jarak Paling Pendek Dari Node Awal Ke Node Akhir Adalah {num} blok")

        #Clears the grid  
        if event.key == pygame.K_c:
          set_start = False
          set_end = False
          grid = create_grid(ROWS, width)

        #Quits the application
        if event.key == pygame.K_q:
          running = False      
  pygame.quit()

main(WIN, WIDTH)