from drivetrain import Drivetrain
from arm import Arm
from intake import Intake
from controller import Controller

import wpilib

AUTONOMOUS_SPEED = 0.5

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.controller = Controller()
        self.drivetrain = Drivetrain()
        self.arm = Arm()
        self.intake = Intake()
        self.timer = wpilib.Timer()

    def teleopInit(self) -> None:
        self.drivetrain.differential_drive.setSafetyEnabled(True)

    def teleopPeriodic(self) -> None:
        self.drivetrain.move( *self.controller.get_drive() )

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

        if self.controller.decrease_arm_angle():
            self.arm.decrease_arm_angle()

        if self.controller.increase_arm_angle():
            self.arm.increase_arm_angle()

        if self.controller.stop_arm_angle():
            self.arm.stop_arm_angle()
        
    def autonomousInit(self) -> None:
        self.drivetrain.differential_drive.setSafetyEnabled(True)
        self.drivetrain.differential_drive.setExpiration(0.1)
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self) -> None:
        # if not self.arm.is_homed:
        #     self.arm.home()
        #     return

        self.drivetrain.move_straight(AUTONOMOUS_SPEED)
        if self.timer.get() > 5.0 and self.timer.get() < 7:
            self.drivetrain.move_straight(-AUTONOMOUS_SPEED)
        elif self.timer.get() > 7:
            self.drivetrain.stop(0, 0)
            
if __name__ == "__main__":
    wpilib.run(MyRobot)