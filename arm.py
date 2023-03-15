import rev

ARM_LENGHT_SPARK_ID = 50
ARM_ANGLE_SPARK_ID = 51

ANGLE_HOMING_SPEED = 0.10
LENGHT_HOMING_SPEED = 0.10

LIMIT_ANGLE_FORWARD = 0
LIMIT_ANGLE_BACKWARD = 21.7

LIMIT_LENGHT_FORWARD = 4.97
LIMIT_LENGHT_BACKWARD = 0

ARM_ANGLE= {
    "KP" : 0.1,
    "KI" : 0.0,
    "KD" : 0.1,
}

ARM_LENGHT= {
    "KP" : 0.3,
    "KI" : 0.0,
    "KD" : 0.1,   
}

class Arm:     
    def __init__(self):
        self.is_homed = False
        self.lenght_is_homed = False
        self.angle_is_homed = False

        self.m_arm_angle = rev.CANSparkMax(ARM_ANGLE_SPARK_ID, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        self.m_arm_lenght = rev.CANSparkMax(ARM_LENGHT_SPARK_ID,  rev.CANSparkMaxLowLevel.MotorType.kBrushless)

        self.m_arm_angle_pid = self.m_arm_angle.getPIDController()
        self.m_arm_angle_pid.setP(ARM_ANGLE["KP"])
        self.m_arm_angle_pid.setI(ARM_ANGLE["KI"])
        self.m_arm_angle_pid.setD(ARM_ANGLE["KD"])

        self.m_arm_lenght_pid = self.m_arm_lenght.getPIDController()
        self.m_arm_lenght_pid.setP(ARM_LENGHT["KP"])
        self.m_arm_lenght_pid.setI(ARM_LENGHT["KI"])
        self.m_arm_lenght_pid.setD(ARM_LENGHT["KD"])

    # def init function with empty return type annotation
    def init(self) -> None:
        pass

    def homeArm(self) -> None:
        if not self.lenght_is_homed:
            self.home_lenght()
        if not self.angle_is_homed:
            self.home_angle()
        if self.angle_is_homed and self.lenght_is_homed:
            self.is_homed = True
        return
    
    def home_lenght(self, speed:float = LENGHT_HOMING_SPEED) -> None:
        self.m_arm_angle_pid.setReference(speed, rev.CANSparkMax.ControlType.kDutyCycle)
        return

    def home_angle(self, speed:float = ANGLE_HOMING_SPEED) -> None:
        self.m_arm_angle_pid.setReference(speed, rev.CANSparkMax.ControlType.kDutyCycle)
        return

    def setAnglePosition(self, angle:float) -> None:
        self.m_arm_angle_pid.setReference(angle, rev.CANSparkMax.ControlType.kPosition)
        return

    def setLenghtPosition(self, lenght:float) -> None:
        self.m_arm_lenght_pid.setReference(lenght, rev.CANSparkMax.ControlType.kPosition)
        return
    
    def setAngleSpeed(self, speed:float) -> None:
        self.m_arm_angle_pid.setReference(speed, rev.CANSparkMax.ControlType.kDutyCycle)
        return
    
    def setLenghtSpeed(self, speed:float) -> None:
        self.m_arm_lenght_pid.setReference(speed, rev.CANSparkMax.ControlType.kDutyCycle)
        return
    
