LETR={1:'A','2':'B','3':'C','4':'D','5':'E','6':'F','7':'G','8':'H' }

def to_letr(ch):
    return {
        '1':"A",
        '2':"B",
        '3':"C",
        '4':"D",
        '5':"E",
        '6':"F",
        '7':"G",
        '8':"H",      

    }.get(ch)
c=0
text=to_letr(str(c+1))
print(text)