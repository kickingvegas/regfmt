class Field:
    def __init__(self, config=None):
        self.name: str = None
        self.width: int = None
        self.start: int = None
        self.end: int = None

        if config:
            self.name = config['name'] if 'name' in config else None
            if 'width' in config and type(config['width']) == type(1):
                self.width = config['width']
            else:
                # TODO: throw error
                pass
