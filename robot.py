from drivetrain import Drivetrain
from arm import Arm
from intake import Intake
from controller import Controller
from dashboard import Dashboard

import wpilib

AUTONOMOUS_SPEED = 0.4
AUTONOMOUS_DISTANCE = 1

GAMEPIECE_SCORING_DURATION = 5
AUTONOMOUS_MOVEMENT_DURATION = 8
ONLY_DRIVETRAIN_MODE = True

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.controller = Controller()
        self.drivetrain = Drivetrain()
        self.arm = Arm()
        self.intake = Intake()
        self.timer = wpilib.Timer()

        self.smartdashboard = wpilib.SmartDashboard
        self.field = wpilib.Field2d()
        
        leftPosition = self.drivetrain.get_left_distance()
        rightPosition = self.drivetrain.get_right_distance()
        
        self.arm.stop_arm_angle()
        self.arm.stop_arm_lenght()
        
    #update the dashboard
    def robotPeriodic(self) -> None:
        left_distance = self.drivetrain.get_left_distance()
        right_distance = self.drivetrain.get_right_distance()
        
        self.smartdashboard.putNumber("Angle", self.arm.get_angle_position())
        self.smartdashboard.putNumber("Lenght", self.arm.get_length_position())
                
        self.smartdashboard.putNumber("Left Pulses", left_distance)
        self.smartdashboard.putNumber("Left Distance", right_distance)

        self.smartdashboard.putNumber("Right Pulses", self.drivetrain.get_right_encoder_pulses())
        self.smartdashboard.putNumber("Right Distance", self.drivetrain.get_right_distance())
        self.smartdashboard.putNumber("Distance", self.drivetrain.get_distance())
        
        self.smartdashboard.putBoolean("Compressor", self.intake.compressor.isEnabled())
        self.smartdashboard.putNumber("Arfagem", self.drivetrain.get_pitch())
        
        self.smartdashboard.putData("NavX", self.drivetrain.navx)
        
        self.drivetrain.update_odometry()
        self.field.setRobotPose(self.drivetrain.get_pose())
        self.smartdashboard.putData("Field", self.field)
        
    def teleopInit(self) -> None:
        self.drivetrain.differential_drive.setSafetyEnabled(True)

    def teleopPeriodic(self) -> None:
        self.drivetrain.move( *self.controller.get_drive() )
        self.intake.compressor.disable()

        if ONLY_DRIVETRAIN_MODE:
            self.intake.compressor.disable()
            return

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
        self.intake.compressor.disable()
        self.drivetrain.differential_drive.setSafetyEnabled(True)
        self.drivetrain.differential_drive.setExpiration(0.1)
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self) -> None:
        self.arm.stop_arm_angle()
        # if not self.arm.is_homed:
        #     self.arm.home()
        #     return

        if self.drivetrain.get_distance() < AUTONOMOUS_DISTANCE:
            self.drivetrain.move_straight(-AUTONOMOUS_SPEED)        

        if ONLY_DRIVETRAIN_MODE:
            return


if __name__ == "__main__":
    wpilib.run(MyRobot)