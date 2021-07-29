class BoardCoord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return BoardCoord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return BoardCoord(self.x - other.x, self.y - other.y)

    def __str__(self):
        return str(self.x) + ", " + str(self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def get_tuple(self):
        return self.x, self.y
