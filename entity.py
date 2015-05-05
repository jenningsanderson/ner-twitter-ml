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
    def __init__(self):
        self.name = "Location"

    def featurize(self, features):
        return {'word': features['Word'],
                'Quote': features['Quote'],'Space': features['Space'],'Article':features['Article'],'Preps':features['Preps'],'Incl':features['Incl'],'Affect':features['Affect'],
                'Posemo':features['Posemo'],
                'Caps':features['Caps'],'POS':features['POS'],'Dep_rel':features['Dep_rel'],'Dep_head':features['Dep_head']
}



class Organization(Entity):
    def __init__(self):
        self.name = "Organization"

    def featurize(self, features):
        return {'word': features['Word'],
                'Pronoun'   : features['Pronoun'],'Social'   : features['Social'],'Othref'   : features['Othref'],'Article':features['Article'],
                'OtherP'   : features['OtherP'],'Comma': features['Comma'],'Leisure'   : features['Leisure'],'Job':features['Job'],'Occup':features['Occup'],
                'Caps':features['Caps'],'POS':features['POS'],'Dep_rel':features['Dep_rel'],'Dep_head':features['Dep_head']
}



class Facility(Entity):
    def __init__(self):
        self.name = "Facility"

    def featurize(self, features):
        return {'word': features['Word'],
                'Space'   : features['Space'],'Leisure'   : features['Leisure'],'Incl'   : features['Incl'],'Home'   : features['Home'],
                'Leisure'   : features['Leisure'],'Quote': features['Quote'],'Article':features['Article'],'Preps':features['Preps'],
                'Caps':features['Caps'],'POS':features['POS'],'Dep_rel':features['Dep_rel'],'Dep_head':features['Dep_head']
}





class Person(Entity):
    def __init__(self):
        self.name = "Person"

    def featurize(self, features):
        #return features
        
        return {'word': features['Word'],
                'Pronoun'   : features['Pronoun'],'self':features['Self'],'Othref':features['Othref'],
                'Social'   : features['Social'],
                'Caps':features['Caps'],'POS':features['POS'],'Dep_rel':features['Dep_rel'],'Dep_head':features['Dep_head']
}



class Artifact(Entity):
    def __init__(self):
        self.name = "Artifact"

    def featurize(self, features):
        return {'word': features['Word'],
                'OtherP'   : features['OtherP'],'Preps':features['Preps'],
                'Article':features['Article'],'Space' : features['Space'],'Leisure'   : features['Leisure'], 'Home'   : features['Home'],
                'Caps':features['Caps'],'POS':features['POS'],'Dep_rel':features['Dep_rel'],'Dep_head':features['Dep_head']
}
