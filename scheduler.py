from z3 import *

class Schedule:
    def __init__(self):
        self.solver = Solver()
        # Names of Staffers
        self.names = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Jim", "Kristin", "Lloyd", "Mike", "Nathan", "Oscar", "Papa", "Quebec", "Ronald", "Sierra", "Ted", "Ursula", "Victor", "Wendy", "Xavier", "Yvonne", "Zulu"]
        self.day1Puzzles = ["ALPHA", "BRAVO", "CHARLIE", "DELTA", "ECHO", "FOXTROT", "GOLF", "HOTEL", "INDIA"]
        self.day2Puzzles = ["JULIET", "KILO", "LIMA", "MIKE", "NOVEMBER", "OSCAR", "PAPA"]
        self.allPuzzles = self.day1Puzzles + self.day2Puzzles
        self.scheduled = {}
        for p in self.allPuzzles:
            self.scheduled[p] = {}
            for n in self.names:
                self.scheduled[p][n] = Bool(p + n)

    def MutuallyExclude(self, firstPuzzle, secondPuzzle):
        for n in self.names:
            self.solver.add(Not(And(self.scheduled[firstPuzzle][n], self.scheduled[secondPuzzle][n])))

    def StaffCount(self, puzzle, desired):
        count = 0
        for n in self.names:
            count = count + If(self.scheduled[puzzle][n], 1, 0)
        self.solver.add(count == desired)

    def Unavailable(self, name, puzzle):
        self.solver.add(Not(self.scheduled[puzzle][name]))

    def __countStaffedPuzzles(self, name, puzzleNames):
        count = 0
        for p in puzzleNames:
            count = count + If(self.scheduled[p][name], 1, 0)
        return count

    def MaxDay1Puzzles(self, name, max):
        self.solver.add(self.__countStaffedPuzzles(name, self.day1Puzzles) <= max)

    def MaxDay2Puzzles(self, name, max):
        self.solver.add(self.__countStaffedPuzzles(name, self.day2Puzzles) <= max)

    def MaxTotalPuzzles(self, name, max):
        self.solver.add(self.__countStaffedPuzzles(name, self.allPuzzles) <= max)

    def OnlyOneDay(self, name):
        self.solver.add(Or(self.__countStaffedPuzzles(name, self.day1Puzzles) == 0, self.__countStaffedPuzzles(name, self.day2Puzzles) == 0))

    def Require(self, name, puzzle):
        self.solver.add(self.scheduled[puzzle][name])

    def MinTotalPuzzlesForAll(self, min):
        for n in self.names:
            self.solver.add(self.__countStaffedPuzzles(n, self.allPuzzles) >= min)

    def PrintSchedule(self):
        print(self.solver.check())
        m = self.solver.model()

        # Print the puzzle schedule
        for p in self.allPuzzles:
            print(p + ": ", end="")
            staff = []
            for n in self.names:
                if m[self.scheduled[p][n]]:
                    staff.append(n)
            print(*staff, sep=', ')
        print("")

        # Print the staffer schedule
        for n in self.names:
            print(n + ": ", end="")
            puzz = []
            for p in self.allPuzzles:
                if m[self.scheduled[p][n]]:
                    puzz.append(p)
            print(*puzz, sep=', ',)



# Hypothetical Schedule:
# Day 1
# 8:00      9:00        10:00       11:00       12:00       13:00       14:00       15:00       16:00       17:00       18:00
# ALPHA     ALPHA       ALPHA
#           BRAVO       BRAVO
#           CHARLIE     CHARLIE     CHARLIE
#                                   DELTA       DELTA       DELTA
#                                               ECHO        ECHO        ECHO
#                                                           FOXTROT     FOXTROT     FOXTROT     FOXTROT     FOXTROT
#                                                                       GOLF        GOLF        GOLF
#                                                                                   HOTEL       HOTEL       HOTEL       HOTEL
#                                                                                                           INDIA       INDIA

