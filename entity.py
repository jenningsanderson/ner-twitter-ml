from binary_learner import Entity

class Location(Entity):
    def __init__(self):
        self.name = "Location"

    def __call__(self, text):
        yield text
        if text[0].isupper():
            yield "Capped"




class Organization(Entity):
    def __init__(self):
        self.name = "Organization"

    # def __call__(self, text):





class Facility(Entity):
    def __init__(self):
        self.name = "Facility"

    # def __call__(self, text):





class Person(Entity):
    def __init__(self):
        self.name = "Person"

    # def __call__(self, text):





class Artifact(Entity):
    def __init__(self):
        self.name = "Artifact"

    # def __call__(self, text):