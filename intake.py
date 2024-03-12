import phoenix5 as ctre
import wpilib
from controller import Controller

C_INNER = 12

C_FRONT = 3
C_BACK = 12

PORT_SENSOR_DETECT_NOTE = 0
PORT_LIGHT_DETECT_NOTE = 0

RECIEVE_SPEED = 0.6

class Intake:
    def __init__(self):
        self.m_front = ctre.WPI_VictorSPX(C_BACK)
        self.m_lower = ctre.WPI_VictorSPX(C_FRONT)
        self.detect_note = wpilib.DigitalInput(PORT_SENSOR_DETECT_NOTE)
        self.light_detect_note = wpilib.Relay(PORT_LIGHT_DETECT_NOTE)

        self.motors = wpilib.MotorControllerGroup(self.m_lower, self.m_front)
        self.motors.setInverted(True)

    def update_dashboard(self, dashboard) -> None:
        dashboard.putBoolean("Detect Note", self.detect_note.get())

    def teleop_control(self, controller: Controller) -> None:
        if not self.detect_note.get():
            self.turn_on_light()
        else:
            self.turn_off_light()

        if controller.is_held('Y_BUTTON'):
            self.catch_gamepiece()
        if controller.is_held('A_BUTTON'):
            self.eject_gamepiece()
        if not controller.are_any_held('A_BUTTON', 'Y_BUTTON'):
            self.stop()

    def turn_on_light(self):
        self.light_detect_note.set(wpilib.Relay.Value.kForward)
    
    def turn_off_light(self):
        self.light_detect_note.set(wpilib.Relay.Value.kOff)

    def catch_gamepiece(self):
        self.motors.set(RECIEVE_SPEED)

    def stop(self):
        self.motors.set(0)

    def store_gamepiece(self):
        self.motors.set(RECIEVE_SPEED)

    def eject_gamepiece(self):
        self.motors.set(-RECIEVE_SPEED)
