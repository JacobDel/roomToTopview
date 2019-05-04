from rpw import db

def getObjects():
    # levels = db.Collector(of_category='Levels', is_type=True)
    walls = db.Collector(of_class='Wall', where=lambda x: x.parameters['Length'] > 5)
    desks = db.Collector(of_class='FamilyInstance', level='Level 1')
    windows = db.Collector(of_class='Window')
    return windows,walls,desks

def equalsBIM(rWalls,rWindows,rDesks):
    #copy the objects
    qWalls = rWalls
    qWindows=rWindows
    qDesks=rDesks

    #get BIM objects
    bWindows,bWalls,bDesks=getObjects()

    #go through every object in our BIM & search an equal object
    print("Compare walls..")
    compareObjectLists(qWalls,bWalls)
    print("Compare desks..")
    compareObjectLists(qDesks,bDesks)
    print("Compare windows..")
    compareObjectLists(qWindows,bWindows)

def compareObjectLists(copyList,bimList): #compare a category of objects from the bim model and a copylist (a copy of the objects in that category we found)
    for bimobj in bimList:
        # improve this algorithm to also accept objects with slightly variation on size
        found=False
        for i in range(0,len(copyList)):
            if(copyList[i]==bimobj):
                found=True
                break
        if(found==False):
            print("Could not find the following object from our BIM model: ")
            print(bimobj)
    if(len(copyList)>0):
        print("There are new objects in the room: ")
        for obj in copyList:
            print obj