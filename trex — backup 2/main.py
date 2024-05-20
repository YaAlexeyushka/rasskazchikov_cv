import keyboard
import pyautogui
import time
import matplotlib.pyplot as plt


## константы
distance_trex_detect_obstacles = 280
start_wait_time_after_jump = 0.4
time_in_jump = 0.6

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
            'mini_cactus': ['images/mini_cactus.png', 1]
        }


def find_obstacle_coordinates(obstacle_path, region=None):
        
    try:
        objects_list = list(pyautogui.locateAllOnScreen(obstacle_path, confidence=0.95, region=region, grayscale=True))
    except:
        return None
            
    min_x = 100500
    
    for object in objects_list:
        if object[0] < min_x:
            min_x = object[0]
            closest_object = object
    
    closest_object_coordinates = {'left':closest_object[0],
                                  'top':closest_object[1],
                                  'width':closest_object[2],
                                  'height':closest_object[3],
                                  'path':obstacle_path}
    
    return closest_object_coordinates



def if_trex_in_jump(trex_top):
    
    trex_coordinates = find_obstacle_coordinates(trex_path)
    current_trex_top = trex_coordinates['top']
    
    return  not(trex_top == current_trex_top)


def calculate_speed(obstacle_coordinates, trex_coordinates):
    
    trex_start = trex_coordinates['left']
    
    left = int(trex_coordinates['left'] + trex_coordinates['width'])
    top = int(trex_coordinates['top'] - trex_coordinates['height'] * 0.5)
    width = distance_trex_detect_obstacles
    height = int(trex_coordinates['height'] * 4)
    region = (left, top, width, height)
    
    obstacle_path = obstacle_coordinates['path']
    trex_start = trex_coordinates['left']
    
    current_obstacle_start = find_obstacle_coordinates(obstacle_path, region)['left']
    distance1 = current_obstacle_start - trex_start
    time1 = time.time()

    current_obstacle_coordinates = find_obstacle_coordinates(obstacle_path, region)
    current_obstacle_start = current_obstacle_coordinates['left']
    distance2= current_obstacle_start - trex_start
    time2 = time.time()

    speed = (distance1 - distance2) / (time2 - time1)
    print(f"speed is {speed}")

    return speed, distance2, current_obstacle_coordinates


def calculate_wait_time_before_jump(obstacle_coordinates, trex_coordinates, time_in_jump):
        
    obstacle_length = obstacle_coordinates['width']
        
    if ( obstacle_coordinates['left'] - trex_coordinates['left'] + trex_coordinates['width'] < 80 ):
        wait_time_before_jump = 0
        distance_before_jump = distance
        print('emergency!')
    else:
        speed, distance, obstacle_coordinates = calculate_speed(obstacle_coordinates, trex_coordinates)
        #print(obstacle_coordinates['left'] - trex_coordinates['left'] + trex_coordinates['width'])
        distance_before_jump = speed * time_in_jump 
        wait_time_before_jump = (distance + obstacle_length + trex_coordinates['width'] - distance_before_jump) / speed
        
    return wait_time_before_jump


def jump(obstacle_coordinates, trex_coordinates, time_in_jump, wait_time_after_jump, obstacle):
    
    wait_time_before_jump = calculate_wait_time_before_jump(obstacle_coordinates,
                                                                      trex_coordinates,
                                                                      time_in_jump)
    

    if not(obstacles[obstacle][1]):
        wait_time_after_jump += 0.1 
    
    if wait_time_before_jump > 0:
        time.sleep(wait_time_before_jump)
        
    keyboard.release('down')
    keyboard.press('space')
    
    if wait_time_after_jump > 0:
        time.sleep(wait_time_after_jump)

    #keyboard.press('down')



def play_trex():
    
    trex_coordinates = find_obstacle_coordinates(trex_path)
        
    print("trex is ready!")

    while True:
        
        if find_obstacle_coordinates(gameover_path) or keyboard.is_pressed('ESC'):
            return

        for obstacle in obstacles:
            obstacle_path = obstacles[obstacle][0]
                
            left = int(trex_coordinates['left'] + trex_coordinates['width'])
            top = int(trex_coordinates['top'] - trex_coordinates['height'] * 0.5)
            width = distance_trex_detect_obstacles
            height = int(trex_coordinates['height'] * 4)
            region = (left, top, width, height)

            obstacle_coordinates = find_obstacle_coordinates(obstacle_path, region)
            
            if obstacle_coordinates:
                print(f"trex found {obstacle}")
                
                current_time = time.time()
                duration = current_time - start_time
                wait_time_after_jump = start_wait_time_after_jump - (duration / 150)
                
                jump(obstacle_coordinates, trex_coordinates, time_in_jump, wait_time_after_jump, obstacle)
                break


## начало программы
if __name__ == "__main__":
    while True:
        if keyboard.is_pressed('space'):
            start_time = time.time()
            time.sleep(0.5)
            play_trex()
            break
