class StructuralError(Exception):
    response: str

    def __init__(self, r):
        self.response = r
