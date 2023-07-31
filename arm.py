import rev
import wpilib

ARM_ANGLE_SPARK_ID = 50
ARM_LENGTH_SPARK_ID = 51

LIMIT_ANGLE_FORWARD = 0
LIMIT_ANGLE_BACKWARD = 17

# LIMIT_LENGTH_FORWARD = -3.6
# LIMIT_LENGTH_BACKWARD = 0
LIMIT_LENGTH_BACKWARD = -3.6
LIMIT_LENGTH_FORWARD = 0

ARM_ANGLE_PID = {
    "KP" : 0.1,
    "KI" : 0.0,
    "KD" : 0.1,
}

ARM_LENGTH_PID = {
    "KP" : 0.1,
    "KI" : 0.0,
    "KD" : 0.1,   
}

# ANGLE_SWITCH_PORT = 0

# LENGTH_SWITCH_PORT = 1
ANGLE_HOMING_DUTY_CYCLE = 0.17
LENGTH_HOMING_DUTY_CYCLE = 0.15

class Arm:     
    def __init__(self):
        self.is_homed = False
        self.length_is_homed = False
        self.angle_is_homed = False

        self.m_angle = rev.CANSparkMax(ARM_ANGLE_SPARK_ID, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        # self.m_angle.setInverted(True) 
        self.m_length = rev.CANSparkMax(ARM_LENGTH_SPARK_ID,  rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        # self.m_length.setInverted(True) 

        self.angle_encoder = self.m_angle.getEncoder()
        self.length_encoder = self.m_length.getEncoder()

        self.angle_pid = self.m_angle.getPIDController()
        self.angle_pid.setP(ARM_ANGLE_PID["KP"])
        self.angle_pid.setI(ARM_ANGLE_PID["KI"])
        self.angle_pid.setD(ARM_ANGLE_PID["KD"])

        self.length_pid = self.m_length.getPIDController()
        self.length_pid.setP(ARM_LENGTH_PID["KP"])
        self.length_pid.setI(ARM_LENGTH_PID["KI"])
        self.length_pid.setD(ARM_LENGTH_PID["KD"])

        # self.angle_limit_switch = wpilib.DigitalInput(ANGLE_SWITCH_PORT)
        # self.length_limit_switch = wpilib.DigitalInput(LENGTH_SWITCH_PORT)

    def init(self) -> None:
        pass

    def angle_switch_is_pressed(self) -> bool:
        return self.angle_limit_switch.get()
    
    def length_switch_is_pressed(self) -> bool:
        return self.length_limit_switch.get()

    def home(self) -> None:
        if not self.angle_is_homed:
            self.home_angle()
        if not self.length_is_homed:
            self.home_length()
        if self.angle_is_homed and self.length_is_homed:
            self.is_homed = True

    def home_angle(self, duty_cycle:float = ANGLE_HOMING_DUTY_CYCLE) -> None:
        if self.angle_switch_is_pressed():
            self.set_angle_duty_cycle(0)
            self.angle_is_homed = True
        else:
            self.set_angle_duty_cycle(duty_cycle)
    
    def home_length(self, duty_cycle:float = LENGTH_HOMING_DUTY_CYCLE) -> None:
        if self.length_switch_is_pressed():
            self.set_length_duty_cycle(0)
            self.length_is_homed = True
        else:
            self.set_length_duty_cycle(duty_cycle)

    def get_angle_position(self) -> float:
        return self.angle_encoder.getPosition()
    
    def get_length_position(self) -> float:
        return self.length_encoder.getPosition()
    
    def set_angle_position(self, angle:float) -> None:
        self.angle_pid.setReference(angle, rev.CANSparkMax.ControlType.kPosition)
    
    def set_length_position(self, length:float) -> None:
        self.length_pid.setReference(length, rev.CANSparkMax.ControlType.kPosition)

    def stop_arm_angle(self) -> None:
        position = self.get_angle_position()
        self.angle_pid.setReference(position, rev.CANSparkMax.ControlType.kPosition)

    def stop_arm_length(self) -> None:
        position = self.get_length_position()
        self.length_pid.setReference(position, rev.CANSparkMax.ControlType.kPosition)

    def set_angle_duty_cycle(self, duty_cycle:float) -> None:
        self.angle_pid.setReference(duty_cycle, rev.CANSparkMax.ControlType.kDutyCycle)

    def set_length_duty_cycle(self, duty_cycle:float) -> None:
        self.length_pid.setReference(duty_cycle, rev.CANSparkMax.ControlType.kDutyCycle)
    
    def increase_arm_length(self) -> None:
        self.set_length_duty_cycle(1.5 * LENGTH_HOMING_DUTY_CYCLE)

    def decrease_arm_length(self) -> None:
        self.set_length_duty_cycle(-LENGTH_HOMING_DUTY_CYCLE)

    def increase_arm_angle(self) -> None:
        self.set_angle_duty_cycle(1.5 * ANGLE_HOMING_DUTY_CYCLE)

    def decrease_arm_angle(self) -> None:
        self.set_angle_duty_cycle(-ANGLE_HOMING_DUTY_CYCLE)
        