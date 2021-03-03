class EventHandler:
    def __init__(self, camera, renderer, animator):
        self.camera = camera
        self.renderer = renderer
        self.animator = animator
    def keyEvent(self, event):
        if event.char == 'a':
            self.camera.move([-0.5, 0, 0])
            self.renderer.update()
        elif event.char == 'd':
            self.camera.move([0.5, 0, 0])
            self.renderer.update()
        elif event.char == 'w':
            self.camera.move([0, 0.5, 0])
            self.renderer.update()
        elif event.char == 's':
            self.camera.move([0, -0.5, 0])
            self.renderer.update()
        elif event.char == 'q':
            self.camera.move([0, 0, 0.5])
            self.renderer.update()
        elif event.char == 'e':
            self.camera.move([0, 0, -0.5])
            self.renderer.update()
        elif event.char == 'c':
            self.renderer.changeProjection()
            self.renderer.update()
    def update(self):
        self.animator.update()
        #self.renderer.update()