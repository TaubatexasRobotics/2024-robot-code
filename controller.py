import wpilib

JOYSTICK_PORT = 0

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
# AXIS_LEFT_TRIGGER = 2 - XBOX CONTROLLER
# AXIS_RIGHT_TRIGGER = 3 - XBOX CONTROLLER
AXIS_LEFT_TRIGGER = 2
AXIS_RIGHT_TRIGGER = 5

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
    
    def toggle_compressor(self):
        if self.stick.getRawButtonPressed(SELECT_BUTTON) == True:
            return True
        return False
    
    def get_drive(self) -> (float, float):
        rt_value = self.stick.getRawAxis(AXIS_RIGHT_TRIGGER)
        lt_value = self.stick.getRawAxis(AXIS_LEFT_TRIGGER)
        combined_value = lt_value - rt_value

        return self.stick.getRawAxis(5), self.stick.getRawAxis(AXIS_LEFT_X)
    
    def decrease_arm_length(self):
        return self.stick.getRawButton(LB_BUTTON)
    
    def increase_arm_length(self):
        return self.stick.getRawButton(RB_BUTTON)
    
    def stop_arm_length(self):
        return self.stick.getRawButtonReleased(LB_BUTTON) or self.stick.getRawButtonReleased(RB_BUTTON)
    
    def move_angle(self):
        return self.stick.getRawAxis(AXIS_RIGHT_Y)
    
    def decrease_arm_angle(self):
        return self.stick.getRawButton(A_BUTTON)
    
    def increase_arm_angle(self):
        return self.stick.getRawButton(Y_BUTTON)
    
    def stop_arm_angle(self):
        return self.stick.getRawButtonReleased(A_BUTTON) or self.stick.getRawButtonReleased(Y_BUTTON)
    
    def catch_gamepiece(self):
        return self.stick.getRawButton(B_BUTTON)
    
    def release_gamepiece(self):
        return self.stick.getRawButton(X_BUTTON)
    
    def stop_intake(self):
        return self.stick.getRawButtonReleased(B_BUTTON) or self.stick.getRawButtonReleased(X_BUTTON)

