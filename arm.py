import rev
import wpilib

ARM_ANGLE_SPARK_ID = 51
ARM_LENGHT_SPARK_ID = 50

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

ANGLE_SWITCH_PORT = 0
LENGTH_SWITCH_PORT = 1

ANGLE_HOMING_DUTY_CYCLE = 0.17
LENGHT_HOMING_DUTY_CYCLE = 0.15

class Arm:     
    def __init__(self):
        self.is_homed = False
        self.lenght_is_homed = False
        self.angle_is_homed = False

        self.m_angle = rev.CANSparkMax(ARM_ANGLE_SPARK_ID, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        self.m_angle.setInverted(True) 
        self.m_lenght = rev.CANSparkMax(ARM_LENGHT_SPARK_ID,  rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        self.m_lenght.setInverted(True) 

        self.angle_encoder = self.m_angle.getEncoder()
        self.lenght_encoder = self.m_lenght.getEncoder()

        self.angle_pid = self.m_angle.getPIDController()
        self.angle_pid.setP(ARM_ANGLE["KP"])
        self.angle_pid.setI(ARM_ANGLE["KI"])
        self.angle_pid.setD(ARM_ANGLE["KD"])

        self.lenght_pid = self.m_lenght.getPIDController()
        self.lenght_pid.setP(ARM_LENGHT["KP"])
        self.lenght_pid.setI(ARM_LENGHT["KI"])
        self.lenght_pid.setD(ARM_LENGHT["KD"])

        self.angle_limit_switch = wpilib.DigitalInput(ANGLE_SWITCH_PORT)
        self.lenght_limit_switch = wpilib.DigitalInput(LENGTH_SWITCH_PORT)

    # def init function with empty return type annotation
    def init(self) -> None:
        pass

    def angle_switch_is_pressed(self) -> bool:
        return self.angle_limit_switch.get()
    
    def lenght_switch_is_pressed(self) -> bool:
        return self.lenght_limit_switch.get()

    def home(self) -> None:
        if not self.angle_is_homed:
            self.home_angle()
        if not self.lenght_is_homed:
            self.home_lenght()
        if self.angle_is_homed and self.lenght_is_homed:
            self.is_homed = True

    def home_angle(self, duty_cycle:float = ANGLE_HOMING_DUTY_CYCLE) -> None:
        if self.angle_switch_is_pressed():
            self.set_angle_duty_cycle(0)
            self.angle_is_homed = True
        else:
            self.set_angle_duty_cycle(duty_cycle)
    
    def home_lenght(self, duty_cycle:float = LENGHT_HOMING_DUTY_CYCLE) -> None:
        if self.lenght_switch_is_pressed():
            self.set_lenght_duty_cycle(0)
            self.lenght_is_homed = True
        else:
            self.set_lenght_duty_cycle(duty_cycle)

    def get_angle_position(self) -> float:
        return self.angle_encoder.getPosition()
    
    def get_length_position(self) -> float:
        return self.lenght_encoder.getPosition()
    
    def set_angle_position(self, angle:float) -> None:
        self.angle_pid.setReference(angle, rev.CANSparkMax.ControlType.kPosition)
    
    def set_lenght_position(self, lenght:float) -> None:
        self.lenght_pid.setReference(lenght, rev.CANSparkMax.ControlType.kPosition)

    def stop_arm_angle(self) -> None:
        position = self.get_angle_position()
        self.angle_pid.setReference(position, rev.CANSparkMax.ControlType.kPosition)

    def stop_arm_lenght(self) -> None:
        position = self.get_length_position()
        self.lenght_pid.setReference(position, rev.CANSparkMax.ControlType.kPosition)

    def set_angle_duty_cycle(self, duty_cycle:float) -> None:
        self.angle_pid.setReference(duty_cycle, rev.CANSparkMax.ControlType.kDutyCycle)

    def set_lenght_duty_cycle(self, duty_cycle:float) -> None:
        self.lenght_pid.setReference(duty_cycle, rev.CANSparkMax.ControlType.kDutyCycle)
    
    def increase_arm_lenght(self) -> None:
        self.set_lenght_duty_cycle(1.5 * LENGHT_HOMING_DUTY_CYCLE)

    def decrease_arm_lenght(self) -> None:
        self.set_lenght_duty_cycle(-LENGHT_HOMING_DUTY_CYCLE)

    def increase_arm_angle(self) -> None:
        self.set_angle_duty_cycle(1.5 * ANGLE_HOMING_DUTY_CYCLE)

    def decrease_arm_angle(self) -> None:
        self.set_angle_duty_cycle(-ANGLE_HOMING_DUTY_CYCLE)
        