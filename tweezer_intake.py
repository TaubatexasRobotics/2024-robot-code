import ctre

BOTTOM_MOTOR_REDLINE = 12 
REDLINE_FORCE = .8

class TweezerIntake:
   def __init__(self):
      self.m_intake = ctre.WPI_VictorSPX(BOTTOM_MOTOR_REDLINE)
   
   def catch_gamepiece(self) -> None:
      self.m_intake.set(-REDLINE_FORCE)

   def release_gamepiece(self) -> None:
      self.m_intake.set(REDLINE_FORCE)

   def stop(self) -> None:
      self.m_intake.set(0)
      