# Day 2
# 8:00      9:00        10:00       11:00       12:00       13:00       14:00       15:00       16:00       17:00       18:00
# JULIET    JULIET      JULIET
# KILO      KILO        KILO
#           LIMA        LIMA        LIMA        LIMA
#                       MIKE        MIKE        MIKE        MIKE
#                                               NOVEMBER    NOVEMBER    NOVEMBER
#                                                           OSCAR       OSCAR       OSCAR       OSCAR 
#                                                                                   PAPA        PAPA        PAPA        PAPA

s = Schedule()

s.MinTotalPuzzlesForAll(1)

s.StaffCount("ALPHA", 3)
s.StaffCount("BRAVO", 2)
s.StaffCount("CHARLIE", 5)
s.StaffCount("DELTA", 2)
s.StaffCount("ECHO", 1)
s.StaffCount("FOXTROT", 4)
s.StaffCount("GOLF", 2)
s.StaffCount("HOTEL", 3)
s.StaffCount("INDIA", 1)
s.StaffCount("JULIET", 2)
s.StaffCount("KILO", 2)
s.StaffCount("LIMA", 4)
s.StaffCount("MIKE", 2)
s.StaffCount("NOVEMBER", 3)
s.StaffCount("OSCAR", 2)
s.StaffCount("PAPA", 2)

# Day 1
s.MutuallyExclude("ALPHA", "BRAVO")
s.MutuallyExclude("BRAVO", "CHARLIE")
s.MutuallyExclude("ALPHA", "CHARLIE")
s.MutuallyExclude("CHARLIE", "DELTA")
s.MutuallyExclude("DELTA", "ECHO")
s.MutuallyExclude("DELTA", "FOXTROT")
s.MutuallyExclude("ECHO", "FOXTROT")
s.MutuallyExclude("ECHO", "GOLF")
s.MutuallyExclude("FOXTROT", "GOLF")
s.MutuallyExclude("FOXTROT", "HOTEL")
s.MutuallyExclude("FOXTROT", "INDIA")
s.MutuallyExclude("GOLF", "HOTEL")
s.MutuallyExclude("HOTEL", "INDIA")

# Day 2
s.MutuallyExclude("JULIET", "KILO")
s.MutuallyExclude("JULIET", "LIMA")
s.MutuallyExclude("JULIET", "MIKE")
s.MutuallyExclude("KILO", "LIMA")
s.MutuallyExclude("KILO", "MIKE")
s.MutuallyExclude("LIMA", "MIKE")
s.MutuallyExclude("LIMA", "NOVEMBER")
s.MutuallyExclude("MIKE", "NOVEMBER")
s.MutuallyExclude("MIKE", "OSCAR")
s.MutuallyExclude("NOVEMBER", "OSCAR")
s.MutuallyExclude("OSCAR", "PAPA")

# ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Jim", "Kristin", "Lloyd", 
# "Mike", "Nathan", "Oscar", "Papa", "Quebec", "Ronald", "Sierra", "Ted", "Ursula", "Victor", "Wendy", "Xavier", "Yvonne", "Zulu"]

# Arbitrary scheduling constraints
for n in ["Alice", "Bob", "Carol", "David", "Eve", "Frank"]:
    s.OnlyOneDay(n)

s.MaxTotalPuzzles("Alice", 1)
s.MaxTotalPuzzles("Bob", 2)
s.Require("Carol", "CHARLIE")
s.Unavailable("David", "ECHO")
s.Unavailable("David", "LIMA")

for n in ["Grace", "Heidi", "Ivan", "Jim", "Kristin", "Lloyd"]:
    s.MaxDay1Puzzles(n, 1)
    s.MaxDay2Puzzles(n, 1)

for n in ["Mike", "Nathan", "Oscar", "Papa", "Quebec", "Ronald", "Sierra"]:
    s.MaxTotalPuzzles(n, 2)

s.PrintSchedule()