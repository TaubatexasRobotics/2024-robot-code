import wpilib

MODULE_ID = 0
SOLENOID_FORWARD_CHANNEL = 0
SOLENOID_REVERSE_CHANNEL = 1

class PneumaticIntake:
    def __init__(self):
        self.is_open = False

        self.pcm = wpilib.PneumaticsControlModule(MODULE_ID)
        self.solenoid = self.pcm.makeDoubleSolenoid(SOLENOID_FORWARD_CHANNEL, SOLENOID_REVERSE_CHANNEL)
        self.compressor = self.pcm.makeCompressor()

    def init(self):
        pass

    def open_intake(self):
        self.solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)

    def close_intake(self):
        self.solenoid.set(wpilib.DoubleSolenoid.Value.kForward)

    def toggle(self):
        if self.is_open:
            self.close_intake()
        else:
            self.open_intake()
        self.is_open = not self.is_open

    def enable_compressor(self):
        self.compressor.enableDigital()

    def disable_compressor(self):
        self.compressor.disable()

    def toggle_compressor(self):
        if self.compressor.isEnabled():
            self.disable_compressor()
        else:
            self.enable_compressor()

    def get_is_full(self):
        return self.compressor.getPressureSwitchValue()
