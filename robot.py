from drivetrain import Drivetrain
from arm import Arm
from intake import Intake

import wpilib

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.stick = wpilib.Joystick(0)

        self.drivetrain = Drivetrain()
        self.arm = Arm()
        self.intake = Intake()

    def teleopInit(self) -> None:
        self.drivetrain.differential_drive.setSafetyEnabled(True)

    def teleopPeriodic(self) -> None:
        self.drivetrain.differential_drive.arcadeDrive(
            self.stick.getRawAxis(1),
            self.stick.getRawAxis(0),
        )

        if not self.arm.is_homed:
            self.arm.home_arm()
            return

        if self.stick.getRawButtonPressed(7) == True:
            self.intake.toggle_compressor()
        
        if self.stick.getRawButtonPressed(2) == True:
            self.intake.toggle_intake()
        
    def autonomousPeriodic(self) -> None:
        if not self.arm.is_homed:
            self.arm.home_arm()
            return
            
if __name__ == "__main__":
    wpilib.run(MyRobot)