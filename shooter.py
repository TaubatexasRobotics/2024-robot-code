import phoenix5 as ctre
import wpilib
from controller import Controller

C_LOWER = 1
C_UPPER = 2

SHOOT_SPEED = 1

class Shooter:
    def __init__(self):
        self.m_lower = ctre.WPI_VictorSPX(C_LOWER)
        self.m_upper = ctre.WPI_VictorSPX(C_UPPER)

        self.motors = wpilib.MotorControllerGroup(self.m_lower, self.m_upper)
        self.motors.setInverted(True)

    def update_dashboard(self, dashboard) -> None:
        dashboard.putBoolean("Detect Note", self.detect_note.get())

    def teleop_control(self, controller: Controller) -> None:
        # if not self.detect_note.get():
        #     self.turn_on_light()
        # else:
        #     self.turn_off_light()

        if controller.is_held('X_BUTTON'):
            self.eject()
        if controller.is_held('B_BUTTON'):
            self.shoot()
        if not controller.are_any_held('X_BUTTON', 'B_BUTTON'):
            self.stop_shooter()

    def shoot(self):
        self.motors.set(SHOOT_SPEED)

    def stop_shooter(self):
        self.motors.set(0)

    def eject(self):
        self.motors.set(-SHOOT_SPEED)