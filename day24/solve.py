import sys

IMMUNE = True
INFECTION = False
army_name = {IMMUNE:'Immune',INFECTION:'Infection'}
attack_types = ['fire', 'bludgeoning', 'cold', 'radiation', 'slashing']
NATO = {'A':'Alpha', 'B':'Bravo','C':'Charlie', 'D':'Delta', 'E':'Echo', 'F':'Foxtrot', 'G':'Golf',"H":"Hotel", 'I':'India', 'J':'Juliet', 'K':'Kilo', 'L':'Lima', 'M':'Mike', 'N':'November', 'O':'Oscar', 'P':'Papa', 'Q':'Quebec', 'R':'Romeo', 'S':'Sierra', 'T':'Tango', 'U':'Uniform', 'V':'Victor', 'W':'Whiskey', 'X':'Xray', 'Y':'Yankee', 'Z':'Zulu'}

class Group:
    id = {IMMUNE : 0, INFECTION : 0}
    def __init__(self,system,description,boost):
        self.system = system
        self.id = Group.id[system]
        Group.id[system] += 1
        self.dead = False
        words = description.split()
        self.units = int(words[0])
        self.hp = int(words[4])
        does = words.index('does')
        self.damage = int(words[does+1])+boost
        self.damage_type = words[does+2]
        self.initiative = int(words[does+6])
        self.weakness = []
        self.immunity = []
        self.target = None
        try:
            typestr = line[line.index('(')+1:line.index(')')]
            typelst = [x.strip() for x in typestr.split(';')]
            for kind in typelst:
                parsing = self.weakness if kind[0] == 'w' else self.immunity
                for attack in attack_types:
                    if kind.find(attack) >= 0:
                        parsing.append(attack)
        except ValueError:
            pass

    def __str__(self):
        out = self.title()
        if self.dead:
            out += 'is DEAD'
            return out
        out += '\n '+str(self.units)+' units'
        out += '\n '+str(self.hp) + ' hit points'
        out += '\n '+str(self.damage) + ' ' + self.damage_type + ' damage'
        out += ' (effective power ' + str(self.power()) + ')'
        out += '\n '+str(self.initiative) + ' initiative'
        out += '\n weaknesses:' + str(self.weakness)
        out += '\n immunities:' + str(self.immunity)
        return out

    def title(self):
        return army_name[self.system] + ' unit ' + NATO[chr(ord('A') + self.id)]

    def power(self):
        return self.units * self.damage

    def choose_target(self,targets):
        """Choose a target from the targets list, and remove it from the list"""
        if self.dead or targets == []:
            self.target = None
            return

        self.target = max(targets,
                            key = lambda g :
                                (self.damage_to(g), g.power(), g.initiative))
        if self.damage_to(self.target) == 0:
            # can't hurt any group, target None
            self.target = None
        else:
            targets.remove(self.target)

    def damage_to(self,opponent):
        """Return damage done by this group to opponent group."""
        if self.dead:
            return 0
        if opponent == None:
            return 0
        if self.damage_type in opponent.immunity:
            return 0
        if self.damage_type in opponent.weakness:
            return 2*self.power()
        return self.power()

    def take_hit(self,damage):
        kill = damage/self.hp
        self.units = max(self.units - kill, 0)
        out = self.title()+' took '+str(kill)+' damage'
        if self.units == 0:
            self.dead = True
            out += ' and is DEAD!'
        print out

    def attack(self):
        """Deal damage to current target."""
        if self.dead or self.target == None:
            return
        print self.title(),'is attacking'
        d = self.damage_to(self.target)
        self.target.take_hit(d)


#
# Read data
#        
filename = sys.argv[1]
try:
    boost = int(sys.argv[2])
except:
    boost = 0
data = open(filename).readlines()

army = {}
army[IMMUNE] = []
army[INFECTION] = []
allgroups = []
for line in data:
    if line[:3] == 'Imm':
        system = IMMUNE
        continue
    if line[:3] == 'Inf':
        system = INFECTION
        continue
    if line.strip() == '':
        continue

    g = Group(system,line,boost if system == IMMUNE else 0)
    army[system].append(g)
    allgroups.append(g)

    print g
    print

# Battle!
alive = {INFECTION: True, IMMUNE: True}
round = 0
while alive[INFECTION] and alive[IMMUNE]:
    print
    print '='*12
    print 'Round',round
    print '='*12
    # Target selection phase
    targets = {}
    targets[IMMUNE] = [x for x in army[INFECTION] if not x.dead]
    targets[INFECTION] = [x for x in army[IMMUNE] if not x.dead]

    allgroups.sort(key = lambda g : (g.power(),g.initiative), reverse=True)
    for g in allgroups:
        print g.title(),'with',g.units,'units'
        g.choose_target(targets[g.system])
        print '  will attack '+('None' if not g.target else g.target.title()),
        print 'for',g.damage_to(g.target),'damage'

    # Attack phase
    for g in sorted(allgroups, key = lambda g : g.initiative, reverse = True):
        g.attack()

    # Victory check
    for system in alive:
        alive[system] = False
        for g in army[system]:
            if not g.dead:
                alive[system] = True
    round += 1

print
print '='*12
print 'Final outcome (boost %d)' % boost
print '='*12
for system in alive:
    if alive[system]:
        winunits = 0
        for g in army[system]:
            print g
            winunits += g.units
        print army_name[system],'has',winunits,'remaining.'
    else:
        print army_name[system],'was destroyed.'

        
    
