class top_intake:

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