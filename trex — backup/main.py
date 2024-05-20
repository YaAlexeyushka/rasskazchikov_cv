import numpy as np
import cv2
import mss
import keyboard
import time

## константы
distance_trex_detect_obstacles = 300
trex_path = 'images/trex.png'
grey_pixel_path = 'images/grey_pixel.png'
trex_in_jump_path = 'images/trex_in_jump.png'


def find_obstacle_coordinates(obstacle_path, trex_end_x=0, is_trex=False, search_range=None, y_search_range=None):
    # Загрузка шаблона объекта
    obstacle_img = cv2.imread(obstacle_path, cv2.IMREAD_GRAYSCALE)
    if obstacle_img is not None:
        # Захват скриншота с помощью mss
        with mss.mss() as sct:
            # Получение информации о мониторе
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)

            # Преобразование скриншота в OpenCV формат
            screen_shot = np.array(screenshot)
            screen_shot = cv2.cvtColor(screen_shot, cv2.COLOR_BGR2GRAY)

            # Определение границ поиска по x
            start_x = None
            if search_range is not None:
                start_x, end_x = search_range
                screen_shot = screen_shot[:, start_x:end_x]
                cv2.show(screen_shot)

            # Определение границ поиска по y
            start_y = None
            if y_search_range is not None:
                start_y, end_y = y_search_range
                screen_shot = screen_shot[start_y:end_y, :]

            # Поиск объекта на скриншоте
            result = cv2.matchTemplate(screen_shot, obstacle_img, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            threshold = 0.8

            if max_val >= threshold:
                # Координаты объекта на скриншоте
                if start_x is None and start_y is None:
                    abs_max_loc = max_loc
                elif start_y is None:
                    abs_max_loc = (max_loc[0] + start_x, max_loc[1])
                elif start_x is None:
                    abs_max_loc = (max_loc[0], max_loc[1] + start_y)
                else:
                    abs_max_loc = (max_loc[0] + start_x, max_loc[1] + start_y)

                start_x = abs_max_loc[0]
                start_y = abs_max_loc[1]
                end_x = start_x + obstacle_img.shape[1]
                end_y = start_y + obstacle_img.shape[0]
                length = end_x - start_x
                height = obstacle_img.shape[0]
                distance = start_x - trex_end_x

                if (distance <= 0 or distance > distance_trex_detect_obstacles) and not is_trex:
                    return None

                return {'x1': start_x, 'x2': end_x, 'y1': start_y, 'y2': end_y,
                        'height': height, 'length': length, 'distance': distance}

            else:
                return None


def if_trex_in_jump(trex_start_y):
    trex_coordinates = find_obstacle_coordinates(trex_path, 0, True)
    current_start_y = trex_coordinates['y1']
    
    return  not(trex_start_y == current_start_y)


def calculate_speed(obstacle, trex_end_x):
    obstacle_path = obstacle[0]
    distance1 = find_obstacle_coordinates(obstacle_path, trex_end_x)['distance']
    time1 = time.time()

    time.sleep(0.0001)

    coordinates = find_obstacle_coordinates(obstacle_path, trex_end_x)
    time2 = time.time()
    distance2 = coordinates['distance']

    speed = (distance1 - distance2) / (time2 - time1)
    print(f"speed is {speed}")

    return speed, distance2, coordinates

def calculate_wait_time(obstacle, trex_coordinates, time_in_jump):
    speed, distance, obstacle_coordinates = calculate_speed(obstacle, trex_coordinates['x2'])

    obstacle_length = obstacle_coordinates['length']

    distance_before_jump = speed * time_in_jump

    wait_time_before_jump = (distance + obstacle_length + trex_coordinates['length'] - distance_before_jump) / speed

    wait_time_after_jump = distance_before_jump / speed

    return wait_time_before_jump, wait_time_after_jump

def jump(obstacle, trex_coordinates, time_in_jump):
    wait_time_before_jump, wait_time_after_jump = calculate_wait_time(obstacle, trex_coordinates, time_in_jump)

    keyboard.release('down')

    if wait_time_before_jump > 0:
        time.sleep(wait_time_before_jump)

    keyboard.press('space')

    time.sleep(wait_time_after_jump)

    keyboard.press('down')

def play_trex():
    print("trex is ready!")

    trex_coordinates = find_obstacle_coordinates(trex_path, 0, True)
    trex_start_y = trex_coordinates['y1']
    trex_in_jump = False

    time_in_jump = 0.35

    while True:
        while if_trex_in_jump(trex_start_y):
            pass

        gameover_path = 'images/gameover.png'
        if find_obstacle_coordinates(gameover_path) or keyboard.is_pressed('ESC'):
            return

        trex_coordinates = find_obstacle_coordinates(trex_path, 0, True)

        obstacles = {
            'triple_cactus': ['images/triple_cactus.png'],
            'double_cactus': ['images/double_cactus.png'],
            'cactus': ['images/cactus.png'],
            'mini_triple_cactus': ['images/triple_mini_cactus.png'],
            'mini_double_cactus': ['images/double_mini_cactus.png'],
            'mini_cactus': ['images/mini_cactus.png']
        }

        for obstacle in obstacles:
            obstacle_path = obstacles[obstacle][0]

            obstacles[obstacle].append(find_obstacle_coordinates(obstacle_path, trex_coordinates['x2']))

            if obstacles[obstacle][1]:
                print(f"trex found {obstacle}, its start {obstacles[obstacle][1]}")
                jump(obstacles[obstacle], trex_coordinates, time_in_jump)
                break

## начало программы
if __name__ == "__main__":
    while True:
        if keyboard.is_pressed('space'):
            time.sleep(1)
            play_trex()
            break
