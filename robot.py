from drivetrain import Drivetrain
from arm import Arm

import wpilib

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.stick = wpilib.Joystick(0)

        self.drivetrain = Drivetrain()
        self.arm = Arm()

    def teleopInit(self):
        self.drivetrain.differential_drive.setSafetyEnabled(True)

    def teleopPeriodic(self):
        self.drivetrain.differential_drive.arcadeDrive(
            self.stick.getRawAxis(1),
            self.stick.getRawAxis(0),
            True
        )
    
if __name__ == "__main__":
    wpilib.run(MyRobot)