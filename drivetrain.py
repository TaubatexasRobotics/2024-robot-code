import wpilib 
import wpilib.drive
import wpimath.controller
import wpimath.geometry
import wpimath.kinematics

from navx import AHRS

import ctre
import math

C_RIGHT_FRONT = 1
C_RIGHT_BACK = 2
C_LEFT_FRONT = 3
C_LEFT_BACK = 4

LEFT_ENCODER = (0, 1)
RIGHT_ENCODER = (2, 3)

ENCODER_DISTANCE_PER_PULSE = 3.05/3925
INITIAL_POSE = (0, 0, 0) # (x, y, theta)

class Drivetrain:
    def __init__(self):
        self.m_left_back = ctre.WPI_VictorSPX(C_LEFT_BACK)
        self.m_left_front = ctre.WPI_VictorSPX(C_LEFT_FRONT)
        self.m_right_front = ctre.WPI_VictorSPX(C_RIGHT_FRONT)
        self.m_right_back = ctre.WPI_VictorSPX(C_RIGHT_BACK)

        self.m_left= wpilib.MotorControllerGroup(self.m_left_front,self.m_left_back) 
        self.m_left.setInverted(True)
        self.m_right= wpilib.MotorControllerGroup(self.m_right_front,self.m_right_back) 

        self.differential_drive  = wpilib.drive.DifferentialDrive(self.m_left, self.m_right)

        self.encoder_left = wpilib.Encoder(*LEFT_ENCODER, True, wpilib.Encoder.EncodingType.k4X)
        self.encoder_right = wpilib.Encoder(*RIGHT_ENCODER, False, wpilib.Encoder.EncodingType.k4X)

        self.encoder_left.reset()
        self.encoder_right.reset()
        
        self.navx = AHRS.create_spi()
        self.navx.reset()

        self.encoder_left.setDistancePerPulse(ENCODER_DISTANCE_PER_PULSE)
        self.encoder_right.setDistancePerPulse(ENCODER_DISTANCE_PER_PULSE)
        
        self.reference_pid_controller = wpimath.controller.PIDController(0, 0, 0)
        self.left_pid_controller = wpimath.controller.PIDController(0, 0, 0)
        self.right_pid_controller = wpimath.controller.PIDController(0, 0, 0)
        
        rotation = wpimath.geometry.Rotation2d.fromDegrees(self.navx.getAngle())
        initial_pose = wpimath.geometry.Pose2d(*INITIAL_POSE)
        self.odometry = wpimath.kinematics.DifferentialDriveOdometry(rotation, 0, 0, initial_pose)

    def set_stop_distance(self):
        self.stop_distance = self.get_distance()

    def stop(self):
        self.kp = 100
        error = self.get_distance() - self.stop_distance
        power = math.ceil(error * self.kp)
        self.move_straight(-power)

    # def stop(self):
    #     stop_distance = self.get_distance()
    #     # if(self.get_distance < stop_distance)
    #     error = self.get_distance()
    #     error = self.
    #     self.move_straight(kp * )
        
    def move_straight(self, speed):
        self.differential_drive.arcadeDrive(speed, 0)

    def make_turn(self, turn_speed):
        self.differential_drive.arcadeDrive(0, turn_speed)

    def idle(self):
        self.differential_drive.arcadeDrive(0, 0)

    def move(self, speed, turn_speed):
        self.differential_drive.arcadeDrive(speed, turn_speed)

    def reset_encoders(self):
        self.encoder_left.reset()
        self.encoder_right.reset()

    def get_left_encoder_pulses(self):
        return self.encoder_left.get()
    
    def get_right_encoder_pulses(self):
        return self.encoder_right.get()

    def get_distance(self):
        return self.encoder_right.getDistance()
        # return (self.encoder_left.getDistance() + self.encoder_right.getDistance()) / 2
    
    def get_left_distance(self):
        return self.encoder_left.getDistance()
    
    def get_right_distance(self):
        return self.encoder_right.getDistance()
    
    def update_odometry(self):
        rotation = wpimath.geometry.Rotation2d.fromDegrees(self.navx.getAngle())
        self.odometry.update(rotation, self.encoder_left.getDistance(), self.encoder_right.getDistance())
        
    def get_pose(self):
        return self.odometry.getPose()
    
    def get_pitch(self):
        return self.navx.getPitch()
    
    def set_tank_drive_volts(self, leftVolts, rightVolts):
        self.m_left.setVoltage(leftVolts)
        self.m_right.setVoltage(-rightVolts)
        self.differential_drive.feed()
    
    def get_motors_voltage(self):
        motor_left_v = (self.m_left_back.getMotorOutputVoltage() + self.m_left_front.getMotorOutputVoltage())/2
        motor_right_v = (self.m_right_back.getMotorOutputVoltage() + self.m_right_front.getMotorOutputVoltage())/2
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
        
