import wpilib 
import wpilib.drive
import wpimath.controller
import wpimath.geometry
import wpimath.kinematics

from controller import Controller

from navx import AHRS

import rev
import math

C_RIGHT_FRONT = 53
C_RIGHT_BACK = 51
C_LEFT_FRONT = 50
C_LEFT_BACK = 52

# ENCODER_DISTANCE_PER_PULSE = 3.05/3925
INITIAL_POSE = (0, 0, 0) # (x, y, theta)

class Drivetrain:
    def __init__(self):
        self.m_left_back = rev.CANSparkMax(C_LEFT_BACK, rev.CANSparkMax.MotorType.kBrushless)
        self.m_left_front = rev.CANSparkMax(C_LEFT_FRONT, rev.CANSparkMax.MotorType.kBrushless)
        self.m_right_front = rev.CANSparkMax(C_RIGHT_FRONT, rev.CANSparkMax.MotorType.kBrushless)
        self.m_right_back = rev.CANSparkMax(C_RIGHT_BACK, rev.CANSparkMax.MotorType.kBrushless)

        self.m_left= wpilib.MotorControllerGroup(self.m_left_front,self.m_left_back) 
        self.m_left.setInverted(True)
        self.m_right= wpilib.MotorControllerGroup(self.m_right_front,self.m_right_back) 

        self.differential_drive  = wpilib.drive.DifferentialDrive(self.m_left, self.m_right)

        self.encoder_left = self.m_left_back.getEncoder()
        self.encoder_right = self.m_right_back.getEncoder()

        self.encoder_left.setPositionConversionFactor(1)
        self.encoder_right.setPositionConversionFactor(1)
        
        self.encoder_left.setPosition(0)
        self.encoder_right.setPosition(0)
        
        self.navx = AHRS.create_spi()
        self.navx.reset()

        self.field = wpilib.Field2d()

        self.reference_pid_controller = wpimath.controller.PIDController(0, 0, 0)
        self.left_pid_controller = wpimath.controller.PIDController(0, 0, 0)
        self.right_pid_controller = wpimath.controller.PIDController(0, 0, 0)
        
        rotation = wpimath.geometry.Rotation2d.fromDegrees(self.navx.getAngle())
        initial_pose = wpimath.geometry.Pose2d(*INITIAL_POSE)
        self.odometry = wpimath.kinematics.DifferentialDriveOdometry(rotation, 0, 0, initial_pose)

    def update_dashboard(self, dashboard) -> None:
        left_distance = self.get_left_distance()
        right_distance = self.get_right_distance()
        left_voltage, right_voltage = self.get_motors_voltage()

        dashboard.putNumber("Left Pulses", left_distance)
        dashboard.putNumber("Left Distance", right_distance)
        dashboard.putNumber("Left Volts", left_voltage)
        dashboard.putNumber("Right Volts", right_voltage)

        dashboard.putNumber("Right Distance", self.get_right_distance())
        dashboard.putNumber("Distance", self.get_distance())

        dashboard.putNumber("Pitch", self.get_pitch())
        dashboard.putData("NavX", self.navx)
        dashboard.putData("PID", self.reference_pid_controller)

        self.field.setRobotPose(self.get_pose())
        dashboard.putData("Field", self.field)
        
        self.update_odometry()

    def teleop_control(self, controller: Controller) -> None:
        if controller.is_pressed('SELECT_BUTTON'):
            controller.toggle_low_sensitivity_mode()
        
        self.move( *controller.get_drive() )

    def set_stop_distance(self):
        self.stop_distance = self.get_distance()

    def stop(self):
        self.kp = 100
        error = self.get_distance() - self.stop_distance
        power = math.ceil(error * self.kp)
        self.move_straight(-power)

    def move_straight(self, speed):
        self.differential_drive.arcadeDrive(speed, 0)

    def make_turn(self, turn_speed):
        self.differential_drive.arcadeDrive(0, turn_speed)

    def idle(self):
        self.differential_drive.arcadeDrive(0, 0)

    def move(self, speed, turn_speed):
        self.differential_drive.arcadeDrive(speed, turn_speed)

    def reset_encoders(self):
        self.encoder_left.setPosition(0)
        self.encoder_right.setPosition(0)

    def get_distance(self):
        return (self.encoder_left.getPosition() + self.encoder_right.getPosition()) / 2
    
    def get_left_distance(self):
        return self.encoder_left.getPosition()
    
    def get_right_distance(self):
        return self.encoder_right.getPosition()
    
    def update_odometry(self):
        rotation = wpimath.geometry.Rotation2d.fromDegrees(self.navx.getAngle())
        self.odometry.update(rotation, self.get_left_distance(), self.get_right_distance())
        
    def get_pose(self):
        return self.odometry.getPose()
    
    def get_pitch(self):
        return self.navx.getPitch()
    
    def get_roll(self):
        return self.navx.getRoll()
    
    def set_tank_drive_volts(self, leftVolts, rightVolts):
        self.m_left.setVoltage(leftVolts)
        self.m_right.setVoltage(-rightVolts)
        self.differential_drive.feed()
    
    def get_motors_voltage(self):
        motor_left_v = (self.m_left_back.getBusVoltage() + self.m_left_front.getBusVoltage())/2
        motor_right_v = (self.m_right_back.getBusVoltage() + self.m_right_front.getBusVoltage())/2
        return motor_left_v, motor_right_v
    
    def update_pid_constants(self):
        constants = (
            self.reference_pid_controller.getP(),
            self.reference_pid_controller.getI(),
            self.reference_pid_controller.getD()
        )
        self.left_pid_controller.setPID(*constants)
        self.right_pid_controller.setPID(*constants)
    
    #method to lock the robot in place using pid controller
    def lock(self, left_setpoint, right_setpoint):
        self.update_pid_constants()
        
        left_output = self.left_pid_controller.calculate(left_setpoint, self.encoder_left.getDistance())
        right_output = self.right_pid_controller.calculate(right_setpoint, self.encoder_right.getDistance())
        
        self.set_tank_drive_volts(left_output, right_output)
        
