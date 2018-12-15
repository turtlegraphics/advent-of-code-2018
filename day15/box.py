#
# Boxes on the board
#
import color

class Box():
    def __init__(self,c):
        self.c = c

    def __str__(self):
        return self.c

class Wall(Box):
    def __init__(self):
        Box.__init__(self,'#')

class Empty(Box):
    def __init__(self):
        Box.__init__(self,'.')

class Unit(Box):
    def __init__(self,race):
        Box.__init__(self,race)
        self.hp = 200
        self.moved = False

    def __str__(self):
        return color.fade(self.c,self.hp)

    def hurt(self):
        """Returns True if killed."""
        self.hp -= 3
        if self.hp <= 0:
            return True
        return False

class Elf(Unit):
    def __init__(self):
        Unit.__init__(self,'E')

    def enemy(self):
        return Gnome

class Gnome(Unit):
    def __init__(self):
        Unit.__init__(self,'G')

    def enemy(self):
        return Elf

if __name__=="__main__":
    g = Gnome()
    e = Elf()
    print g.enemy()
    print e.enemy()
