class Entity:
    def __init__(self):
        self.components: dict = {}

    def add(self, component):
        self.components[type(component)] = component
        return self

    def get(self, component_type):
        return self.components.get(component_type)
