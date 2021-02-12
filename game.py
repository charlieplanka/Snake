import time
import curses
import curses.textpad
import random
from point import Point
from snake import Snake
from utils import draw_char
from direction import Direction
from action import Action
from mushroom import create_random_mushroom_on_screen

# ввести объект Стены

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

MUSHROOMS_TO_WIN = 2


def draw_str(scr, x, y, s, style=curses.A_NORMAL):
    scr.addstr(y, x, s, style)


def check_if_direction_is_allowed(action, direction):
    if action == Action.MOVE_DOWN and direction == Direction.UP:
        return False
    elif action == Action.MOVE_UP and direction == Direction.DOWN:
        return False
    elif action == Action.MOVE_LEFT and direction == Direction.RIGHT:
        return False
    elif action == Action.MOVE_RIGHT and direction == Direction.LEFT:
        return False
    else:
        return True


def get_action_from_key(key):
    if key in ["KEY_UP", "KEY_A2"]:
        return Action.MOVE_UP
    elif key in ["KEY_DOWN", "KEY_C2"]:
        return Action.MOVE_DOWN
    elif key in ["KEY_RIGHT", "KEY_B3"]:
        return Action.MOVE_RIGHT
    elif key in ["KEY_LEFT", "KEY_B1"]:
        return Action.MOVE_LEFT
    elif key == "q":
        return Action.EXIT
    else:
        return Action.CRASH


def get_direction_from_action(action):
    if action == Action.MOVE_UP:
        return Direction.UP
    elif action == Action.MOVE_DOWN:
        return Direction.DOWN
    elif action == Action.MOVE_RIGHT:
        return Direction.RIGHT
    elif action == Action.MOVE_LEFT:
        return Direction.LEFT
    else:
        raise Exception(f"Unknown action: {action}")


def get_action(scr):
    try:
        key = scr.getkey()
    except:
        return Action.NONE

    return get_action_from_key(key)


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

    draw_str(scr, x-8, y-5, "G A M E  O V E R", curses.color_pair(1))
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
    draw_str(scr, x-17, y-6, "OH BOY, YOU'VE GOT A HUGE ANACONDA!", curses.color_pair(4))
    draw_str(scr, x-15, y-4, "C O N G R A T U L A T I O N S !", curses.color_pair(4))

    scr.refresh()
    time.sleep(3)
    snake_screen(scr, WIN_SNAKE_DATA, curses.color_pair(5))


def snake_screen(scr, snake_items, color):
    scr.clear()
    for i in range(len(snake_items)):
        x = 1
        y = 1 + i
        line = snake_items[i]
        draw_str(scr, x, y, line, color)
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
    draw_str(scr, 4, 2, "HELLO, FRIEND.")
    draw_str(scr, 4, 3, "GROW YOUR OWN ANACONDA!")
    draw_str(scr, 4, 4, "BE A MAN!")
    scr.refresh()
    time.sleep(1.5)

    draw_str(scr, 4, 5, ".. OR A WOMAN!")
    scr.refresh()
    time.sleep(1.5)

    draw_str(scr, 4, 7, "Use arrow keys to move anaconda.")
    draw_str(scr, 4, 8, "Press q to quit the game at any moment.")
    draw_str(scr, 4, 9, "Press any other key to start the game.")
    draw_str(scr, 4, 11, "You have to eat ")
    draw_str(scr, 20, 11, "10 mushrooms ", curses.color_pair(1))
    draw_str(scr, 33, 11, "to win the game.")
    draw_str(scr, 4, 12, "Your anaconda is very hungry..")

    return scr.getkey()


def game_loop(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    snake = Snake([
        Point(10, 10),
        Point(9, 10),
        Point(8, 10),
        Point(7, 10),
        Point(6, 10),
        ])
    snake.draw(stdscr)
    draw_border(stdscr)

    direction = Direction.RIGHT
    mushroom = create_random_mushroom_on_screen(stdscr)
    mushroom.draw(stdscr)

    mushroom_eaten = 0

    # узнать, почему 3
    curses.halfdelay(3)

    while True:
        action = get_action(stdscr)
        if action == Action.NONE:
            snake.move(direction)
        # elif Action.is_move(action):
        elif action.is_move_my():
            if check_if_direction_is_allowed(action, direction):
                direction = get_direction_from_action(action)
                snake.move(direction)
        elif action == Action.EXIT:
            return "EXIT"
        elif action == Action.CRASH:
            head_point = snake.points[0]
            draw_str(stdscr, head_point.x, head_point.y, 'BAD BOY!')
            stdscr.refresh()
            time.sleep(0.3)
        else:
            raise("Incorrect action: {}!".format(action))

        snake_head = snake.points[0]
        if snake_head == mushroom.point:
            mushroom_eaten += 1
            if mushroom_eaten == MUSHROOMS_TO_WIN:
                return "WIN"
            mushroom = create_random_mushroom_on_screen(stdscr)
            last_index = len(snake.points)-1

            snake.points.append(snake.points[last_index])

        if snake.check_border_collision(width, height):
            return "LOSS"

        if snake.check_self_collision():
            return "LOSS"

        stdscr.clear()
        draw_border(stdscr)
        snake.draw(stdscr)
        mushroom.draw(stdscr)


def main(stdscr):
    curses.curs_set(False)

    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)
    curses.init_pair(5, curses.COLOR_CYAN, -1)

    # creating custom color to make anaconda looks like kolbaska
    # curses.init_color(10, 17, 117, 24)

    while True:
        key = hello_screen(stdscr)
        if key == 'q':
            return

        result = game_loop(stdscr)
        if result == "WIN":
            win_screen(stdscr)
            break
        elif result == "LOSS":
            game_over(stdscr)
            continue
        elif result == "EXIT":
            break
        else:
            raise "Unexpected game_loop result: {}!".format(result)


curses.wrapper(main)
print("Серёжа и Настя котики!")

# написать тесты
