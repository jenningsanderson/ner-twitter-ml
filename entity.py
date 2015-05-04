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
        return {'word': features['Word']}


class Facility(Entity):
    def __init__(self):
        self.name = "Facility"

    def featurize(self, features):
        return {'word': features['Word']}


class Person(Entity):
    def __init__(self):
        self.name = "Person"

    def featurize(self, features):
        return {'word': features['Word'],
                'Pronoun'   : features['Pronoun'],'I'   : features['I'],'We'   : features['We'],'Self'   : features['Self'],
                'You'   : features['You'],'Other'   : features['Other'],
                'Social'   : features['Social'], 'othref':features['Othref']}

class Artifact(Entity):
    def __init__(self):
        self.name = "Artifact"

    def featurize(self, features):
        return {'word': features['Word']}
