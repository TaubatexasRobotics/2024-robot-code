from drivetrain import Drivetrain
from arm import Arm
from climber import Climber
from controller import Controller
from shooter import Shooter

import wpilib

AUTONOMOUS_SPEED = 0.45
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

        # wpilib.CameraServer.launch()
        self.smartdashboard = wpilib.SmartDashboard
                
        self.arm.stop_arm_angle()
        
    def robotPeriodic(self) -> None:
        self.drivetrain.robotPeriodic()
        for mechanism in self.mechanisms:
            try:
                mechanism.update_dashboard(self.smartdashboard)

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

            self.initial_angle = self.drivetrain.get_yaw()

            self.drivetrain.autonomousInit()

        except BaseException as e:
            log_exception(e)
    def autonomousPeriodic(self) -> None:
        try:
            if self.task_count == 0:
                self.shooter.shoot()
                if self.timer.get() > 2:
                    self.shooter.store_gamepiece()
                if self.timer.get() > 4:
                    self.shooter.stop_shooter()
                    self.shooter.stop_shooter_feeder()
                    self.task_count += 1
                return

            if self.task_count == 1:
                self.drivetrain.move_straight(-AUTONOMOUS_SPEED)
                # if self.timer.get() > 0.8:
                if self.drivetrain.get_right_distance()<-3.2:
                    self.drivetrain.idle()
                    self.drivetrain.reset_encoders()
                    self.task_count += 1
                return
                # self.drivetrain.seek_angle(self.initial_angle + 45)
                pass
                # if distance > -2.40:
                #     self.drivetrain.move_straight(-self.auto_speed)

                # elif distance < -2:
                #     self.drivetrain.move_straight(self.auto_speed)
                #     self.auto_speed = self.auto_speed*.99
                # else:
                #     self.drivetrain.idle()

                if ONLY_DRIVETRAIN_MODE:
                    return
        except BaseException as e:
            log_exception(e)
        
        # try:
            # self.drivetrain.seek_angle(150)
            # self.arm.stop_arm_angle()
            # self.climber.home()

        # except BaseException as e:
        #     log_exception(e)

if __name__ == "__main__":
    wpilib.run(MyRobot)