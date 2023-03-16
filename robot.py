from drivetrain import Drivetrain
from arm import Arm
from intake import Intake
from controller import Controller

import wpilib

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.controller = Controller()
        self.drivetrain = Drivetrain()
        self.arm = Arm()
        self.intake = Intake()

    def teleopInit(self) -> None:
        self.drivetrain.differential_drive.setSafetyEnabled(True)

    def teleopPeriodic(self) -> None:
        self.drivetrain.differential_drive.arcadeDrive( *self.controller.get_drive() )

        # if not self.arm.is_homed:
        #     self.arm.home()
        #     return

        if self.controller.toggle_compressor():
            self.intake.toggle_compressor()
        
        if self.controller.toggle_intake():
            self.intake.toggle()
        
        if self.controller.decrease_arm_lenght():
            self.arm.decrease_arm_lenght()

        if self.controller.increase_arm_lenght():
            self.arm.increase_arm_lenght()

        if self.controller.stop_arm_lenght():
            self.arm.stop_arm_lenght()
        
    def autonomousPeriodic(self) -> None:
        if not self.arm.is_homed:
            self.arm.home()
            return
            
if __name__ == "__main__":
    wpilib.run(MyRobot)