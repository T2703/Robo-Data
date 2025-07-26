class FormattedMoveData:
    def __init__(self, _input, move, damage, guard, invincibility, startup,
                 block, active, recovery, frc_window, proration,
                 guard_bar_plus, guard_bar_minus, level, images, hitboxes_images, meter_images):
        self.input = _input
        self.move = move
        self.damage = damage
        self.guard = guard
        self.invincibility = invincibility
        self.startup = startup
        self.block = block
        self.active = active
        self.recovery = recovery
        self.frc_window = frc_window
        self.proration = proration
        self.guard_bar_plus = guard_bar_plus
        self.guard_bar_minus = guard_bar_minus
        self.level = level
        self.images = images
        self.hitboxes_images = hitboxes_images
        self.meter_images = meter_images

    def __str__(self):
        return (
            f"Input: {self.input}\n"
            f"Name: {self.move}\n"
            f"Damage: {self.damage}\n"
            f"Guard: {self.guard}\n"
            f"Invincibility: {self.invincibility}\n"
            f"Startup: {self.startup}\n"
            f"Active: {self.active}\n"
            f"Recovery: {self.recovery}\n"
            f"Block: {self.block}\n"
            f"FRC Window: {self.frc_window}\n"
            f"Proration: {self.proration}\n"
            f"Guard Bar +: {self.guard_bar_plus}\n"
            f"Guard Bar -: {self.guard_bar_minus}\n"
            f"Level: {self.level}\n"
            f"Images: {self.images}\n"
            f"Hitboxes: {self.hitboxes_images}\n"
            f"Meter: {self.meter_images}\n"
        )
