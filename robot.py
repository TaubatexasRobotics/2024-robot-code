from drivetrain import Drivetrain
from arm import Arm
from tweezer_intake import TweezerIntake as Intake
from controller import Controller

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
        self.intake = Intake()
        self.timer = wpilib.Timer()

        self.task_count = 0
        # self.high_angle = 1
        # self.high_lenght = 1

        self.high_angle = -11.404823303222656
        self.high_lenght = 2.738093852996826

        self.mid_angle = -12.38
        self.mid_lenght = 3.1428
        self.low_angle = 2.098
        self.low_lenght = -20.190
        wpilib.CameraServer.launch()

        self.smartdashboard = wpilib.SmartDashboard
        self.field = wpilib.Field2d()
        
        leftPosition = self.drivetrain.get_left_distance()
        rightPosition = self.drivetrain.get_right_distance()
        
        self.arm.stop_arm_angle()
        self.arm.stop_arm_length()

        self.smartdashboard.putNumber("Mid Angle", self.mid_angle)
        self.smartdashboard.putNumber("Mid Length", self.mid_lenght)
        self.smartdashboard.putNumber("Comunity Angle", self.high_angle)
        self.smartdashboard.putNumber("Comunity Length", self.high_lenght)
        self.smartdashboard.putNumber("Low Angle", self.low_angle)
        self.smartdashboard.putNumber("Low Length", self.low_lenght)
        
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

            self.mid_angle = self.smartdashboard.getNumber("Mid Angle", self.mid_angle)
            self.mid_lenght = self.smartdashboard.getNumber("Mid Length", self.mid_lenght)
            self.high_angle = self.smartdashboard.getNumber("Comunity Angle", self.high_angle)
            self.high_lenght = self.smartdashboard.getNumber("Comunity Length", self.high_lenght)

            self.low_angle = self.smartdashboard.getNumber("Low Angle", self.low_angle)
            self.low_lenght = self.smartdashboard.getNumber("Low Length", self.low_lenght)

        except BaseException as e:
            log_exception(e)
        
    def teleopInit(self) -> None:
        try:
            self.drivetrain.differential_drive.setSafetyEnabled(True)
            self.arm.reset_lenght_encoder()
            self.arm.reset_angle_encoder()
        except BaseException as e:
            log_exception(e)

    def teleopPeriodic(self) -> None:
        try:
            self.drivetrain.move( *self.controller.get_drive() )
        except BaseException as e: 
            log_exception(e)
        
        try:
            if ONLY_DRIVETRAIN_MODE:
                return
            
            if self.controller.sensitivity_toggle_button():
                self.controller.toggle_low_sensitivity_mode()

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


            if self.controller.catch_gamepiece():
                self.intake.catch_gamepiece()

            if self.controller.release_gamepiece():
                self.intake.release_gamepiece()

            if self.controller.stop_intake():
                self.intake.stop()

            if self.controller.set_angle_and_lenght_position_high():
                self.arm.set_angle_position(self.high_angle)
                # self.arm.set_length_position(self.high_lenght)

            if self.controller.set_angle_and_lenght_position_mid():
                self.arm.set_angle_position(self.mid_angle)
                # self.arm.set_length_position(self.mid_lenght)

            if self.controller.set_angle_and_lenght_position_low():
                self.arm.set_angle_position(self.low_angle)
                # self.arm.set_length_position(self.low_lenght)

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
                    print('start 1')
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
            # if not self.arm.is_homed:
            #     self.arm.home()
            #     return
        except BaseException as e:
            log_exception(e)


if __name__ == "__main__":
    wpilib.run(MyRobot)