from drivetrain import Drivetrain
from arm import Arm
from climber import Climber
from controller import Controller
from shooter import Shooter

import wpilib

AUTONOMOUS_SPEED = 0.65
AUTONOMOUS_DISTANCE = -2.4
AUTONOMOUS_MAX_DISTANCE =-3

GAMEPIECE_SCORING_DURATION = 5
AUTONOMOUS_MOVEMENT_DURATION = 8
ONLY_DRIVETRAIN_MODE = False

SHORT_LINE_DISTANCE = -1.87
LONG_LINE_DISTANCE = -3.42
INITIAL_GAMEPIECES_DISTANCE = -5.69
MIDDLE_LINE_DISTANCE = -7.24

def log_exception(e):
    wpilib.DataLogManager.log(repr(e))

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.controller = Controller()
        self.drivetrain = Drivetrain()
        self.arm = Arm()
        self.shooter = Shooter()
        self.climber = Climber()
        self.mechanisms = [self.drivetrain, self.arm, self.shooter, self.climber]
        self.timer = wpilib.Timer()

        self.task_count = 0
        # self.high_angle = 1

        self.high_angle = -11.404823303222656

        self.mid_angle = -12.38
        self.low_angle = -2.098
        wpilib.CameraServer.launch()

        self.smartdashboard = wpilib.SmartDashboard
        self.field = wpilib.Field2d()
        
        leftPosition = self.drivetrain.get_left_distance()
        rightPosition = self.drivetrain.get_right_distance()
        
        self.arm.stop_arm_angle()

        self.smartdashboard.putNumber("Mid Angle", self.mid_angle)
        self.smartdashboard.putNumber("Comunity Angle", self.high_angle)
        self.smartdashboard.putNumber("Low Angle", self.low_angle)
        
    #update the dashboard
    def robotPeriodic(self) -> None:
        try:
            left_distance = self.drivetrain.get_left_distance()
            right_distance = self.drivetrain.get_right_distance()
            
            self.smartdashboard.putNumber("Angle", self.arm.get_angle_position())
                    
            left_voltage, right_voltage = self.drivetrain.get_motors_voltage()
            self.smartdashboard.putNumber("Left Pulses", left_distance)
            self.smartdashboard.putNumber("Left Distance", right_distance)
            self.smartdashboard.putNumber("Left Volts", left_voltage)

            self.smartdashboard.putBoolean("Climber left end", self.climber.end_lower_l_value)
            self.smartdashboard.putBoolean("Climber right end", self.climber.end_lower_r_value)
            self.smartdashboard.putBoolean("Climber left upper end", self.climber.end_upper_l_value)
            self.smartdashboard.putBoolean("Climber right upper end", self.climber.end_upper_r_value)

            self.smartdashboard.putNumber("Right Distance", self.drivetrain.get_right_distance())
            self.smartdashboard.putNumber("Distance", self.drivetrain.get_distance())
            self.smartdashboard.putNumber("Right Volts", right_voltage)
            
            self.smartdashboard.putNumber("Pitch", self.drivetrain.get_pitch())
            
            self.smartdashboard.putData("NavX", self.drivetrain.navx)
            self.smartdashboard.putData("PID", self.drivetrain.reference_pid_controller)
            
            self.drivetrain.update_odometry()
            self.field.setRobotPose(self.drivetrain.get_pose())
            self.smartdashboard.putData("Field", self.field)

            self.mid_angle = self.smartdashboard.getNumber("Mid Angle", self.mid_angle)
            self.high_angle = self.smartdashboard.getNumber("Comunity Angle", self.high_angle)

            self.low_angle = self.smartdashboard.getNumber("Low Angle", self.low_angle)

        except BaseException as e:
            log_exception(e)
        
    def teleopInit(self) -> None:
        try:
            self.climber.update_end_switches()
            self.drivetrain.differential_drive.setSafetyEnabled(True)
            self.arm.reset_angle_encoder()
        except BaseException as e:
            log_exception(e)

    def teleopPeriodic(self) -> None:
        for mechanism in self.mechanisms:
            try:
                mechanism.teleop_control(self.controller)
            except BaseException as e:
                log_exception(e)

    def autonomousInit(self) -> None:
        try:
            self.drivetrain.differential_drive.setSafetyEnabled(True)
            self.drivetrain.differential_drive.setExpiration(0.1)
            self.timer.reset()
            self.timer.start()

            self.drivetrain.set_stop_distance()
            self.auto_speed = AUTONOMOUS_SPEED

        except BaseException as e:
            log_exception(e)
    def autonomousPeriodic(self) -> None:
        distance = self.drivetrain.get_distance()
        try:
            if self.task_count == 0:
                self.drivetrain.move_straight(AUTONOMOUS_SPEED)
                if self.timer.get() > 0.8:
                    self.drivetrain.idle()
                    self.drivetrain.reset_encoders()
                    self.task_count += 1
                return

            if self.task_count == 1:
                if distance > -2.40:
                    self.drivetrain.move_straight(-self.auto_speed)

                elif distance < -2:
                    self.drivetrain.move_straight(self.auto_speed)
                    self.auto_speed = self.auto_speed*.99
                else:
                    self.drivetrain.idle()

                if ONLY_DRIVETRAIN_MODE:
                    return
        except BaseException as e:
            log_exception(e)
        
        try:
            self.arm.stop_arm_angle()
            # self.climber.home()
        except BaseException as e:
            log_exception(e)

if __name__ == "__main__":
    wpilib.run(MyRobot)