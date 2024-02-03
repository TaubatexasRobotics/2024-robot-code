import ctre
import wpilib


C_LOWER = 0
C_UPPER = 1

SHOOT_SPEED = 0.8
RECEIVE_SPEED = -0.4

class Shooter:
    def __init__(self):
        self.m_lower = ctre.WPI_VictorSPX(C_LOWER)
        self.m_upper = ctre.WPI_VictorSPX(C_UPPER)

        self.motors = wpilib.MotorControllerGroup(self.m_lower, self.m_upper)


        def shoot(self):
            self.motors.set(SHOOT_SPEED)

        def stop(self):
            self.motors.set(0)

        def receive(self):
            self.motors.set(RECEIVE_SPEED)