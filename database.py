from tinydb import TinyDB, Query
import random
db = TinyDB('primers.json')
position_table= db.table("Position")

MAX_ROW=10
MAX_COLUMN=10
MAX_BOX=10

# This function returns (Success, Existing, Position)
# Add the primer if it doesn't already exist
# If the primer already exists, return (Failure, Existing, None)
# If primer was added successfully, return (Success, None, Added Position)
def addPrimer(id, gene, species, dye, placement):
    existing = db.search(Query().id==id)
    if (len(existing)):
        return (False, existing, None)
    pos = nextEmptyPosition()
    db.insert({'position': pos, 'id': id, 'gene': gene, 'species': species, 'dye': dye, 'placement':placement})
    return (True, None, pos)

# return the next empty position to put primer into  
def nextEmptyPosition():
    for b in range(MAX_BOX):
        for r in range(MAX_ROW):
            for c in range(MAX_COLUMN):
                if positionEmpty(b, r, c):
                    empty_pos = {'Box': b+1, 'Row': chr(65+r), 'Column': c+1}
                    position_table.insert(empty_pos)
                    print(empty_pos)
                    return empty_pos

# check if the given position is empty or not
def positionEmpty(box, row, column):
    filled_pos = position_table.get(Query().fragment({'Box': box+1, 'Row': chr(65+row), 'Column': column+1}))
    return filled_pos == None

# search for the primer by gene
# return a list of primers match the gene
def lookUp(gene):
    return db.search(Query().gene==gene)

def getAll():
    return db.all()

def clean():
    db.truncate()
    position_table.truncate()

# clean()
def createData():
    for x in range(200):
        i = random.randint(0,100)
        db.insert({'position': {'Box':i+1, 'Row':chr(65+i), 'Column':i}, 'id': i, 'gene': i, 'species': i, 'dye': i, 'placement':i})
# createData()