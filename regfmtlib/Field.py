class Field:
    def __init__(self, config=None):
        self.name: str = None
        self.width: int = None
        self.leftIndex: int = None
        self.rightIndex: int = None

        if config:
            self.name = config['name']
            if 'width' in config:
                self.width = config['width']
            else:
                # TODO: throw error
                pass
