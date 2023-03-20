import wpilib 
import wpilib.drive
import wpimath.controller
import wpimath.geometry
import wpimath.kinematics

from navx import AHRS

import ctre

C_LEFT_BACK = 1
C_LEFT_FRONT = 2
C_RIGHT_FRONT = 3
C_RIGHT_BACK = 4

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

        self.encoder_left = wpilib.Encoder(6, 7, True, wpilib.Encoder.EncodingType.k4X)
        self.encoder_right = wpilib.Encoder(8, 9, False, wpilib.Encoder.EncodingType.k4X)

        self.encoder_left.reset()
        self.encoder_right.reset()
        
        self.navx = AHRS.create_spi()
        self.navx.reset()

        self.encoder_left.setDistancePerPulse(ENCODER_DISTANCE_PER_PULSE)
        self.encoder_right.setDistancePerPulse(ENCODER_DISTANCE_PER_PULSE)
        
        rotation = wpimath.geometry.Rotation2d.fromDegrees(180 - self.navx.getAngle())
        initial_pose = wpimath.geometry.Pose2d(*INITIAL_POSE)
        self.odometry = wpimath.kinematics.DifferentialDriveOdometry(rotation, 0, 0, initial_pose)
        
    def move_straight(self, speed):
        self.differential_drive.arcadeDrive(speed, 0)

    def make_turn(self, speed):
        self.differential_drive.arcadeDrive(0, speed)

    def stop(self):
        self.differential_drive.arcadeDrive(0, 0)

    def move(self, speed, turn):
        self.differential_drive.arcadeDrive(speed, turn)

    def reset_encoders(self):
        self.encoder_left.reset()
        self.encoder_right.reset()

    def get_left_encoder_pulses(self):
        return self.encoder_left.get()
    
    def get_right_encoder_pulses(self):
        return self.encoder_right.get()

    def get_distance(self):
        return (self.encoder_left.getDistance() + self.encoder_right.getDistance()) / 2
    
    def get_left_distance(self):
        return self.encoder_left.getDistance()
    
    def get_right_distance(self):
        return self.encoder_right.getDistance()
    
    def update_odometry(self):
        rotation = wpimath.geometry.Rotation2d.fromDegrees(180 - self.navx.getAngle())
        self.odometry.update(rotation, self.encoder_left.getDistance(), self.encoder_right.getDistance())
        
    def get_pose(self):
        return self.odometry.getPose()
    
    def get_pitch(self):
        return self.navx.getPitch()

