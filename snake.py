import time
import curses
import curses.textpad
import random

WIN_SNAKE_DATA = [
"                 .-'`     '.                        ",
"              __/  __       \                       ",
"             /  \ /  \       |    ___               ",
"            | /`\| /`\|      | .-'  /^\/^\          ",
"            | \(/| \(/|      |/     |) |)|          ",
"           .-\__/ \__/       |      \_/\_/__..._    ",
"   _...---'-.                /   _              '.  ",
"  /,      ,             \   '|  `\  sergio        \ ",
" | ))     ))           /`|   \    `.       /)  /) | ",
" | `      `          .'       |     `-._         /  ",
" \    anastasia    .'         |     ,_  `--....-'   ",
"  `.           __.' ,         |     / /`'''`        ",
"    `'-.____.-' /  /,         |    / /              ",
"        `. `-.-` .'  \        /   / |               ",
"          `-.__.'|    \      |   |  |-.             ",
"             _.._|     |     /   |  |  `'.          ",
]

LOSS_SNAKE_DATA = [
"       ---_ ......._-_--.     ",
"      (|\ /      / /| \  \    ",
"      /  /     .'  -=-'   `.  ",
"     /  /    .'             ) ",
"   _/  /   .'        _.)   /  ",
"  / o   o        _.-' /  .'   ",
"  \          _.-'    / .'*|   ",
"   \______.-'//    .'.' \*|   ",
"    \|  \ | //   .'.' _ |*|   ",
"     `   \|//  .'.'_ _ _|*|   ",
"      .  .// .'.' | _ _ \*|   ",
"      \`-|\_/ /    \ _ _ \*\  ",
"       `/'\__/      \ _ _ \*\ ",
"      /^|            \ _ _ \* ",
"     '  `             \ _ _ \ ",
"       W A S T E D     \_     "
]


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


def check_if_direction_is_allowed(key, direction):
    if key == "KEY_DOWN" and direction == "KEY_UP":
      return False
    elif key == "KEY_UP" and direction == "KEY_DOWN":
      return False
    elif key == "KEY_LEFT" and direction == "KEY_RIGHT":
      return False
    elif key == "KEY_RIGHT" and direction == "KEY_LEFT":
      return False
    else: 
      return True 
    

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
    scr.clear()
    draw_border(scr)

    height, width = scr.getmaxyx() 
    x, y = width//2, height//2
       
    drawstr(scr, x-8, y-5, "G A M E  O V E R", curses.color_pair(1))
    scr.refresh()
    time.sleep(3)
    snake_screen(scr, LOSS_SNAKE_DATA, curses.color_pair(1))


def clear_keys_buffer(scr):
    # forcely clear keys buffer by reading it out
    scr.nodelay(True)
    while True:
      try:
        scr.getkey()
      except:
        break
    scr.nodelay(False)


def win_screen(scr):
    time.sleep(1)
    scr.clear()
    draw_border(scr)

    height, width = scr.getmaxyx() 
    x, y = width//2, height//2
    drawstr(scr, x-17, y-6, "OH BOY, YOU'VE GOT A HUGE ANACONDA!", curses.color_pair(4))
    drawstr(scr, x-15, y-4, "C O N G R A T U L A T I O N S !", curses.color_pair(4))

    scr.refresh()
    time.sleep(3)
    snake_screen(scr, WIN_SNAKE_DATA, curses.color_pair(5))


def snake_screen(scr, snake_items, color):
  scr.clear()
  for i in range(len(snake_items)):
    x = 1
    y = 1 + i
    line = snake_items[i]
    drawstr(scr, x, y, line, color)
    scr.refresh()
    time.sleep(0.1)
  time.sleep(3)


def hello_screen(scr):
    # clear keys buffer to prevent game autostart 
    # by buffered key values from previous game session 
    clear_keys_buffer(scr)

    # forcely disable halfdelay mode    
    curses.cbreak()
    scr.keypad(True)
    
    scr.clear()
    
    draw_border(scr)
    scr.refresh()
    time.sleep(0.5)
    drawstr(scr, 4, 2, "HELLO, FRIEND.")
    drawstr(scr, 4, 3, "GROW YOUR OWN ANACONDA!")
    drawstr(scr, 4, 4, "BE A MAN!")
    scr.refresh()
    time.sleep(1.5)

    drawstr(scr, 4, 5, ".. OR A WOMAN!")
    scr.refresh()

    time.sleep(1.5)
    drawstr(scr, 4, 7, "Use arrow keys to move anaconda.")
    drawstr(scr, 4, 8, "Press q to quit the game at any moment.")
    drawstr(scr, 4, 9, "Press any other key to start the game.")
    drawstr(scr, 4, 11, "You have to eat ")
    drawstr(scr, 20, 11, "15 mushrooms ", curses.color_pair(1))
    drawstr(scr, 33, 11, "to win the game.")
    drawstr(scr, 4, 12, "Your anaconda is very hungry..")
    
    return scr.getkey()
    

def game_loop(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx() 
    chleniks = [(10, 10), (9, 10), (8, 10), (7, 10), (6, 10)]
    draw_snake(stdscr, chleniks)
    draw_border(stdscr) 
    
    mush_x, mush_y = create_mushroom(stdscr)
    draw_mushroom(stdscr, mush_x, mush_y)
    direction = "KEY_RIGHT"
    mushroom_eaten = 0

    curses.halfdelay(3)

    while True:
      action = get_action(stdscr, direction)
      if action in ["KEY_UP", "KEY_DOWN", "KEY_RIGHT", "KEY_LEFT"]:
        if check_if_direction_is_allowed(action, direction):
          direction = action
          move_snake(direction, chleniks)        
      elif action == "EXIT":
        return "EXIT"
      elif action == "CRASH":
        x, y = chleniks[0]       
        drawstr(stdscr, x, y, 'BAD BOY!')
        stdscr.refresh()
        time.sleep(0.3)
      else:
        raise("Incorrect action: {}!".format(action))

      if chleniks[0] == (mush_x, mush_y):
        mushroom_eaten += 1
        if mushroom_eaten == 15:
          return "WIN"
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
          return "LOSS"

      if chleniks[0] in chleniks[1:]:
          game_over(stdscr)
          return "LOSS"

      stdscr.clear() 
      draw_border(stdscr)
      draw_snake(stdscr, chleniks)
      draw_mushroom(stdscr, mush_x, mush_y)       


def main(stdscr):    
    curses.curs_set(False)

    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)    
    curses.init_pair(3, curses.COLOR_BLUE, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)
    curses.init_pair(5, curses.COLOR_CYAN, -1)

    # creating custom color to make anaconda looks like kolbaska
    #curses.init_color(10, 17, 117, 24)

    while True:
      key = hello_screen(stdscr)
      if key == 'q':
        return
    
      result = game_loop(stdscr)
      if result == "WIN":
        win_screen(stdscr)
        break
      elif result == "LOSS":
        continue
      elif result == "EXIT":
        break
      else:
        raise "Unexpected game_loop result: {}!".format(result)

curses.wrapper(main)
print("Серёжа и Настя котики!")
