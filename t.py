
def check( item : object) -> bool:

    condition = item is None

    if ( condition):
        print("Item is None:",item)
    
    if(not condition):
        print("Item is:",type(item))

a : object = None
check(a)

a = 89
check(a)