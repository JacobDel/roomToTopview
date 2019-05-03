from rpw import db
def getObjects():
    levels = db.Collector(of_category='Levels', is_type=True)
    walls = db.Collector(of_class='Wall', where=lambda x: x.parameters['Length'] > 5)
    desks = db.Collector(of_class='FamilyInstance', level='Level 1')
    return levels,walls,desks
