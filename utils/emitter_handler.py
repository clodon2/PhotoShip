import arcade


class EmitterHandler:
    """Handles multiple emitters, sort of like a list for them"""
    def __init__(self):
        self.emitters = []

    def add_emitter(self, emitter):
        self.emitters.append(emitter)

    def draw(self):
        for emitter in self.emitters:
            emitter.draw()

    def on_update(self):
        for emitter in self.emitters:
            emitter.update()
