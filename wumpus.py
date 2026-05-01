from flask import Flask, send_file, jsonify, request
import random
import threading
import time

app = Flask(__name__)

# Game state variables
grid_rows, grid_cols = 6, 6
player_pos = [0, 0]
pit_locations = set() 
monster_pos = None
treasure_pos = None
explored_cells = set()
safe_cells = set()
risky_cells = set()
logic_count = 0
is_running = False
game_thread = None


def get_adjacent_cells(row, col):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    adjacent = []

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc

        if 0 <= new_row < grid_rows and 0 <= new_col < grid_cols:
            adjacent.append((new_row, new_col))

    return adjacent


def create_world(total_rows, total_cols):
    global grid_rows, grid_cols, player_pos
    global pit_locations, monster_pos, treasure_pos
    global explored_cells, safe_cells, risky_cells
    global logic_count, is_running, game_thread

    # Stop running agent first
    is_running = False

    if game_thread and game_thread.is_alive():
        time.sleep(0.5)

    # Reset game data
    grid_rows, grid_cols = total_rows, total_cols
    player_pos = [0, 0]
    pit_locations = set()
    monster_pos = None
    treasure_pos = None
    explored_cells = {(0, 0)}
    safe_cells = {(0, 0)}
    risky_cells = set()
    logic_count = 0
    is_running = False

    # Random pit generation
    for row in range(grid_rows):
        for col in range(grid_cols):
            if (row, col) != (0, 0) and random.random() < 0.2:
                pit_locations.add((row, col))

    # Random monster placement
    while True:
        random_monster = (
            random.randint(0, grid_rows - 1),
            random.randint(0, grid_cols - 1)
        )

        if random_monster != (0, 0) and random_monster not in pit_locations:
            monster_pos = random_monster
            break

    # Random treasure placement
    while True:
        random_treasure = (
            random.randint(0, grid_rows - 1),
            random.randint(0, grid_cols - 1)
        )

        if (
            random_treasure != (0, 0)
            and random_treasure not in pit_locations
            and random_treasure != monster_pos
        ):
            treasure_pos = random_treasure
            break


def get_percepts(row, col):
    has_breeze = any(cell in pit_locations for cell in get_adjacent_cells(row, col))
    has_stench = any(cell == monster_pos for cell in get_adjacent_cells(row, col))

    return has_breeze, has_stench


def update_knowledge(row, col):
    global logic_count

    has_breeze, has_stench = get_percepts(row, col)
    logic_count += 1

    for cell in get_adjacent_cells(row, col):
        if not has_breeze and not has_stench:
            safe_cells.add(cell)
        else:
            if cell not in safe_cells:
                risky_cells.add(cell)


def select_next_move():
    # Priority 1: safe but unexplored cells
    for cell in safe_cells:
        if cell not in explored_cells:
            return cell

    # Priority 2: neighboring cells not marked risky
    for cell in get_adjacent_cells(player_pos[0], player_pos[1]):
        if cell not in explored_cells and cell not in risky_cells:
            return cell

    return None


def run_agent():
    global player_pos, is_running, logic_count, explored_cells, game_thread

    limit_steps = 100
    current_step = 0

    while is_running and current_step < limit_steps:
        current_step += 1

        row, col = player_pos
        explored_cells.add((row, col))
        update_knowledge(row, col)

        # Treasure found
        if treasure_pos and player_pos[0] == treasure_pos[0] and player_pos[1] == treasure_pos[1]:
            is_running = False
            break

        # Monster reached
        if monster_pos and player_pos[0] == monster_pos[0] and player_pos[1] == monster_pos[1]:
            is_running = False
            break

        next_cell = select_next_move()

        if next_cell:
            player_pos = [next_cell[0], next_cell[1]]
            time.sleep(0.3)
        else:
            is_running = False
            break

    is_running = False


@app.route('/')
def home_page():
    return send_file('index.html')


@app.route('/init', methods=['POST'])
def initialize_game():
    data = request.json
    create_world(data['rows'], data['cols'])

    return jsonify({"status": "ok"})


@app.route('/start', methods=['POST'])
def start_game():
    global is_running, game_thread

    if not is_running:
        is_running = True
        game_thread = threading.Thread(target=run_agent, daemon=True)
        game_thread.start()

    return jsonify({"status": "running"})


@app.route('/stop', methods=['POST'])
def stop_game():
    global is_running

    is_running = False

    return jsonify({"status": "stopped"})


@app.route('/state')
def get_game_state():
    has_breeze, has_stench = get_percepts(player_pos[0], player_pos[1])

    return jsonify({
        "rows": grid_rows,
        "cols": grid_cols,
        "agent": player_pos,
        "visited": list(explored_cells),
        "safe": list(safe_cells),
        "danger": list(risky_cells),
        "pits": list(pit_locations),
        "wumpus": monster_pos,
        "gold": treasure_pos,
        "breeze": has_breeze,
        "stench": has_stench,
        "steps": logic_count,
        "running": is_running
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001)