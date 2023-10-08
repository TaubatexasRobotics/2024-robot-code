import rev
import ctre

TOP_MOTOR_SPARK_ID = 52
BOTTOM_MOTOR_REDLINE = 12 
SPARK_FORCE = -1
REDLINE_FORCE = .80

class TopIntake:
   def __init__(self):
      self.m_upper = rev.CANSparkMax(TOP_MOTOR_SPARK_ID, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
      self.m_lower = ctre.WPI_VictorSPX(BOTTOM_MOTOR_REDLINE)
   
   def catch_gamepiece(self) -> None:
      self.m_upper.set(-SPARK_FORCE)
      self.m_lower.set(-REDLINE_FORCE)

   def release_gamepiece(self) -> None:
      self.m_upper.set(SPARK_FORCE)
      self.m_lower.set(REDLINE_FORCE)

   def stop(self) -> None:
      self.m_upper.set(0)
      self.m_lower.set(0)
      