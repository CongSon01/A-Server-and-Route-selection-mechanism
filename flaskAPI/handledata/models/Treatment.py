class Treatment(object):
    """Treatment array holds each instruction object"""
    def __init__(self):
        self.instructions = []

    def set_instructions(self, instruction_object):
        self.instructions.append( instruction_object )

    def get_instructions(self):
        return self.instructions


