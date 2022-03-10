def DFS(element, l):
    found = False
    visited = {}
    toVisit = [start]
    while toVisit.size() > 0 and not found:
        (x, y) = toVisit.pop(0)
        visited[(x, y)] = 1

        if (x, y) == element:
            found = true
        else:
            children = []
            for child in ...: # every direction
                if ok(child) # accesible, inside the map, unvisited
                    chidlren.append(child)
            toVisit = children + toVisit
    return found
            
