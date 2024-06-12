import arcade


class EmitterHandler:
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
