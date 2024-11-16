import math, time, os
from modules.lsystem_class import LSystem

def load_system(l_sys_text, start, length, ratio):
    st = time.time()
    with open(l_sys_text) as f:
        name = os.path.basename(l_sys_text).split('.')[0]            
        axiom = f.readline()
        numRules = int(f.readline())
        rules = {}
        for i in range(numRules):
            rule = f.readline().split(' ')
            rules[rule[0]] = rule[1]
        dTheta = math.radians(int(f.readline()))
        system = LSystem(name, axiom, rules, dTheta, start, length, ratio)
    return system
