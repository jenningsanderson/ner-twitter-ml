from learner import Entity

"""
'Key','Filename','Segment','Word','WC','WPS','Sixltr','Dic','Unique','Abbreviations','Emoticons','Pronoun','I','We',
                            'Self','You','Other','Negate','Assent','Article','Preps','Number','Affect','Posemo','Posfeel','Optim','Negemo',
                            'Anx','Anger','Sad','Cogmech','Cause','Insight','Discrep','Inhib','Tentat','Certain','Senses','See','Hear', 'Feel',
                            'Social','Comm','Othref','Friends','Family','Humans','Time','Past','Present','Future','Space','Up','Down','Incl',
                            'Excl','Motion','Occup','School','Job','Achieve','Leisure','Home','Sports','TV','Music','Money','Metaph','Relig',
                            'Death','Physcal','Body','Sexual','Eating','Sleep','Groom', 'Swear','Nonfl','Fillers',  'Period','Comma','Colon',
                            'SemiC','QMark','Exclam','Dash','Quote','Apostro','Parenth','OtherP',   'AllPct','Caps','POS','Dep_rel','Dep_head', Artifact    Facility
    'Artifact', 'Facility', 'Organization','Location','Person'
"""
class Location(Entity):
    def __init__(self, features):
        self.name = "Location"
        self.liwc = ['Quote','Space','Article','Preps','Incl','Affect','Posemo']
        
        self.build_features(features)


class Organization(Entity):
    def __init__(self, features):
        self.name = "Organization"
        self.liwc = ['Social','Othref','Article','Leisure']

        self.build_features(features)


class Facility(Entity):
    def __init__(self, features):
        self.name = "Facility"
        self.liwc = ['Space', 'Incl','Leisure','Home','Quote','Article','Preps']

        self.build_features(features)

class Person(Entity):
    def __init__(self, features):
        self.name = "Person"
        self.liwc = ['Pronoun','self','Othref','Social']

        self.build_features(features)


class Artifact(Entity):
    def __init__(self, features):
        self.name = "Artifact"
        self.liwc = ['OtherP','Preps','Article','Space','Leisure','Home']

        self.build_features(features)
