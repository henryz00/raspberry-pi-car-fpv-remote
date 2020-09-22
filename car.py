import threading

import motor
import ranging

avoid_obst = True

# ------- motor -------

def move(direction, speed):
    thread = threading.Thread(target=move_motor, args=(direction, int(speed)))
    thread.start()

def move_motor(direction, speed):
    print("Motor Signaled: " + direction)
    if direction == "forward":
        if not avoid_obst or (avoid_obst and range > 15) :
            motor.t_up(speed, 6)
        else:
            motor.buzz()
    elif direction == "backward":
        motor.t_down(speed, 6)
    elif direction == "left":
        motor.t_left(40, 1)
    elif direction == "right":
        motor.t_right(40, 1)
    elif direction == "buzz":
        motor.buzz()
    else:
        motor.t_stop(1)

# ------- ranging -------

def set_interval(func, sec):
    # ref https://stackoverflow.com/questions/2697039/
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def get_us_range():
    global range, left, right
    range = ranging.us_distance()
    left = ranging.ir_left()
    right = ranging.ir_right()
    if avoid_obst and range < 15 :
      motor.t_stop(1)
    # print("US - %s, Left - %s, Right - %s" % (range, left, right))
    return range


# ------- setup -------

def setup():
    motor.setup()
    ranging.setup()
    set_interval(get_us_range, 0.1)
