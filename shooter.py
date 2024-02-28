import phoenix5 as ctre
import wpilib
from controller import Controller

C_INNER = 12

C_LOWER = 1
C_UPPER = 2

SHOOT_SPEED = 1
RECEIVE_SPEED = -0.4

class Shooter:
    def __init__(self):
        self.m_lower = ctre.WPI_VictorSPX(C_LOWER)
        self.m_upper = ctre.WPI_VictorSPX(C_UPPER)
        self.m_feeder = ctre.WPI_VictorSPX(C_INNER)

        self.motors = wpilib.MotorControllerGroup(self.m_lower, self.m_upper)
        self.motors.setInverted(True)

    def update_dashboard(self, dashboard) -> None:
        pass

    def teleop_control(self, controller: Controller) -> None:
        if controller.is_held('X_BUTTON'):
            self.catch_gamepiece()
        if controller.is_held('B_BUTTON'):
            self.shoot()
        if not controller.are_any_held('X_BUTTON', 'B_BUTTON'):
            self.stop_shooter()
        if controller.axis_to_digital('AXIS_RIGHT_X', -0.2):
            self.store_gamepiece()
        if controller.axis_to_digital('AXIS_RIGHT_X', 0.2):
            self.send_to_shoot()
        if controller.axis_between('AXIS_RIGHT_X', -0.2, 0.2):
            self.stop_shooter_feeder()

    def catch_gamepiece(self):
        self.motors.set(RECEIVE_SPEED)

    def store_gamepiece(self):
        self.m_feeder.set(SHOOT_SPEED)

    def send_to_shoot(self):
        self.m_feeder.set(-SHOOT_SPEED)

    def stop_shooter_feeder(self):
        self.m_feeder.set(0)

    def shoot(self):
        self.motors.set(SHOOT_SPEED)

    def stop_shooter(self):
        self.motors.set(0)