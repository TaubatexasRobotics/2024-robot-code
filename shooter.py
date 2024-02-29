import phoenix5 as ctre
import wpilib
from controller import Controller

C_INNER = 12

C_LOWER = 1
C_UPPER = 2

PORT_SENSOR_DETECT_NOTE = 0
PORT_LIGHT_DETECT_NOTE = 0

SHOOT_SPEED = 1
RECEIVE_SPEED = -0.4

class Shooter:
    def __init__(self):
        self.m_lower = ctre.WPI_VictorSPX(C_LOWER)
        self.m_upper = ctre.WPI_VictorSPX(C_UPPER)
        self.m_feeder = ctre.WPI_VictorSPX(C_INNER)
        self.detect_note = wpilib.DigitalInput(PORT_SENSOR_DETECT_NOTE)
        self.light_detect_note = wpilib.Relay(PORT_LIGHT_DETECT_NOTE)

        self.motors = wpilib.MotorControllerGroup(self.m_lower, self.m_upper)
        self.motors.setInverted(True)

    def update_dashboard(self, dashboard) -> None:
        dashboard.putBoolean("Detect Note", self.detect_note.get())

    def teleop_control(self, controller: Controller) -> None:
        if not self.detect_note.get():
            self.turn_on_light()
        else:
            self.turn_off_light()

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

    def turn_on_light(self):
        self.light_detect_note.set(wpilib.Relay.Value.kForward)
    
    def turn_off_light(self):
        self.light_detect_note.set(wpilib.Relay.Value.kOff)

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