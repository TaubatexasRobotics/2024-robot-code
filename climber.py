import phoenix5 as ctre
import wpilib

C_LEFT = 3
C_RIGHT = 4

CLIMBER_SPEED = 1

class Climber:
    def __init__(self):
        self.m_left = ctre.WPI_VictorSPX(C_LEFT)
        self.m_right = ctre.WPI_VictorSPX(C_RIGHT)

        self.climber_motors = wpilib.MotorControllerGroup(self.m_left, self.m_right)

    def climb_up(self):
        self.climber_motors.set(CLIMBER_SPEED)

    def stop(self):
        self.climber_motors.set(0)

    def climb_down(self):
        self.climber_motors.set(-CLIMBER_SPEED)