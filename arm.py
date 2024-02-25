import rev

ARM_ANGLE_SPARK_ID = 54

LIMIT_ANGLE_FORWARD = 0
LIMIT_ANGLE_BACKWARD = 17

ARM_ANGLE_PID = {
    "KP" : 0.1,
    "KI" : 0.0,
    "KD" : 0.1,
    "MAX_VELOCITY" : 2000,
    "MAX_ACCELERATION" : 1500,
    "ALLOWABLE_ERROR" : 0
}

ANGLE_HOMING_DUTY_CYCLE = 0.17

class Arm:     
    def __init__(self):
        self.is_homed = False
        self.angle_is_homed = False

        self.m_angle = rev.CANSparkMax(ARM_ANGLE_SPARK_ID, rev.CANSparkMax.MotorType.kBrushless)
        self.m_angle.setInverted(True) 

        self.angle_encoder = self.m_angle.getEncoder()

        self.angle_pid = self.m_angle.getPIDController()
        self.angle_pid.setP(ARM_ANGLE_PID["KP"])
        self.angle_pid.setI(ARM_ANGLE_PID["KI"])
        self.angle_pid.setD(ARM_ANGLE_PID["KD"])

        #set angle smart motion constants
        # self.angle_pid.setSmartMotionMaxVelocity(ARM_ANGLE_PID["MAX_VELOCITY"])
        # self.angle_pid.setSmartMotionMaxAccel(ARM_ANGLE_PID["MAX_ACCELERATION"])
        # self.angle_pid.setSmartMotionAllowedClosedLoopError(ARM_ANGLE_PID["ALLOWABLE_ERROR"])

        # self.angle_limit_switch = wpilib.DigitalInput(ANGLE_SWITCH_PORT)

    def init(self) -> None:
        pass

    def home_angle(self, duty_cycle:float = ANGLE_HOMING_DUTY_CYCLE) -> None:
        if self.angle_switch_is_pressed():
            self.set_angle_duty_cycle(0)
            self.angle_is_homed = True
        else:
            self.set_angle_duty_cycle(duty_cycle)
    
    def get_angle_position(self) -> float:
        return self.angle_encoder.getPosition()

    def reset_angle_encoder(self):
        self.angle_encoder.setPosition(0)
        self.set_angle_position(0)
        
    def set_angle_position(self, angle:float) -> None:
        self.angle_pid.setReference(angle, rev.CANSparkMax.ControlType.kPosition)

    # set angle smart motion
    def set_angle_smart_motion(self, angle:float) -> None:
        self.angle_pid.setReference(angle, rev.CANSparkMax.ControlType.kSmartMotion)

    def stop_arm_angle(self) -> None:
        position = self.get_angle_position()
        self.angle_pid.setReference(position, rev.CANSparkMax.ControlType.kPosition)

    def set_angle_duty_cycle(self, duty_cycle:float) -> None:
        self.angle_pid.setReference(duty_cycle, rev.CANSparkMax.ControlType.kDutyCycle)


    def increase_arm_angle(self) -> None:
        self.set_angle_duty_cycle(1.5 * ANGLE_HOMING_DUTY_CYCLE)
    
    def decrease_arm_angle(self) -> None:
        self.set_angle_duty_cycle(-ANGLE_HOMING_DUTY_CYCLE)
    