import wpilib 
import wpilib.drive
import ctre

C_LEFT_BACK = 1
C_LEFT_FRONT = 2
C_RIGHT_FRONT = 3
C_RIGHT_BACK = 4

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

    def init(self):
        pass