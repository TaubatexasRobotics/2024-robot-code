import phoenix5 as ctre
import wpilib


C_INNER = 12

C_LOWER = 1
C_UPPER = 2

SHOOT_SPEED = 1
RECEIVE_SPEED = -0.4

class Shooter:
    def __init__(self):
        self.m_lower = ctre.WPI_VictorSPX(C_LOWER)
        self.m_upper = ctre.WPI_VictorSPX(C_UPPER)
        self.m_inner = ctre.WPI_VictorSPX(C_INNER)

        self.motors = wpilib.MotorControllerGroup(self.m_lower, self.m_upper)
        self.motors.setInverted(True)

    def catch_gamepiece(self):
        self.motors.set(RECEIVE_SPEED)

    def release_gamepiece(self):
        self.motors.set(SHOOT_SPEED)

    def store_gamepiece(self):
        self.m_inner.set(SHOOT_SPEED)

    def send_to_shoot(self):
        self.m_inner.set(-SHOOT_SPEED)

    def stop_shooter_feeder(self):
        self.m_inner.set(0)

    def shoot(self):
        self.motors.set(SHOOT_SPEED)

    def stop(self):
        self.motors.set(0)

    def receive(self):
        self.motors.set(RECEIVE_SPEED)