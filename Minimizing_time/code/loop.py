class LoopDetected(Exception):
    def __init__(self):
        super().__init__("Loop is present")