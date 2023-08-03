import wpilib

JOYSTICK_PORT = 0
LOW_SENSITIVITY_FACTOR = 0.6

A_BUTTON = 1
B_BUTTON = 2
X_BUTTON = 3
Y_BUTTON = 4
LB_BUTTON = 5
RB_BUTTON = 6
SELECT_BUTTON = 7
START_BUTTON = 8
L3_BUTTON = 9
R3_BUTTON = 10

AXIS_LEFT_X = 0
AXIS_LEFT_Y = 1
AXIS_RIGHT_X = 4
AXIS_RIGHT_Y = 5
AXIS_LEFT_TRIGGER = 2 #- XBOX CONTROLLER
AXIS_RIGHT_TRIGGER = 3 #- # XBOX CONTROLLER
# AXIS_LEFT_TRIGGER = 2 - Playstation
# AXIS_RIGHT_TRIGGER = 5

POV_UP = 0
POV_UP_RIGHT = 45
POV_RIGHT = 90
POV_DOWN_RIGHT = 135
POV_DOWN = 180
POV_DOWN_LEFT = 225
POV_LEFT = 270
POV_UP_LEFT = 315



class Controller:
    def __init__(self):
        self.stick = wpilib.Joystick(JOYSTICK_PORT)
        self.low_sensitivity_mode = False
    
    # def toggle_compressor(self):
    #     if self.stick.getRawButtonPressed(SELECT_BUTTON) == True:
    #         return True
    #     return False

    def sensitivity_factor(self):
        if self.low_sensitivity_mode == True:
            return LOW_SENSITIVITY_FACTOR
        return 1.0
    
    def get_drive(self) -> (float, float):
        rt_value = self.stick.getRawAxis(AXIS_RIGHT_TRIGGER)
        lt_value = self.stick.getRawAxis(AXIS_LEFT_TRIGGER)
        combined_value = lt_value - rt_value
        
        forward_speed = combined_value * self.sensitivity_factor()
        rotation_speed = self.stick.getRawAxis(AXIS_LEFT_X) * self.sensitivity_factor()

        return forward_speed , rotation_speed
    
    def decrease_arm_length(self):
        return self.stick.getRawButton(LB_BUTTON)
    
    def increase_arm_length(self):
        return self.stick.getRawButton(RB_BUTTON)
    
    def stop_arm_length(self):
        return self.stick.getRawButtonReleased(LB_BUTTON) or self.stick.getRawButtonReleased(RB_BUTTON)
    
    def move_angle(self):
        return self.stick.getRawAxis(AXIS_RIGHT_Y)
    
    def decrease_arm_angle(self):
        return self.stick.getRawButton(Y_BUTTON)
    
    def increase_arm_angle(self):
        return self.stick.getRawButton(A_BUTTON)
    
    def stop_arm_angle(self):
        return self.stick.getRawButtonReleased(A_BUTTON) or self.stick.getRawButtonReleased(Y_BUTTON)
    
    def catch_gamepiece(self):
        return self.stick.getRawButton(X_BUTTON)
    
    def release_gamepiece(self):
        return self.stick.getRawButton(B_BUTTON)
    
    def stop_intake(self):
        return self.stick.getRawButtonReleased(B_BUTTON) or self.stick.getRawButtonReleased(X_BUTTON)

    def set_angle_and_lenght_position_mid(self):
        return self.stick.getPOV(POV_RIGHT)

    def set_angle_and_lenght_position_comunity(self):
        return self.stick.getPOV(POV_UP)
    
    def set_angle_and_lenght_position_lower(self):
        return self.stick.getPOV(POV_DOWN)
    
    def toggle_low_sensitivity_mode(self):
        return self.stick.getRawButtonPressed(SELECT_BUTTON)
    

    
