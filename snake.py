import time
import curses
import curses.textpad
import random


def draw(scr, x, y, ch, style = curses.A_NORMAL):
    scr.addch(y, x, ch, style)


def drawstr(scr, x, y, s, style = curses.A_NORMAL):
    scr.addstr(y, x, s, style)


def draw_snake(scr, chleniks):  
    for i in range(0, len(chleniks)):
      x = chleniks[i][0]
      y = chleniks[i][1]
      draw(scr, x, y, "*", curses.color_pair(2))


def create_mushroom(scr):
    height, width = scr.getmaxyx() 
     
    x = random.randint(1, width-2)
    y = random.randint(1, height-2)
    return x, y


def draw_mushroom(scr, x, y):
    draw(scr, x, y, "T", curses.color_pair(1))


def move(direction, x, y):
    if direction == "KEY_UP":
      y -= 1
    elif direction == "KEY_DOWN":         
      y += 1
    elif direction == "KEY_RIGHT":         
      x += 1
    elif direction == "KEY_LEFT":
      x -= 1 

    return x, y


def move_snake(direction, chleniks):
    for i in range(len(chleniks)-1, 0, -1):
      x, y = chleniks[i]
      x2, y2 = chleniks[i-1]
      x, y = x2, y2
      chleniks[i] = x, y

    x, y = chleniks[0]
    chleniks[0] = move(direction, x, y)  


def get_action(scr, direction):
    try:
      key = scr.getkey()
    except:
      return direction

    if key in ["KEY_UP", "KEY_DOWN", "KEY_RIGHT", "KEY_LEFT"]:
      return key
    elif key == "q":
      return "EXIT"
    else:
      return "CRASH"


def draw_border(scr):
    y, x = scr.getmaxyx()
    scr.hline(0, 0, "#", x-1, curses.color_pair(3)) 
    scr.hline(y-1, 0, "#", x, curses.color_pair(3)) 
    scr.vline(0, 0, "#", y-1, curses.color_pair(3))
    scr.vline(0, x-1, "#", y-1, curses.color_pair(3))


def game_over(scr):
    time.sleep(1)
    curses.textpad.rectangle(scr, 1, 1, 5, 30)
    drawstr(scr, 7, 2, "                ")
    drawstr(scr, 8, 3, "G A M E  O V E R", curses.color_pair(1))
    drawstr(scr, 7, 4, "                ")
    scr.refresh()
    time.sleep(3)


def main(stdscr):
    curses.halfdelay(3)
    curses.curs_set(False)

    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    #curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_color(10, 17, 117, 24)
    curses.init_pair(3, curses.COLOR_BLUE, -1)

    height, width = stdscr.getmaxyx() 
    chleniks = [(10, 10), (9, 10), (8, 10), (7, 10), (6, 10)]
    draw_snake(stdscr, chleniks)
    draw_border(stdscr) 

    mush_x, mush_y = create_mushroom(stdscr)
    draw_mushroom(stdscr, mush_x, mush_y)
    direction = "KEY_RIGHT"
        
    while True:    
      action = get_action(stdscr, direction)
      if action in ["KEY_UP", "KEY_DOWN", "KEY_RIGHT", "KEY_LEFT"]:
        direction = action
        move_snake(direction, chleniks)        
      elif action == "EXIT":
        break
      elif action == "CRASH":
        x, y = chleniks[0]       
        drawstr(stdscr, x, y, 'POPKA!')
        stdscr.refresh()
        time.sleep(0.3)
      else:
        raise('Incorrect action: {}!'.format(action))

      if chleniks[0] == (mush_x, mush_y):
        mush_x, mush_y = create_mushroom(stdscr)
        last_index = len(chleniks)-1
        chleniks.append(chleniks[last_index])

      head_x = chleniks[0][0]
      head_y = chleniks[0][1]
      if head_x == width or \
        head_x == 0 or \
        head_y == height or \
        head_y == 0:
          game_over(stdscr)
          return

      if chleniks[0] in chleniks[1:]:
          game_over(stdscr)
          return

      stdscr.clear() 
      draw_border(stdscr)
      draw_snake(stdscr, chleniks)
      draw_mushroom(stdscr, mush_x, mush_y)       

curses.wrapper(main)
print("Серёжа и Настя котики!")
