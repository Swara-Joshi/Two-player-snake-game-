import socket
from ast import literal_eval
import heapq
import time
import random

HOST = '0.0.0.0'
PORT = 5002
WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def predict_opponent_next(yx1, yy1, yx2, yy2):
    dx, dy = yx2 - yx1, yy2 - yy1
    if dx > 0: return yx2 + SEG_SIZE, yy2, "Right"
    if dx < 0: return yx2 - SEG_SIZE, yy2, "Left"
    if dy > 0: return yx2, yy2 + SEG_SIZE, "Down"
    if dy < 0: return yx2, yy2 - SEG_SIZE, "Up"
    return yx2, yy2, "Straight"

def a_star(start_x, start_y, prev_x, prev_y, goal_x, goal_y, max_iterations=1000):
    directions = {"Up": (0, -SEG_SIZE), "Down": (0, SEG_SIZE), "Left": (-SEG_SIZE, 0), "Right": (SEG_SIZE, 0)}
    open_set = [(manhattan_distance(start_x, start_y, goal_x, goal_y), 0, start_x, start_y, None, [])]
    closed_set = set()
    iterations = 0

    while open_set and iterations < max_iterations:
        f_score, g_score, x, y, _, path = heapq.heappop(open_set)
        
        if (x, y) == (goal_x, goal_y):
            first_direction = path[0] if path else "Straight"
            next_x = start_x + directions.get(first_direction, (0, 0))[0]
            next_y = start_y + directions.get(first_direction, (0, 0))[1]
            if 0 <= next_x < WIDTH and 0 <= next_y < HEIGHT:
                return first_direction
            continue
            
        if (x, y) in closed_set:
            continue
            
        closed_set.add((x, y))
        
        for dir_name, (dx, dy) in directions.items():
            next_x, next_y = x + dx, y + dy
            if (next_x < 0 or next_x >= WIDTH or next_y < 0 or next_y >= HEIGHT or
                (next_x == prev_x and next_y == prev_y)):
                continue
                
            new_g = g_score + 1
            new_h = manhattan_distance(next_x, next_y, goal_x, goal_y)
            new_f = new_g + new_h
            new_path = path + [dir_name]
            
            heapq.heappush(open_set, (new_f, new_g, next_x, next_y, dir_name, new_path))
        
        iterations += 1
    
    safe_directions = []
    for dir_name, (dx, dy) in directions.items():
        next_x, next_y = start_x + dx, start_y + dy
        if (0 <= next_x < WIDTH and 0 <= next_y < HEIGHT and
            (next_x != prev_x or next_y != prev_y)):
            safe_directions.append(dir_name)
    
    return safe_directions[0] if safe_directions else "Straight"

def stay_inside(start_x, start_y, direction):
    directions = {"Up": (0, -SEG_SIZE), "Down": (0, SEG_SIZE), "Left": (-SEG_SIZE, 0), "Right": (SEG_SIZE, 0)}
    next_x = start_x + directions.get(direction, (0, 0))[0]
    next_y = start_y + directions.get(direction, (0, 0))[1]
    
    if not (0 <= next_x < WIDTH and 0 <= next_y < HEIGHT):
        if start_x >= WIDTH - SEG_SIZE: return "Left"
        if start_x <= 0: return "Right"
        if start_y >= HEIGHT - SEG_SIZE: return "Up"
        if start_y <= 0: return "Down"
    
    return direction

