import itertools

# Cities
cities = ["A", "B", "C", "D", "E", "F"]

# Distance matrix
distances = {
    ("A", "A"): 0, ("A", "B"): 10, ("A", "C"): 15, ("A", "D"): 20, ("A", "E"): 25, ("A", "F"): 30,
    ("B", "A"): 10, ("B", "B"): 0, ("B", "C"): 35, ("B", "D"): 25, ("B", "E"): 17, ("B", "F"): 28,
    ("C", "A"): 15, ("C", "B"): 35, ("C", "C"): 0, ("C", "D"): 30, ("C", "E"): 28, ("C", "F"): 40,
    ("D", "A"): 20, ("D", "B"): 25, ("D", "C"): 30, ("D", "D"): 0, ("D", "E"): 22, ("D", "F"): 16,
    ("E", "A"): 25, ("E", "B"): 17, ("E", "C"): 28, ("E", "D"): 22, ("E", "E"): 0, ("E", "F"): 35,
    ("F", "A"): 30, ("F", "B"): 28, ("F", "C"): 40, ("F", "D"): 16, ("F", "E"): 35, ("F", "F"): 0,
}

def route_distance(route):
    total = 0
    for i in range(len(route) - 1):
        total += distances[(route[i], route[i+1])]
    return total


other_cities = ["B", "C", "D", "E", "F"]
shortest_route = None
min_distance = float("inf")

for perm in itertools.permutations(other_cities):
    route = ("A",) + perm + ("A",)
    dist = route_distance(route)
    if dist < min_distance:
        min_distance = dist
        shortest_route = route

# Print result
print("Shortest Route:", " -> ".join(shortest_route))
print("Total Distance:", min_distance)
