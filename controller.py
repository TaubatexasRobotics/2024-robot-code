import wpilib
from joystick_profiles import joysticks
joysticks_profile = 'xbox_controller'
controller = joysticks[joysticks_profile]

JOYSTICK_PORT = 0
LOW_SENSITIVITY_FACTOR = 0.6

class Controller:
    def __init__(self):
        self.stick = wpilib.Joystick(JOYSTICK_PORT)
        self.low_sensitivity_mode = False
    
    def sensitivity_factor(self) -> float:
        if self.low_sensitivity_mode == True:
            return LOW_SENSITIVITY_FACTOR
        return 1.0
    
    def get_drive(self) -> tuple[float, float]:
        rt_value = self.stick.getRawAxis(controller['AXIS_RIGHT_TRIGGER'])
        lt_value = self.stick.getRawAxis(controller['AXIS_LEFT_TRIGGER'])
        combined_value = lt_value - rt_value
        
        forward_speed = combined_value * self.sensitivity_factor()
        rotation_speed = self.stick.getRawAxis(controller['AXIS_LEFT_X']) * self.sensitivity_factor()

        return forward_speed , rotation_speed
    
    def move_angle(self) -> float:
        return self.stick.getRawAxis(controller['AXIS_RIGHT_Y'])
    
    def decrease_arm_angle(self) -> bool:
        return self.stick.getRawButton(controller['Y_BUTTON'])
    
    def increase_arm_angle(self) -> bool:
        return self.stick.getRawButton(controller['A_BUTTON'])
    
    def stop_arm_angle(self) -> bool:
        return self.stick.getRawButtonReleased(controller['A_BUTTON']) or self.stick.getRawButtonReleased(controller['Y_BUTTON'])
    
    def catch_gamepiece(self) -> bool:
        return self.stick.getRawButton(controller['X_BUTTON'])
    
    def store_gamepiece(self) -> bool:
        return self.stick.getRawAxis(controller['AXIS_RIGHT_X']) < -0.2
    
    def send_to_shoot(self) -> bool:
        print(self.stick.getRawAxis(controller['AXIS_RIGHT_X']) > 0.2)
        return self.stick.getRawAxis(controller['AXIS_RIGHT_X']) > 0.2
    
    def release_gamepiece(self) -> bool:
        return self.stick.getRawButton(controller['B_BUTTON'])
    
    def stop_intake(self) -> bool:
        return self.stick.getRawButtonReleased(controller['B_BUTTON']) or self.stick.getRawButtonReleased(controller['X_BUTTON'])

    def sensitivity_toggle_button(self) -> bool:
        return self.stick.getRawButtonPressed(controller['SELECT_BUTTON'])
    
    def toggle_low_sensitivity_mode(self) -> bool:
        self.low_sensitivity_mode = not self.low_sensitivity_mode

    def climb_up(self) -> bool:
        return self.stick.getRawButton(controller['RB_BUTTON'])

    def climb_down(self) -> bool:
        return self.stick.getRawButton(controller['LB_BUTTON'])
    
