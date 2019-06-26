import math


class Node:

    def __init__(self, x, y, r, canvas):
        self.x = x
        self.y = y
        self.r = r
        self.selected = False
        self.canvas = canvas
        self.children = []
        self.d = None
        self.r3 = None
        self.dtheta = None
        self.tlen = None

    def append(self, c):
        self.children.append(c)
        largest = self if self.r >= c.r else c
        smallest = self if self.r < c.r else c
        c.d = math.hypot(smallest.x - largest.x, smallest.y - largest.y)
        c.r3 = largest.r - smallest.r
        c.dtheta = math.asin(c.r3 / c.d)
        c.tlen = math.sqrt((c.d * c.d) - (c.r3 * c.r3))

    def leaves(self):
        if self.children:
            lvs = []
            for c in self.children:
                clvs = c.leaves()
                lvs += clvs
            return lvs
        else:
            return [self]

    def all(self):
        return [self] + [y for x in
                         [c.all() for c in self.children]
                         for y in x]

    def check_for_click(self, x, y):
        dx = x-self.x
        dy = y-self.y
        d = math.sqrt(dx*dx+dy*dy)
        return d < self.r

    def draw(self):
        color = 'yellow' if self.selected else ''
        self.canvas.create_oval(self.x-self.r, self.y-self.r,
                                self.x+self.r, self.y+self.r,
                                fill=color)
        for c in self.children:
            largest = self if self.r >= c.r else c
            smallest = self if self.r < c.r else c
            theta = math.atan2(largest.y-smallest.y, largest.x-smallest.x)

            if c.r3:
                theta1 = theta + c.dtheta
                theta2 = theta - c.dtheta
                tan1 = [smallest.x, smallest.y, smallest.x+c.tlen*math.cos(theta1), smallest.y+c.tlen*math.sin(theta1)]
                tan2 = [smallest.x, smallest.y, smallest.x+c.tlen*math.cos(theta2), smallest.y+c.tlen*math.sin(theta2)]
                s = smallest.r / c.r3
                delta1 = [s*(tan1[2] - largest.x), s*(tan1[3] - largest.y)]
                delta2 = [s*(tan2[2] - largest.x), s*(tan2[3] - largest.y)]
            else:
                tan1 = [smallest.x, smallest.y, largest.x, largest.y]
                tan2 = [smallest.x, smallest.y, largest.x, largest.y]
                s = smallest.r / c.d
                delta1 = [s*(largest.y - smallest.y), -s*(largest.x - smallest.x)]
                delta2 = [-s*(largest.y - smallest.y), s*(largest.x - smallest.x)]
            tan1 = [
                tan1[0] + delta1[0],
                tan1[1] + delta1[1],
                tan1[2] + delta1[0],
                tan1[3] + delta1[1],
            ]
            tan2 = [
                tan2[0] + delta2[0],
                tan2[1] + delta2[1],
                tan2[2] + delta2[0],
                tan2[3] + delta2[1],
            ]
            self.canvas.create_line(*tan1)
            self.canvas.create_line(*tan2)
            c.draw()
