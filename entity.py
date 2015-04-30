from binary_learner import Entity

class Location(Entity):
    def __init__(self):
        self.name = "Location"

    def featurize(self, features):
        return {'word' : features['Word'],
                'school': features['School']}




class Organization(Entity):
    def __init__(self):
        self.name = "Organization"

    def featurize(self, features):
        return features





class Facility(Entity):
    def __init__(self):
        self.name = "Facility"

    def featurize(self, features):
        return features






class Person(Entity):
    def __init__(self):
        self.name = "Person"

    def featurize(self, features):
        return {'word': features['Word'],
                'I'   : features['I']}





class Artifact(Entity):
    def __init__(self):
        self.name = "Artifact"

    def featurize(self, features):
        return features
