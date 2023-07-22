import time


# import robot
# robot = robot()
# robot.left(speed=0.3)
# time.sleep(0.5)
# robot.stop()

from robot import Robot

robot = Robot()
# robot.left(speed=0.15)
# time.sleep(1)
# robot.right(speed=0.15)
# time.sleep(1)
robot.forward(speed=0.1)
time.sleep(0.5)

# for i in range(0.5, 0, -0.05):
#     robot.forward(speed=i)
#     time.sleep(0.15)


# start = 0.5
# end = 0
# step = -0.05

# i = start
# while i >= end:
#     # Ýþlem yapmak istediðiniz kod buraya gelecek
#     robot.forward(speed=i)  # Sadece deðeri yazdýrmak için örnek bir iþlem
#     time.sleep(0.15)
#     i += step    
robot.stop()