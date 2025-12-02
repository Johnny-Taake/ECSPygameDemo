class GameObject:
    """
    A GameObject represents an object in the game world.
    It's a container that holds different components like position,
    graphics, physics, etc. following the Entity-Component-System pattern.
    """
    def __init__(self):
        self.components: dict = {}

    def add(self, component):
        """Add a component to this game object."""
        self.components[type(component)] = component
        return self

    def get(self, component_type):
        """Get a component of the specified type from this game object."""
        return self.components.get(component_type)
