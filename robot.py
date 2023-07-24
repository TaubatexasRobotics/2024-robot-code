from drivetrain import Drivetrain
from arm import Arm
from pneumatic_intake import PneumaticIntake as Intake
from controller import Controller

import wpilib

AUTONOMOUS_SPEED = 0.4
AUTONOMOUS_DISTANCE = 1

GAMEPIECE_SCORING_DURATION = 5
AUTONOMOUS_MOVEMENT_DURATION = 8
ONLY_DRIVETRAIN_MODE = True

def log_exception(e):
    wpilib.DataLogManager.log(repr(e))

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
        self.arm.stop_arm_length()
        
    #update the dashboard
    def robotPeriodic(self) -> None:
        try:
            left_distance = self.drivetrain.get_left_distance()
            right_distance = self.drivetrain.get_right_distance()
            
            self.smartdashboard.putNumber("Angle", self.arm.get_angle_position())
            self.smartdashboard.putNumber("Length", self.arm.get_length_position())
                    
            left_voltage, right_voltage = self.drivetrain.get_motors_voltage()
            self.smartdashboard.putNumber("Left Pulses", left_distance)
            self.smartdashboard.putNumber("Left Distance", right_distance)
            self.smartdashboard.putNumber("Left Volts", left_voltage)

            self.smartdashboard.putNumber("Right Pulses", self.drivetrain.get_right_encoder_pulses())
            self.smartdashboard.putNumber("Right Distance", self.drivetrain.get_right_distance())
            self.smartdashboard.putNumber("Distance", self.drivetrain.get_distance())
            self.smartdashboard.putNumber("Right Volts", right_voltage)
            
            self.smartdashboard.putNumber("Pitch", self.drivetrain.get_pitch())
            
            self.smartdashboard.putData("NavX", self.drivetrain.navx)
            self.smartdashboard.putData("PID", self.drivetrain.reference_pid_controller)
            
            self.drivetrain.update_odometry()
            self.field.setRobotPose(self.drivetrain.get_pose())
            self.smartdashboard.putData("Field", self.field)
        except BaseException as e:
            log_exception(e)
        
    def teleopInit(self) -> None:
        try:
            self.drivetrain.differential_drive.setSafetyEnabled(True)
        except BaseException as e:
            if ONLY_DRIVETRAIN_MODE:
                self.intake.compressor.disable()

    def teleopPeriodic(self) -> None:
        try:
            self.drivetrain.move( *self.controller.get_drive() )
        except BaseException as e: 
            log_exception(e)
        
        try:
            if ONLY_DRIVETRAIN_MODE:
                return

            if self.controller.toggle_compressor():
                self.intake.toggle_compressor()
            if self.controller.toggle_intake():
                self.intake.toggle()
            if self.controller.decrease_arm_length():
                self.arm.decrease_arm_length()

            if self.controller.increase_arm_length():
                self.arm.increase_arm_length()
            if self.controller.stop_arm_length():
                self.arm.stop_arm_length()

            if self.controller.decrease_arm_angle():
                self.arm.decrease_arm_angle()
            if self.controller.increase_arm_angle():
                self.arm.increase_arm_angle()

            if self.controller.stop_arm_angle():
                self.arm.stop_arm_angle()
        except BaseException as e: 
            log_exception(e)
        
    def autonomousInit(self) -> None:
        try:
            self.intake.compressor.disable()
            self.drivetrain.differential_drive.setSafetyEnabled(True)
            self.drivetrain.differential_drive.setExpiration(0.1)
            self.timer.reset()
            self.timer.start()
            
            if ONLY_DRIVETRAIN_MODE:
                self.intake.compressor.disable()
        except BaseException as e:
            log_exception(e)
    def autonomousPeriodic(self) -> None:
        try:
            if self.drivetrain.get_distance() < AUTONOMOUS_DISTANCE:
                self.drivetrain.move_straight(-AUTONOMOUS_SPEED)

            if ONLY_DRIVETRAIN_MODE:
                return
        except BaseException as e:
            log_exception(e)
        
        try:
            self.arm.stop_arm_angle()
            # if not self.arm.is_homed:
            #     self.arm.home()
            #     return
        except BaseException as e:
            log_exception(e)


if __name__ == "__main__":
    wpilib.run(MyRobot)