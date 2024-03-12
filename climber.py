import phoenix5 as ctre
import wpilib
from controller import Controller

C_LEFT = 1
C_RIGHT = 4

CLIMBER_SPEED = 1

PORT_LOWER_L = 2
PORT_LOWER_R = 3
PORT_UPPER_L = 4
PORT_UPPER_R = 1

class Climber:
    def __init__(self):
        # End Switches
        self.end_lower_l = wpilib.DigitalInput(PORT_LOWER_L)
        self.end_lower_r = wpilib.DigitalInput(PORT_LOWER_R)
        self.end_upper_l = wpilib.DigitalInput(PORT_UPPER_L)
        self.end_upper_r = wpilib.DigitalInput(PORT_UPPER_R)

        self.end_lower_l_value = False
        self.end_lower_r_value = False
        self.end_upper_l_value = False
        self.end_upper_r_value = False        

        self.is_homed = False

        # Motors
        self.m_left = ctre.WPI_VictorSPX(C_LEFT)
        self.m_right = ctre.WPI_VictorSPX(C_RIGHT)
        self.m_right.setInverted(True)

        self.climber_motors = wpilib.MotorControllerGroup(self.m_left, self.m_right)

    def update_dashboard(self, dashboard):
        dashboard.putBoolean("Climber left lower end", self.end_lower_l.get())
        dashboard.putBoolean("Climber right lower", self.end_lower_r.get())
        dashboard.putBoolean("Climber left upper end", self.end_upper_l.get())
        dashboard.putBoolean("Climber right upper end", self.end_upper_r.get())

    def teleop_control(self, controller: Controller):
        if controller.is_held('RB_BUTTON'):
            self.climb_up()
        if controller.is_held('LB_BUTTON'):
            self.climb_down()
        if not controller.are_any_held('RB_BUTTON', 'LB_BUTTON'):
            self.stop()

    def update_end_switches(self):
        self.end_lower_l_value = not self.end_lower_l.get()
        self.end_lower_r_value = not self.end_lower_r.get()
        self.end_upper_l_value = not self.end_upper_l.get()
        self.end_upper_r_value = not self.end_upper_r.get()

    def climb_up(self):
        self.update_end_switches()
        if not self.end_upper_l_value:
            self.m_left.set(CLIMBER_SPEED)
        else:
            self.m_left.set(0)
        
        if not self.end_upper_r_value:
            self.m_right.set(CLIMBER_SPEED)
        else:
            self.m_right.set(0)

    def stop(self):
        self.climber_motors.set(0)

    def climb_down(self):
        self.update_end_switches()
        if not self.end_lower_l_value:
            self.m_left.set(-CLIMBER_SPEED)
        else:
            self.m_left.set(0)
        
        if not self.end_lower_r_value:
            self.m_right.set(-CLIMBER_SPEED)
        else:
            self.m_right.set(0)

    def home(self):
        self.update_end_switches()
        self.climb_down()
        if self.end_lower_l_value and self.end_upper_r_value:
            self.is_homed = True