# Track previous directions to detect oscillation
last_directions = []
oscillation_counter = 0
last_apple_pos = (-1, -1)
post_apple_cooldown = 0
fixed_post_apple_direction = None

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Red Snake Server listening on {HOST}:{PORT}")
    
    last_direction = "Right"
    direction_stability = 0
    
    while True:
        client_sock, client_addr = s.accept()
        print('New connection from', client_addr)
        
        try:
            while True:
                start_time = time.time()
                data = client_sock.recv(1024)
                
                if not data:
                    break
                    
                yx1, yy1, yx2, yy2, rx1, ry1, rx2, ry2, ax, ay = literal_eval(data.decode())
                ate_apple = (rx2 == ax and ry2 == ay)
                
                red_dist = manhattan_distance(rx2, ry2, ax, ay)
                yellow_dist = manhattan_distance(yx2, yy2, ax, ay)
                
                yx_next, yy_next, yellow_dir = predict_opponent_next(yx1, yy1, yx2, yy2)
                
                # Check if apple position has changed
                current_apple_pos = (ax, ay)
                if current_apple_pos != last_apple_pos:
                    # Reset oscillation detection when apple changes
                    oscillation_counter = 0
                    last_directions = []
                    last_apple_pos = current_apple_pos
                    post_apple_cooldown = 0
                    fixed_post_apple_direction = None
                
                # Detect oscillation pattern
                if len(last_directions) >= 4:
                    if (last_directions[-1] == last_directions[-3] and 
                        last_directions[-2] == last_directions[-4] and
                        last_directions[-1] != last_directions[-2]):
                        oscillation_counter += 1
                    else:
                        oscillation_counter = 0
                
                # Modified strategy to break oscillation and handle apple eating
                if ate_apple:
                    # Just ate an apple, choose a safe direction to continue moving
                    # and stick with it for several moves
                    possible_dirs = ["Up", "Down", "Left", "Right"]
                    # Remove opposite of last direction to avoid going backward
                    if last_direction == "Up": possible_dirs.remove("Down")
                    elif last_direction == "Down": possible_dirs.remove("Up")
                    elif last_direction == "Left": possible_dirs.remove("Right")
                    elif last_direction == "Right": possible_dirs.remove("Left")
                    
                    # Choose a direction that keeps us inside the game area
                    valid_dirs = []
                    for d in possible_dirs:
                        if stay_inside(rx2, ry2, d) == d:
                            valid_dirs.append(d)
                    
                    if valid_dirs:
                        fixed_post_apple_direction = random.choice(valid_dirs)
                    else:
                        fixed_post_apple_direction = random.choice(possible_dirs)
                    
                    direction = fixed_post_apple_direction
                    post_apple_cooldown = 5  # Stay in this direction for 5 moves
                    print(f"Red ate apple, continuing with fixed direction: {direction} for {post_apple_cooldown} moves")
                elif post_apple_cooldown > 0:
                    # Continue in the fixed direction after eating an apple
                    direction = fixed_post_apple_direction
                    post_apple_cooldown -= 1
                    print(f"Red post-apple cooldown: {post_apple_cooldown}, direction: {direction}")
                elif red_dist <= SEG_SIZE:
                    # Very close to apple, go for it regardless of yellow's position
                    direction = a_star(rx2, ry2, rx1, ry1, ax, ay)
                elif oscillation_counter > 2:
                    # Break oscillation with random movement
                    possible_dirs = ["Up", "Down", "Left", "Right"]
                    # Remove opposite of last direction to avoid going backward
                    if last_direction == "Up": possible_dirs.remove("Down")
                    elif last_direction == "Down": possible_dirs.remove("Up")
                    elif last_direction == "Left": possible_dirs.remove("Right")
                    elif last_direction == "Right": possible_dirs.remove("Left")
                    
                    # Choose random direction with larger offset
                    direction = random.choice(possible_dirs)
                    oscillation_counter = 0
                    print("Breaking oscillation with random direction:", direction)
                else:
                    if red_dist < yellow_dist:
                        # Red is closer to apple, go for it
                        direction = a_star(rx2, ry2, rx1, ry1, ax, ay)
                    else:
                        # Apple is closer to yellow, do not move
                        direction = "Straight"
                
                # Keep track of directions for oscillation detection
                if direction != "Straight":
                    last_directions.append(direction)
                    if len(last_directions) > 10:
                        last_directions.pop(0)
                
                direction = stay_inside(rx2, ry2, direction)
                last_direction = direction if direction != "Straight" else last_direction
                
                # Ensure proper growth response format
                response = f"Grow:{direction}" if ate_apple else direction
                client_sock.sendall(response.encode())
                
                print(f"Red: ate={ate_apple}, red_dist={red_dist}, yellow_dist={yellow_dist}, dir={direction}")
                
                if time.time() - start_time > 1:
                    print("Warning: Red response took too long!")
                    
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_sock.close()
