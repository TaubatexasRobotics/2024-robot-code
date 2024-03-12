import wpilib
from joystick_profiles import joysticks
joysticks_profile = 'playstation_dualshock_4'
joystick_map = joysticks[joysticks_profile]

LOW_SENSITIVITY_FACTOR = 0.6

class Controller:
    def __init__(self, joystick_port=0):
        self.stick = wpilib.Joystick(joystick_port)
        self.low_sensitivity_mode = False
        self.joystick_map = joystick_map

    def is_pressed(self, button_name: str) -> bool:
        return self.stick.getRawButtonPressed(joystick_map[button_name])
    
    def is_released(self, button_name: str) -> bool:
        return self.stick.getRawButtonReleased(joystick_map[button_name])
    
    def is_held(self, button_name: str) -> bool:
        return self.stick.getRawButton(joystick_map[button_name])
    
    def are_all_released(self, *button_names: str) -> bool:
        button_states = [self.is_released(button_name) for button_name in button_names]
        return all(button_states)
    
    def are_any_released(self, *button_names: str) -> bool:
        button_states = [self.is_released(button_name) for button_name in button_names]
        return any(button_states)
    
    def are_all_pressed(self, *button_names: str) -> bool:
        button_states = [self.is_pressed(button_name) for button_name in button_names]
        return all(button_states)
    
    def are_any_pressed(self, *button_names: str) -> bool:
        button_states = [self.is_pressed(button_name) for button_name in button_names]
        return any(button_states)
    
    def are_all_held(self, *button_names: str) -> bool:
        button_states = [self.is_held(button_name) for button_name in button_names]
        return all(button_states)

    def are_any_held(self, *button_names: str) -> bool:
        button_states = [self.is_held(button_name) for button_name in button_names]
        return any(button_states)
    
    def axis_value(self, axis_name:str) -> bool:
        axis_value = self.stick.getRawAxis(joystick_map[axis_name])
        return axis_value
    
    def axis_to_digital(self, axis_name: str, threshold: float) -> bool:
        if threshold < 0:
            return self.axis_value(axis_name) < threshold
        return self.axis_value(axis_name) > threshold
    
    def axis_between(self, axis_name: str, lower_threshold: float, upper_threshold: float) -> bool:
        axis_value = self.axis_value(axis_name)
        return axis_value > lower_threshold and axis_value < upper_threshold
    
    
    def sensitivity_factor(self) -> float:
        if self.low_sensitivity_mode == True:
            return LOW_SENSITIVITY_FACTOR
        return 1.0
    
    def get_drive(self) -> tuple[float, float]:
        rt_value = self.axis_value('AXIS_RIGHT_TRIGGER')
        lt_value = self.axis_value('AXIS_LEFT_TRIGGER')
        
        combined_value = lt_value - rt_value

        sensitivity_factor = self.sensitivity_factor()
        
        forward_speed = combined_value * sensitivity_factor
        rotation_speed = self.axis_value('AXIS_LEFT_X') * sensitivity_factor

        return forward_speed , rotation_speed
    
    def toggle_low_sensitivity_mode(self) -> bool:
        self.low_sensitivity_mode = not self.low_sensitivity_mode
