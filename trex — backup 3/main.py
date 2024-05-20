import keyboard
import mss
import time
import matplotlib.pyplot as plt
import numpy as np
import cv2


## константы
start_distance_trex_detect_obstacles = 140
time_in_jump = 0.7
start_wait_time_after_jump = 0.33

## пути
trex_path = 'images/trex.png'
grey_pixel_path = 'images/grey_pixel.png'
trex_in_jump_path = 'images/trex_in_jump.png'
gameover_path = 'images/gameover.png'

obstacles = {
            'triple_cactus': ['images/triple_cactus.png', 0],
            'double_cactus': ['images/double_cactus.png', 0],
            'cactus': ['images/cactus.png', 0],
            'mini_triple_cactus': ['images/triple_mini_cactus.png', 1],
            'mini_double_cactus': ['images/double_mini_cactus.png', 1],
            'mini_cactus': ['images/mini_cactus.png', 1],
            'pterodactyl': ['images/pterodactyl.png', 0]
        }


def find_obstacle_coordinates(obstacle_path, monitor=None, is_pterodactyl=False, trex_coordinates=None):
        
    obstacle_img = cv2.imread(obstacle_path, cv2.IMREAD_GRAYSCALE)
    if obstacle_img is not None:
        # Захват скриншота с помощью mss
        with mss.mss() as sct:
            # Получение информации о мониторе
            if monitor is None:     
                monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)

            # Преобразование скриншота в OpenCV формат
            screen_shot = np.array(screenshot)
            screen_shot = cv2.cvtColor(screen_shot, cv2.COLOR_BGR2GRAY)

            # Поиск объекта на скриншоте
            result = cv2.matchTemplate(screen_shot, obstacle_img, cv2.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            threshold = 0.99

            if max_val >= threshold:
                # Координаты объекта на скриншоте
                start_x = max_loc[0]
                start_y = max_loc[1]
                end_x = start_x + obstacle_img.shape[1]
                end_y = start_y + obstacle_img.shape[0]
                width = end_x - start_x
                height = obstacle_img.shape[0]

                if (is_pterodactyl):
                    print('eto pterodactyl')
                    if (abs(start_y - trex_coordinates['y1']) > 270):
                        return None

                return {'x1': start_x, 'x2': end_x, 'y1': start_y, 'y2': end_y,
                        'height': height, 'width': width, 'path':obstacle_path}

            else:
                return None




def if_trex_in_jump(trex_top):
    
    trex_coordinates = find_obstacle_coordinates(trex_path)
    current_trex_top = trex_coordinates['top']
    
    return  not(trex_top == current_trex_top)


def calculate_speed(obstacle_coordinates, trex_coordinates, distance_trex_detect_obstacles):
    
    trex_start = trex_coordinates['x1']
    
    left = int(trex_coordinates['x2'])
    top = int(trex_coordinates['y2'] - trex_coordinates['height'] * 2)
    width = int(distance_trex_detect_obstacles)
    height = int(trex_coordinates['height'] * 4)
    monitor = {"top": top, "left": left, "width": width, "height": height}
    
    obstacle_path = obstacle_coordinates['path']
    trex_start = trex_coordinates['x1']
    
    current_obstacle_start = find_obstacle_coordinates(obstacle_path, monitor)['x1']
    distance1 = current_obstacle_start
    time1 = time.time()

    current_obstacle_coordinates = find_obstacle_coordinates(obstacle_path, monitor)
    current_obstacle_start = current_obstacle_coordinates['x1']
    distance2 = current_obstacle_start
    time2 = time.time()
    
    speed = (distance1 - distance2) / (time2 - time1)

    return speed, distance2, current_obstacle_coordinates


def calculate_wait_time_before_jump(obstacle_coordinates, trex_coordinates, time_in_jump, distance_trex_detect_obstacles):
            
    wait_time_before_jump = None
    try:
        speed, distance, obstacle_coordinates = calculate_speed(obstacle_coordinates, trex_coordinates, distance_trex_detect_obstacles)
        distance_before_jump = speed * time_in_jump
    except: 
        wait_time_before_jump = 0 
    
    if wait_time_before_jump is None:
        wait_time_before_jump = (distance + trex_coordinates['width'] - distance_before_jump) / speed
    
    return wait_time_before_jump    
    

def jump(obstacle_coordinates, trex_coordinates, time_in_jump, obstacle, wait_time_after_jump, distance_trex_detect_obstacles):
    
    wait_time_before_jump = calculate_wait_time_before_jump(obstacle_coordinates,
                                                                      trex_coordinates,
                                                                      time_in_jump,
                                                                      distance_trex_detect_obstacles)

    
    if wait_time_before_jump > 0:
        time.sleep(wait_time_before_jump)
        
    keyboard.release('down')
    
    keyboard.press('space')
    
    try:
        speed, distance, obstacle_coordinates = calculate_speed(obstacle_coordinates, trex_coordinates, distance_trex_detect_obstacles)
        wait_time_after_jump += (obstacle_coordinates['width']) / speed
    except:
        wait_time_after_jump = 0
    
    if (obstacles[obstacle][1] == 1 and obstacle != 'triple_mini_cactus'):
        time.sleep(wait_time_after_jump*0.66)
        keyboard.press('down')
        time.sleep(0.01)
        wait_time_after_jump =- 0.01
        keyboard.release('down')

        wait_time_after_jump *= 0.35
    
    if (wait_time_after_jump > 0):
        time.sleep(wait_time_after_jump)

    keyboard.press('down')
    time.sleep(0.1)


def play_trex():
    
    trex_coordinates = find_obstacle_coordinates(trex_path)
        
    print("trex is ready!")

    while True:
        
        keyboard.press('down')
        
        if keyboard.is_pressed('ESC'):
            keyboard.release('down')
            return

        for obstacle in obstacles:
            obstacle_path = obstacles[obstacle][0]
            
            is_pterodactyl = False
            if obstacle == 'pterodactyl':
                is_pterodactyl = True
            
            current_time = time.time()
            duration = current_time - start_time
            
            distance_trex_detect_obstacles  = start_distance_trex_detect_obstacles + duration * 1.3
            
            left = int(trex_coordinates['x2'])
            top = int(trex_coordinates['y2'] - trex_coordinates['height'] * 2)
            width = int(distance_trex_detect_obstacles)
            height = int(trex_coordinates['height'] * 4)
            monitor = {"top": top, "left": left, "width": width, "height": height}

            obstacle_coordinates = find_obstacle_coordinates(obstacle_path, monitor, is_pterodactyl, trex_coordinates)
            
            if obstacle_coordinates:
                if (is_pterodactyl):
                    obstacle_coordinates['width'] = trex_coordinates['width'] * 5
                    
                elif (obstacle == 'mini_cactus'):
                    obstacle_coordinates['width'] *= 0.00001
                    
                elif (obstacle == 'double_mini_cactus'):
                    obstacle_coordinates['width'] *= 0.5
                    
                elif (obstacle == 'cactus'):
                    obstacle_coordinates['width'] *= 1
                    
                elif (obstacle == 'double_cactus'):
                    obstacle_coordinates['width'] *= 0.01
                    
                elif (obstacle == 'mini_cactus'):
                    obstacle_coordinates['width'] *= 0.5
                    
                elif (obstacle == 'triple_cactus'):
                    obstacle_coordinates['width'] *= 45
                    
                elif (obstacle == 'triple_mini_cactus'):
                    obstacle_coordinates['width'] *= 2
                    
                print(f"trex found {obstacle}")
                current_time = time.time()
                duration = current_time - start_time    
            
                wait_time_after_jump = start_wait_time_after_jump - (duration / 2430)
                print(wait_time_after_jump)
                
                jump(obstacle_coordinates, trex_coordinates, time_in_jump, obstacle, wait_time_after_jump, distance_trex_detect_obstacles)
                break


## начало программы
if __name__ == "__main__":
    while True:
        if keyboard.is_pressed('enter'):
            start_time = time.time()
            time.sleep(0.5)
            play_trex()
            break
