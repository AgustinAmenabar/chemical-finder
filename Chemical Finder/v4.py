import math
about = '''
#ABOUT
This is an "original" project, made by Albert Agustin Amenabar!
It helps you find formulas of ionic compounds and acids from name, and even determine chemical equations for you.
As a bonus, you may get balanced equations!
#HISTORY
The latest entry is the last update to this program of the version you have.
4/9/2023 v1: Started the project.
* Made a somewhat working system to find ionic compound formulas from their names, along with acids.
* Also tried implementing the typical acid-base reaction without balancing yet.
5/9/2023 v2:
* Added a working balancing system, up to a coefficient limit (set to 10) due to efficiency limitations.
* Cleaned up code a lil' bit.
* Added more ions and products, and implemented acid-metal reactions (they are easier).
6/9/2023 v3:
* Implemented general single displacement reactions (does not yet take into account reactivities).
* Implemented more failsafe measures.
13/10/2023 v4: Completely revamped the code, now using mainly classes.
* Improved the balancing code.
* Implemented water reactions and basic ionic compound synthesis reactions, and generalised previous reactions to just double-displacements.
* Added diatomification of all species that can (hydrogen and most anion elements).
* Implemented adjustable cation oxidation states in input.
* Added hydride and various other ions, and implemented alternative/colloquial names for species.
* Turned some common errors into exceptions (messages for the user to try again).
* And MORE...
<end>
'''
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
species = []
testing_case = False
last_update = '13/10/2023'
debug = False
limit = 10 ##################################################LIMIT
elementies = {}
moleculies = {}

#this is periodic table of ions
charges = {
    'hydrogen': [1, False],
    'alkali1': [1, True],
    'alkali2': [2, True],
    'transition': [2, True],
    'posttransition': [3, True],
    'metalloid': [4, False],
    'pnictogen': [-3, True],
    'chalcogen': [-2, True],
    'halogen': [-1, True],
    'noble': [None, True],
}

states = {
    'hydrogen': 3,
    'alkali1': 1,
    'alkali2': 1,
    'transition': 1,
    'posttransition': 1,
    'metalloid': 1,
    'pnictogen': 1,
    'chalcogen': 1,
    'halogen': 3,
    'noble': 3,
}
Families = {
    'hydrogen': [1], #coolest exception
    'alkali1': [3, 11, 19, 37, 55, 87],
    'alkali2': [4, 12, 20, 38, 56, 88],
    'transition': [
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
    39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
    72, 73, 74, 75, 76, 77, 78, 79, 80],
    'posttransition': [13, 31, 49, 50, 81, 82, 83, 84],
    'metalloid': [5, 6, 14, 32, 33, 51],
    'pnictogen': [7, 15],
    'chalcogen': [8, 16, 34, 52],
    'halogen': [7, 9, 15, 17, 35, 53, 85],
    'noble': [2, 10, 18, 36, 54, 86],
}
charge_exceptions = [
    [5, 3],
    [47, 1],
    [82, 2],
]

state_exceptions = [
    [7, 3],
    [8, 3],
    [80, 2],
]

elements = [
    ('hydr!ogen', 'H', 1.008),
    ('helium', 'He', 4.003),
    ('lithium', 'Li', 6.94),
    ('beryllium', 'Be', 9.012),
    ('boron', 'B', 10.81),
    ('carb!on', 'C', 12.01),
    ('nitr!ogen', 'N', 14.01),
    ('ox!ygen', 'O', 16),
    ('fluor!ine', 'F', 19),
    ('neon', 'Ne', 20.18),
    ('sodium', 'Na', 22.99),
    ('magnesium', 'Mg', 24.31),
    ('aluminium', 'Al', 26.98),
    ('silicon', 'Si', 28.09),
    ('phosph!orus', 'P', 30.97),
    ('sulf!ur', 'S', 32.06),
    ('chlor!ine', 'Cl', 35.45),
    ('argon', 'Ar', 39.95),
    ('potassium', 'K', 39.1),
    ('calcium', 'Ca', 40.08),
    ('scandium', 'Sc', 44.96),
    ('titanium', 'Ti', 47.87),
    ('vanadium', 'V', 50.94),
    ('chromium', 'Cr', 52),
    ('manganese', 'Mn', 54.94),
    ('iron', 'Fe', 55.85),
    ('cobalt', 'Co', 58.93),
    ('nickel', 'Ni', 58.69),
    ('copper', 'Cu', 63.55),
    ('zinc', 'Zn', 65.38),
    ('gallium', 'Ga', 69.72),
    ('germanium', 'Ge', 72.63),
    ('arsen!ic', 'As', 74.92),
    ('selen!ium', 'Se', 78.97),
    ('brom!ine', 'Br', 79.9),
    ('krypton', 'Kr', 83.8),
    ('rubidium', 'Rb', 85.47),
    ('strontium', 'Sr', 87.62),
    ('yttrium', 'Y', 88.91),
    ('zirconium', 'Zr', 91.22),
    ('niobium', 'Nb', 92.91),
    ('molybdenum', 'Mo', 95.95),
    ('technetium', 'Tc', 98),
    ('ruthenium', 'Ru', 101.1),
    ('rhodium', 'Rh', 102.9),
    ('palladium', 'Pd', 106.4),
    ('silver', 'Ag', 107.9),
    ('cadmium', 'Cd', 112.4),
    ('indium', 'In', 114.8),
    ('tin', 'Sn', 118.7),
    ('antimony', 'Sb', 121.8),
    ('tellur!ium', 'Te', 127.6),
    ('iod!ine', 'I', 126.9),
    ('xenon', 'Xe', 131.3), #Up until here, the molar masses are accurate to my data booklet. The rest are taken from Google.
    ('cesium', 'Cs', 132.91),
    ('barium', 'Ba', 137.33),
    ('', '', 138.91),
    ('', '', 140.12),
    ('', '', 140.91),
    ('', '', 144.24),
    ('', '', 145),
    ('', '', 150.36),
    ('', '', 151.96),
    ('', '', 157.25),
    ('', '', 158.93),
    ('', '', 162.5),
    ('', '', 164.93),
    ('', '', 167.26),
    ('', '', 168.93),
    ('', '', 173.04),
    ('', '', 174.97),
    ('hafnium', 'Hf', 178.49),
    ('tantalum', 'Ta', 180.95),
    ('tungsten', 'W', 183.84),
    ('rhenium', 'Re', 186.21),
    ('osmium', 'Os', 190.23),
    ('iridium', 'Ir', 192.22),
    ('platinum', 'Pt', 195.08),
    ('gold', 'Au', 196.97),
    ('mercury', 'Hg', 200.59),
    ('thallium', 'Tl', 204.38),
    ('lead', 'Pb', 207.2),
    ('bismuth', 'Bi', 208.98),
    ('polonium', 'Po', 209),
    ('astat!ine', 'At', 210),
    ('radon', 'Rn', 222),
    ('', '', 223),
    ('', '', 226),
    ('', '', 227),
    ('', '', 232.04),
    ('', '', 231.04),
    ('', '', 238.03),
    ('', '', 237.05),
    ('', '', 244),
    ('', '', 243),
    ('', '', 247),
    ('', '', 247),
    ('', '', 251),
    ('', '', 252),
    ('', '', 257),
    ('', '', 258),
    ('', '', 259),
    ('', '', 262),
    ('', '', 267),
    ('', '', 262),
    ('', '', 269),
    ('', '', 264),
    ('', '', 269),
    ('', '', 278),
    ('', '', 281),
    ('', '', 282),
    ('', '', 285),
    ('', '', 286),
    ('', '', 289),
    ('', '', 289),
    ('', '', 293),
    ('', '', 294)
]
state_format = ['aq', 's', 'l', 'g']
solubilities_in_water = { #Just 0 (insoluble), 1 (slightly soluble) and 2 (soluble).
    'cations': {
        'sodium': 2,
        'potassium': 2,
        'silver': 0,
    },
    'anions': {
        'chloride': 2,
        'bromide': 2,
        'iodide': 2,
        'nitrate': 2,
        'acetate': 2,
        'ethanoate': 2,
        'sulfate': 2,
        'hydroxide': 0,
        'carbonate': 0,
        'phosphate': 0,
        'sulfide': 0,
    },
    #Specific cases (EXCEPTIONS) go here, they're applied after cation/anion rules.
    'silver chloride': 0,
    'lead chloride': 1,
    'silver bromide': 0,
    'lead bromide': 1,
    'silver iodide': 0,
    'lead iodide': 0,
    'silver hydroxide': 2,
    #...
}
other_cation_names = {
    'cuprous': ['copper', 1],
    'cupric': ['copper', 2],
    'ferrous': ['iron', 2],
    'ferric': ['iron', 3],
    'stannous': ['tin', 2],
    'mercurous': ['mercury', 1],
    'mercuric': ['mercury', 2],
}
other_ionic_compound_names = {
    'salt': 'sodium chloride',
    'cinnabar': 'mercury sulfide',
    'alumina': 'aluminium oxide',
    'rust': 'iron(III) oxide',
    'lye': 'sodium hydroxide',
    'caustic soda': 'sodium hydroxide',
    'baking soda': 'sodium bicarbonate',
    'bleach': 'sodium hypochlorite',
    'vinegar': 'acetic acid',
    'tenorite': 'copper oxide',
    'limestone': 'calcium carbonate',
    'calcite': 'calcium carbonate',
    'magnesia': 'magnesium oxide',
    'vitamin c': 'ascorbic acid',
    'gastric acid': 'hydrochloric acid',
    'sand': 'silicon oxide',
}
ionisable_molecules = {
    'water': 'hydrogen hydroxide',
}
molecules = [
    ('water', 'H2 O', 0, 1),
    ('carbon dioxide', 'C O2', 0, 2),
    ('ammonia', 'N H3', 0, 2),
    ('sulfur dioxide', 'S O2', 0, 2),
    ('methane', 'C H4', 0, 2),
    
    ('ammonium', 'N H4', 1),
    #('fluoride', 'F', -1),
    #('chloride', 'Cl', -1),
    #('bromide', 'Br', -1),
    #('iodide', 'I', -1),
    #('oxide', 'O', -2),
    #('sulfide', 'S', -2),
    #('nitride', 'N', -3),
    ('azide', 'N3 ', -1),
    #('phosphide', 'P', -3),
    ('peroxide', 'O2', -2),
    ('nitrite', 'N O2', -1),
    ('nitrate', 'N O3', -1),
    ('acetate', 'C H3 C O O', -1),
    ('ethanoate', 'C H3 C O O', -1),
    ('citrate', 'C6 H5 O7', -3),
    ('malate', 'C4 H4 O5', -2),

    ('sulfite', 'S O3', -2),
    ('sulfate', 'S O4', -2),
    ('thiosulfate', 'S2 O3', -2),
    ('bisulfate', 'H S O4', -1),

    ('carbonate', 'C O3', -2),
    ('bicarbonate', 'H C O3', -1),

    ('phosphite', 'P O3', -3),
    ('phosphate', 'P O4', -3),

    ('hypochlorite', 'Cl O', -1),
    ('chlorite', 'Cl O2', -1),
    ('chlorate', 'Cl O3', -1),
    ('perchlorate', 'Cl O4', -1),

    ('manganate', 'Mn O4', -2),
    ('permanganate', 'Mn O4', -1),

    ('hydroxide', 'O H', -1),
    ('borohydride', 'B H4', -1),
    ('tetrahydroborate', 'B H4', -1),
    ('borate', 'B O3', -3),
    ('metaborate', 'B O2', -1),
    ('tetraborate', 'B4 O7', -2),
    ('alanate', 'Al H4', -1),
    ('cyanide', 'C N', -1),
    ('ascorbate', 'C6 H7 O6', -1),
    ('oxalate', 'C2 O4', -2),
]

acid_names = {
    'hydrofluoric': 'fluoride',
    'hydrochloric': 'chloride',
    'hydrobromic': 'bromide',
    'hydroiodic': 'iodide',
    'acetic': 'acetate',
    'ethanoic': 'ethanoate',
    'nitric': 'nitrate',
    'nitrous': 'nitrite',
    'hydrazoic': 'azide',
    'sulfurous': 'sulfite',
    'sulfuric': 'sulfate',
    'phosphoric': 'phosphate',
    'carbonic': 'carbonate',
    'chloric': 'chlorate',
    'hypochlorous': 'hypochlorite',
    'perchloric': 'perchlorate',
    'citric': 'citrate',
    'malic': 'malate',
    'ascorbic': 'ascorbate',
    'oxalic': 'oxalate',
    'boric': 'borate',
    'metaboric': 'metaborate',
    'tetraboric': 'tetraborate',
}
break_up = {
    'hydrogen hydride': ['hydrogen'],
    'hydrogen hydroxide': ['water'],
    'hydrogen oxide': ['water'],
    'carbon hydride': ['methane'],
    'hydrogen carbide': ['methane'],
    'carbon oxide': ['carbon dioxide'],
    'hydrogen carbonate': ['water', 'carbon dioxide'],
    'hydrogen bicarbonate': ['water', 'carbon dioxide'],
    'hydrogen sulfite': ['water', 'sulfur dioxide'],
    'ammonium hydroxide': ['water', 'ammonia'],
    'ammonium oxide': ['water', 'ammonia'],
    'ammonium carbonate': ['water', 'carbon dioxide', 'ammonia'],
    'ammonium sulfite': ['water', 'sulfur dioxide', 'ammonia'],
}
class Element:
    def __init__(self, number, name, symbol, m_mass):
        name_no_markers = name.replace('!', '')
        self.number = number
        self.name = name_no_markers
        if '!' in name:
            self.ion_name = name.split('!')[0] + 'ide'
        else:
            self.ion_name = name_no_markers
        self.symbol = symbol
        self.molar_mass = m_mass
        for i in Families:
            for a in Families[i]:
                if self.number == a:
                    self.charge = charges[i][0]
                    self.both = charges[i][1]
                    self.state = states[i]
        for i in charge_exceptions:
            if self.number == i[0]:
                self.charge = i[1]
        for i in state_exceptions:
            if self.number == i[0]:
                self.state = i[1]
        #print(self.name, self.charge)
        '''if self.name in cation:
            self.formula = cation[name][0].replace(' ','').translate(SUB)
        elif self.name in anion:
            self.formula = anion[name][0].replace(' ','').translate(SUB)'''
    def create(self, oxidation = None):
        return Atom(self, oxidation)
class Molecule:
    def __init__(self, name, components, charge = 0):
        self.name = name
        self.symbol = components
        #self.components = elem.components
        xd = components.split(' ')
        self.components = []
        self.component_amounts = []
        for i in xd:
            digit = len(i)
            for j in range(len(i)): #check for num, cringe way to do it though.
                if i[j].isdigit():
                    digit = j
                    break
            name = i[:digit]
            if digit < len(i): #If number is shown
                amount = int(i[digit:len(i)])
            else: #Default to 1 if not
                amount = 1
            self.components.append(name)
            self.component_amounts.append(amount)
        self.stable_charge = charge
        self.compoundable = False
        self.charge = charge
        self.reactivity = 0#########LATERRR
    def family(self):
        for x in Families:
            if self.element.number in Families[x]:
                return x
        return None
    def is_nonmetal(self): #If it is by itself, it will tend to form a diatomic arrangement.
        return self.family() in ['halogen', 'chalcogen', 'pnictogen']
    def is_metal(self):
        return self.family() in ['alkali1', 'alkali2', 'transition', 'posttransition']
    def is_di(self):
        return False
    def ionise(self, other = None):
        self.charge = self.stable_charge
    def deionise(self):
        self.charge = 0
    def chemically_stable(self):
        return self.charge == self.stable_charge
    def is_anion(self):
        return self.charge < 0
    def is_cation(self):
        return self.charge > 0
    def tend_cation(self):
        return self.stable_charge > 0
    def tend_anion(self):
        return self.stable_charge < 0
    def electrons_needed(self):
        return self.charge - self.stable_charge
    def dissolve(self):
        for i in ionisable_molecules:
            if self.name == i:
                return create_compound(ionisable_molecules[i])[1]
        return None
    def interact_with(self, other):
        if other is None:
            if self.tend_cation():
                return [False, compound(self, None)]
            else:
                return [False, compound(None, self)]
        condition1 = self.tend_cation() and other.tend_anion()
        condition2 = self.tend_anion() and other.tend_cation()
        if condition1 or condition2:
            return [True, self.form_ionic_compound(other)]
        else:
            return [False, None]
    def form_ionic_compound(self, other): #
        if self.tend_cation():
            #self.ionise()
            other.ionise(self)
            return compound(self, other)
        else:
            #self.ionise()
            other.ionise(self)
            return compound(other, self)
    def current_name(self):
        return self.name
    def formula(self):
        return self.symbol.replace(' ', '').translate(SUB)
    def count_atoms_in(self, quantity = 1):
        species = self
        #print(type(self.components[component]))
        names = species.components
        amounts = self.component_amounts
        atom_count = {}
        for x in range(len(names)):
            name = names[x]
            amount = amounts[x]
            if name not in atom_count:
                atom_count[name] = amount * quantity
            else:
                atom_count[name] = atom_count[name] + amount * quantity
        #print('SPECIES', species)
        return atom_count
    def atom_count(self, amount = 1):
        return self.count_atoms_in(amount)
    def molar_mass(self):
        mass = 0
        for i in range(len(self.components)):
            mass = mass + self.component_amounts[i] * molar_mass(self.components[i])
        return mass
class Atom(Element):
    def __init__(self, elem, oxidation = None):
        self.name = elem.name
        self.symbol = elem.symbol
        self.element = elem
        self.ion_name = elem.ion_name
        self.stable_charge = elem.charge
        self.both = elem.both
        self.charge = 0
        self.oxidation = oxidation
        self.m_mass = elem.molar_mass
        if oxidation is not None:
            self.stable_charge = oxidation
        self.di = False
        self.components = [self.symbol]
        self.component_amounts = [1]
        if self.is_di():
            self.di = True
        self.reactivity = 0#########LATERRR
    def family(self):
        for x in Families:
            if self.element.number in Families[x]:
                return x
        return None
    def compare_electronegativities(self, elem):
        if abs(self.stable_charge) > abs(elem.stable_charge):
            return True
        return False
    def formula(self):
        return self.symbol
    #def name(self):
    def is_hydrogen(self):
        return self.family() == 'hydrogen'
    def is_nonmetal(self): #If it is by itself, it will tend to form a diatomic arrangement.
        return self.family() in ['halogen', 'chalcogen', 'pnictogen']
    def is_metal(self):
        return self.family() in ['alkali1', 'alkali2', 'transition', 'posttransition']
    def ionise(self, other = None):
        self.charge = self.stable_charge
        if not self.both:
            if self.compare_electronegativities(other):
                self.charge = round(abs(self.stable_charge) * -abs(other.stable_charge)/other.stable_charge)
        self.di = False
    def deionise(self):
        self.charge = 0
        if self.is_di():
            self.di = True
    def is_di(self):
        return self.is_nonmetal() or self.is_hydrogen()
    def diatomify(self):
        self.deionise()
    def chemically_stable(self):
        return self.charge == self.stable_charge
    def is_anion(self):
        return self.charge < 0
    def is_cation(self):
        return self.charge > 0
    def tend_cation(self):
        return self.stable_charge > 0 and self.both
    def tend_anion(self):
        return self.stable_charge < 0 and self.both
    def electrons_needed(self):
        return self.charge - self.stable_charge
    def interact_with(self, other):
        if other is None:
            if self.tend_cation():
                return [False, compound(self, None)]
            else:
                return [False, compound(None, self)]
        condition1 = self.tend_cation() and other.tend_anion()
        condition2 = self.tend_anion() and other.tend_cation()
        #if condition1 or condition2:
        return [True, self.form_ionic_compound(other)]
        #else:
        #    return [False, None]
    def form_ionic_compound(self, other): #
        self.ionise(other)
        other.ionise(self)
        if self.is_cation():
            return compound(self, other)
        else:
            return compound(other, self)
    def current_name(self):
        if self.is_anion():
            return self.ion_name
        if self.oxidation is not None:
            if self.oxidation >= 10000:
                return self.name + '(' + str(self.oxidation) + ')'
            return self.name + '(' + roman(self.oxidation) + ')'
        else:
            return self.name
    def __str__(self):
        return str(self.__dict__)
    def molar_mass(self):
        if self.di:
            return 2 * self.m_mass
        return self.m_mass
class compound:
    def balance_charges(self):
        c = self.components[0].charge
        a = -self.components[1].charge
        cNumber = int(a / math.gcd(c, a))
        aNumber = int(c / math.gcd(c, a))
        self.amounts = [cNumber, aNumber] 
    def __init__(self, cation = None, anion = None):
        self.components = [cation, anion] #None datatype signifies, well, no ion there. so plan to act as a regular atom ie Mg as Mg(s) and H as H2(g) or Br as Br2(g)
        self.amounts = [0, 0]
        if self.compound():
            self.components[0].ionise(self.components[1])
            self.components[1].ionise(self.components[0])
            #for i in self.components:
            #    i.ionise()
            self.balance_charges()
        else:
            for i in range(len(self.components)):
                if self.components[i] is not None:
                    self.amounts[i] = 1
                    if self.components[i].is_di():
                        self.amounts[i] = 2
                    self.components[i].deionise() #Deionise it, because well it's not a compound.
        self.name = []
        for i in self.components:
            if i is not None:
                self.name.append(i.current_name())
        self.name = ' '.join(self.name)
    def compound(self):
        return self.components[0] is not None and self.components[1] is not None
    def get_species(self):
        if self.compound():
            return None
        if self.components[0] is not None:
            return self.components[0]
        else:
            return self.components[1]
    def get_species_num(self):
        if self.compound():
            return None
        if self.components[0] is not None:
            return 0
        else:
            return 1
    def diatomify(self):
        if self.compound():
            None
        if self.components[0] is not None:
            self.components[0].diatomify()
        else:
            self.components[1].diatomify()
    def dissolve(self):
        if not self.compound():
            if isMolecule(self.get_species()):
                i = self.components[self.get_species_num()].dissolve()
                return i
        return None
    def formula(self):
        cNumber2 = self.amounts[0]
        aNumber2 = self.amounts[1]
        cation_display = ''
        anion_display = ''
        if self.components[0] is not None:
            if cNumber2 == 1:
                cation_display = self.components[0].symbol
            else:
                if isMolecule(self.components[0]):
                    cation_display = '(' + self.components[0].formula() + ')' + str(cNumber2).translate(SUB)
                else:
                    cation_display = self.components[0].formula() + str(cNumber2).translate(SUB)
        if self.components[1] is not None:
            if aNumber2 == 1:
                anion_display = self.components[1].formula()
            else:
                if isMolecule(self.components[1]):
                    anion_display = '(' + self.components[1].formula() + ')' + str(aNumber2).translate(SUB)
                else:
                    anion_display = self.components[1].formula() + str(aNumber2).translate(SUB)
        return (cation_display + anion_display).replace(' ', '').translate(SUB)
    def replaceIon(self, index, new):
        if index == 0:
            return compound(new.components[0], self.components[1])
        else:
            return compound(self.components[0], new.components[1])
    def interact_with(self, other):
        reactants = [self, other]
        products = []
        if self.dissolve() is not None:
            self = self.dissolve()
        if other.dissolve() is not None:
            other = other.dissolve()
        #print(self.compound(), other.compound())
        if (not (self.compound() or other.compound())):
            react = self.get_species().interact_with(other.get_species())
            if react[0]:
                products.append(react[1])
        elif other is None:
            products.append(self)
        else:#literally just swap them
            products.append(self.replaceIon(0, other))
            products.append(self.replaceIon(1, other))
        if len(products) == 0:
            raise MyException('No Reaction')
        return Reaction(reactants, products)
    '''{
            'reactants': reactants,
            'products': products,
        }'''
    def count_atoms_in(self, component, quantity = 1):
        species = self.components[component]
        #print(type(self.components[component]))
        if self.components[component] is None:
            return {}
        names = species.components
        amounts = self.components[component].component_amounts
        atom_count = {}
        for x in range(len(names)):
            name = names[x]
            amount = amounts[x]
            if name not in atom_count:
                atom_count[name] = amount * quantity
            else:
                atom_count[name] = atom_count[name] + amount * quantity
        #print('SPECIES', species)
        return atom_count
    def atom_count(self, amount = 1):
        if True:
            #cation
            bals = self.amounts
            num_cations = bals[0]
            cation_atom_count = self.count_atoms_in(0, num_cations * amount)
            #anion
            num_anions = bals[1]
            anion_atom_count = self.count_atoms_in(1, num_anions * amount)
            total_atom_count = {}
            total_atom_count = append_count(total_atom_count, cation_atom_count)
            total_atom_count = append_count(total_atom_count, anion_atom_count)
            return total_atom_count
        else:#assume 1 as amount as no balance necessary
            return count_atoms_in(cation[self.cation.name.split('(')[0]][0], amount)
    def molar_mass(self):
        mass = 0
        if self.components[0] is not None:
            mass = mass + self.amounts[0] * self.components[0].molar_mass()
        if self.components[1] is not None:
            mass = mass + self.amounts[1] * self.components[1].molar_mass()
        return mass
class Reaction:
    def __init__(self, reactants, products):
        self.reactants = reactants
        self.products = products
        self.diatomify()
        self.fix()
        self.break_up_products()
        balance = new_balance(self.reactants, self.products)
        self.balanced = balance[0]
        self.coefficients = balance[1]
        self.unit = [None, None] #[destination, Unit]
    def diatomify(self):
        #return print(self.products)
        for x in range(len(self.reactants)):
            i = self.reactants[x]
            if not i.compound():
                species = i.get_species()
                if not isMolecule(species):
                    self.reactants[x].diatomify()
            else:
                if i.components[0].name == i.components[1].name:
                    self.reactants[x] = compound(self.reactants[x].components[0], None)
                    self.reactants[x].components[0].diatomify()
                    #self.reactants[x].components[1] = None
        for x in range(len(self.products)):
            i = self.products[x]
            if not i.compound():
                species = i.get_species()
                if not isMolecule(species):
                    self.products[x].diatomify()
            else:
                if i.components[0].name == i.components[1].name:
                    self.products[x] = compound(self.products[x].components[0], None)
                    self.products[x].components[0].diatomify()
    def fix(self):
        for x in range(len(self.reactants)):
            if isMolecule(self.reactants[x]):
                self.reactants[x] = self.reactants[x].dissolve()
    def break_up_products(self):
        new_products = []
        for i in range(len(self.products)):
            l = self.products[i]
            if l.name in break_up:
                for x in break_up[l.name]:
                    new_products.append(moleculies[x])
            else:
                new_products.append(l)
        self.products = new_products
    def format_equation(self, mode = 0):
        Reactants = self.reactants
        Products = self.products
        nreactants = len(Reactants) #this wont change
        nproducts = len(Products) #this wont change
        ReactantCoefficients = self.coefficients[0]
        ProductCoefficients = self.coefficients[1]
        #print(Reactants, Products)
        #print(j.name, j.atom_count())
        reactant_display = []
        product_display = []
        reactant_format = []
        product_format = []
        heading = ''
        if mode == 0:
            if self.balanced:
                heading = 'Balanced Chemical Equation'
            else:
                heading = 'Chemical Equation'
            for a in range(nreactants):
                reactant_format.append(Reactants[a].formula())
            for a in range(nproducts):
                product_format.append(Products[a].formula())
            for x in range(nreactants):
                if ReactantCoefficients[x] > 1:
                    reactant_display.append(str(ReactantCoefficients[x]) + reactant_format[x])
                else:
                    reactant_display.append(reactant_format[x])
            for x in range(nproducts):
                if ProductCoefficients[x] > 1:
                    product_display.append(str(ProductCoefficients[x]) + product_format[x])
                else:
                    product_display.append(product_format[x])
            return heading + ':  ' + ' + '.join(reactant_display) + ' ---> ' + ' + '.join(product_display)
        elif mode == 1:
            heading = 'Worded Equation'
            for a in range(nreactants):
                reactant_format.append(Reactants[a].name)
            for a in range(nproducts):
                product_format.append(Products[a].name)
            for x in range(nreactants):
                if ReactantCoefficients[x] > 1:
                    reactant_display.append(reactant_format[x])
                else:
                    reactant_display.append(reactant_format[x])
            for x in range(nproducts):
                if ProductCoefficients[x] > 1:
                    product_display.append(product_format[x])
                else:
                    product_display.append(product_format[x])
            return heading + ':  ' + ' + '.join(reactant_display) + ' ---> ' + ' + '.join(product_display)
    def yay(self, mode = 0):
        return self.format_equation(mode)
    def list_number_prompts(self):
        sList = []
        Dict = {}
        for i in range(len(self.reactants)):
            Dict['A' + str(i + 1)] = [0, i]
            sList.append('A' + str(i + 1) + ' for ' + self.reactants[i].formula())
        for i in range(len(self.products)):
            Dict['B' + str(i + 1)] = [1, i]
            sList.append('B' + str(i + 1) + ' for ' + self.products[i].formula())
        return [Dict, 'Type ' + ', '.join(sList) + '.']
    def molar_ratio(self, destination):
        ratio = self.coefficients[destination[0]][destination[1]] / self.coefficients[self.unit[0][0]][self.unit[0][1]]
        #print(ratio)
        self.unit[0] = destination
        return Unit(self, destination, self.unit[1].number * ratio, 'mol')
    def species(self, destination):
        if destination[0] == 0:
            return self.reactants[destination[1]]
        return self.products[destination[1]]



Units = {
    'mass': {
        'mg': 1000,
        'g': 1,
        'kg': 1/1000,
        'default': 'g',
    },
    'volume': {
        'mL': 1000,
        'L': 1,
        'kL': 1/1000,
        'default': 'L',
    },
    'quantity': {
        'atoms': 6.022*10**23,
        'mol': 1,
        'default': 'mol',
    },
}
class Unit:
    def __init__(self, reaction, destination, number, unit):
        self.reaction = reaction
        self.destination = destination
        self.number = number
        self.unit = unit
        for i in Units:
            if unit in Units[i]:
                self.type = i
    def standardify(self):
        return self.convert(Units[self.type]['default'])
    def convert(self, new_unit = 'mol'):
        if self.unit == new_unit:
            return self
        for i in Units:
            if new_unit in Units[i]:
                unit_type = i
        if unit_type == self.type:
            new_number = self.number / Units[unit_type][self.unit] * Units[unit_type][new_unit]
            return Unit(self.reaction, self.destination, new_number, new_unit)
        standarded = self.standardify()
        new_number = -1*10**1000000
        if 'volume' in [self.type, unit_type]: #If volume is involved in the conversion, there will be an assumption.
            print("ASSUMPTION: " + self.reaction.species(self.destination).formula() + " is gaseous and at STP.")
        if unit_type == 'quantity': #In this check, it's standarded, not self.
            if self.type == 'mass':
                new_number = standarded.number / standarded.reaction.species(self.destination).molar_mass() #n = m/M
            if self.type == 'volume':
                new_number = standarded.number / 22.71 #n = V/22.71
        if unit_type == 'volume':
            if self.type == 'quantity':
                new_number = 22.71 * standarded.number #V = 22.71n
            if self.type == 'mass':
                new_number = 22.71 * standarded.number / standarded.reaction.species(self.destination).molar_mass() #V = 22.71n; n = m/M; V = 22.71*m/M
        if unit_type == 'mass':
            if self.type == 'quantity':
                new_number = standarded.number * standarded.reaction.species(self.destination).molar_mass() #m = nM
            if self.type == 'volume':
                new_number = standarded.number * standarded.reaction.species(self.destination).molar_mass() / 22.71 #n = V/22.71; n = m/M; m/M = V/22.71; m = VM/22.71
        #new_number is now in the default form of the designated unit type.
        new_number = new_number * Units[unit_type][new_unit]
        #Adjusting number to designated unit.
        return Unit(self.reaction, self.destination, new_number, new_unit)
    def display(self, setting = -1):
        if setting == 0:
            return str(self.number)
        if setting == 1:
            return ' '.join([str(self.number), self.unit])
        return 'There is ' + ' '.join([str(self.number), self.unit]) + ' of ' + self.reaction.species(self.destination).formula()

def convert(species, number, unit1, unit2 = 'mol'):
    

    new_1 = None
    for i in mass:
        if unit1 == i:
            new_1 = number * mass[i]
    return print(new_1)
    for i in volume:
        pass

    if unit2 == 'mol':
        return 
    












def new_balance(Reactants, Products):
    ReactantCoefficients = [1, 1]
    ProductCoefficients = []
    for i in Products:
        #print('translate', product[i])
        ProductCoefficients.append(1)
     #'H2'.translate(SUB)
    nreactants = len(Reactants) #this wont change
    nproducts = len(Products) #this wont change
    reactant_loop = True
    product_loop = True
    found = False
    global limit
    ReactantCoefficients[0] = 0
    ProductCoefficients[0] = 0
    while reactant_loop and not found:
        product_loop = True
        for pIndex in range(nproducts):
            ProductCoefficients[pIndex] = 1
        ProductCoefficients[0] = 0
        ReactantCoefficients[0] = ReactantCoefficients[0] + 1
        for rIndex in range(nreactants - 1):
            if ReactantCoefficients[rIndex] > limit:
                ReactantCoefficients[rIndex] = 1
                ReactantCoefficients[rIndex + 1] = ReactantCoefficients[rIndex + 1] + 1
        if ReactantCoefficients[nreactants - 1] > limit:
            found = False
            reactant_loop = False
            break;
        while product_loop and not found:
            ProductCoefficients[0] = ProductCoefficients[0] + 1
            for pIndex in range(nproducts - 1):
                if ProductCoefficients[pIndex] > limit:
                    ProductCoefficients[pIndex] = 1
                    ProductCoefficients[pIndex + 1] = ProductCoefficients[pIndex + 1] + 1
            if ProductCoefficients[nproducts - 1] > limit:
                product_loop = False
                break;
            #######################
            reactant_count = {}
            for reactantIndex in range(nreactants):
                #print('check prior', Reactants[reactantIndex])
                reactant_count = append_count(reactant_count, Reactants[reactantIndex].atom_count(ReactantCoefficients[reactantIndex]))
            product_count = {}
            for productIndex in range(nproducts):
                #print('check salt', Products[productIndex])
                product_count = append_count(product_count, Products[productIndex].atom_count(ProductCoefficients[productIndex]))
            #print('COEFFICIENTS', ReactantCoefficients, ProductCoefficients)
            #print('IS IT EQUAL?', reactant_count, product_count)
            if debug:
                print(reactant_count, product_count)
            if reactant_count == product_count:
                found = True
                print('Balanced coefficients: ', ReactantCoefficients, ', ', ProductCoefficients, '. The balanced equation is below.')
                break
            #print('counts', reactant_count, product_count)
            ##############
    if not found:#Failed, default all to 1.
        print('!!! Could not balance the equation within the set coefficient-limit (' + str(limit) + '). Instead, an equation without coefficients is below.')
        for i in ReactantCoefficients:
            ReactantCoefficients[i] = 1
        for i in ProductCoefficients:
            ProductCoefficients[i] = 1
    return [found, [ReactantCoefficients, ProductCoefficients]]
def unroman(value):
    try:
        value = round(float(value.lower().strip()))
    except ValueError:
        value = value.lower().strip()
        if len(value) == 0:
            return 0
        
        n = 0
        values = ((100, 'c'), (50, 'l'), (10, 'x'), (5, 'v'), (1, 'i'))
        i = 0
        try:
            while i < len(value):
                broken = True
                for a in range(len(values)):
                    if value[i] == values[a][1]:
                        broken = False
                        break
                if broken:
                    raise MyException('Invalid roman numeral "' + value + '".')
                for a in range(len(values)):
                    if value[i] == values[a][1]:
                        index = a - 1
                        condition1 = i + 1 < len(value) and a > 0
                        if condition1:
                            e = -1
                            index = a - 1
                            while index > -1:
                                if value[i + 1] == values[index][1]:
                                    e = index
                                    break
                                index = index - 1
                            condition2 = e > -1
                        else:
                            condition2 = False
                        if condition2 and condition1:
                            n = n + values[index][0] - values[a][0]
                            i = i + 1
                        else:
                            n = n + values[a][0]
                        i = i + 1
                        break
                        
            value = n
        except MyException as e:
            print(e)
        except:
            print('Error parsing oxidation state. Setting to element default.')
            value = 0
    except:
        print('Error parsing oxidation state. Setting to element default.')
        value = 0
    return value
def molar_mass(symbol):
    for i in elements:
        if i.symbol == symbol:
            return i.molar_mass
def roman(value):
    #print(value)
    result = ''
    values = ((100, 'C'), (50, 'L'), (10, 'X'), (5, 'V'), (1, 'I'))
    countdown = value
    while countdown > 0:
        for i in values:
            if countdown == 4:
                countdown = countdown - 4
                result = result + 'IV'
                break
            elif countdown == 9:
                countdown = countdown - 9
                result = result + 'IX'
                break
            elif countdown >= 40 and countdown < 50:
                countdown = countdown - 40
                result = result + 'XL'
            elif countdown >= 90 and countdown < 100:
                countdown = countdown - 90
                result = result + 'XC'
            else:
                if countdown >= i[0]:
                    countdown = countdown - i[0]
                    result = result + i[1]
                    break
    return result
def check_roman(run): #CONFIRMED TO WORK UP TO RUN = 1e5
    e = True
    for x in range(run):
        if not (unroman(roman(x)) == x):
            e = False
            print(x, unroman(roman(x)))
            print(roman(x))
            break
    return e
def append_count(count, new):
    total_atom_count = count
    for i in new:
        if i not in total_atom_count:
            total_atom_count[i] = new[i]
        else:
            total_atom_count[i] = total_atom_count[i] + new[i]
    return total_atom_count
def isMolecule(thing):
    return isinstance(thing, Molecule)
def create_atom(name):
    d = name.split('(')
    name = d[0]
    oxidation = None
    if len(d) > 1:
        oxidation = unroman(d[1].split(')')[0])
        if oxidation == 0:
            oxidation = None
    base = name[:-3]
    ide_check = name[(len(name) - 3):]
    #print(base, ide_check)
    if ide_check == 'ide':
        #if name == 'hydride':
        #    return elements[0].create(-1)
        for i in elementies:
            if i[0:len(base)] == base:
                return elementies[i].create(oxidation)
    for i in moleculies:
        if name == i:
            return moleculies[i]
    for i in other_cation_names:
        if name == i:
            return elementies[other_cation_names[i][0]].create(other_cation_names[i][1])
    return elementies[name].create(oxidation)
    #print('fail', name)
    #raise Exception("That was not a valid species! Try again.")
def create_compound(name):
    for i in other_ionic_compound_names:
        if name == i:
            return create_compound(other_ionic_compound_names[i])
    name = name.split(' ')
    if 'acid' in name:
        if not (name[0] in acid_names):
            raise MyException('Could not find reactant species "' + ' '.join(name) + '".')
        e = acid_names[name[0]]
        thing2 = create_atom(e)
        #print(thing1, thing2)
        return create_atom('hydrogen').interact_with(thing2)
    elif len(name) == 2:
        try: 
            thing1 = create_atom(name[0])
            thing2 = create_atom(name[1])
        except:
            pass
        else:
            return thing1.interact_with(thing2)
    else:
        try: 
            thing = create_atom(name[0])
        except:
            pass
        else:
            return thing.interact_with(None)
    return None




#####################
#####################


for x in range(len(elements)):
    e0 = elements[x][0]
    e1 = elements[x][1]
    e2 = elements[x][2]
    elements[x] = Element(x + 1, e0, e1, e2)
    elementies[elements[x].name] = Element(x + 1, e0, e1, e2)
for x in range(len(molecules)):
    e0 = molecules[x][0]
    e1 = molecules[x][1]
    e2 = molecules[x][2]
    molecules[x] = Molecule(e0, e1, e2)
    moleculies[molecules[x].name] = Molecule(e0, e1, e2)

def lol(n):
    try:
        return create_compound(input('Reactant ' + str(n) + ':').lower())
    #except KeyError:
        #print('That does not seem to be a valid reactant. Have you made a typo? Anyways, try again.')
    except:
        print('Uh oh, something else went wrong!')
res = []
A = None
class MyException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

'''first = None
    while first is None:
        first = lol(1)
    second = None
    while second is None:
        second = lol(2)'''
#reaction = first[1].interact_with(second[1])
#print(show_reaction(reaction))

#print(first[1].atom_count())



reactivity_series = [
    "caesium",
    "francium",
    "rubidium",
    "potassium",
    "sodium",
    "lithium",
    "barium",
    "radium",
    "strontium",
    "calcium",
    "magnesium",
    "beryllium",
    "aluminium",
    "titanium",
    "manganese",
    "zinc",
    "chromium",
    "iron",
    "cadmium",
    "cobalt",
    "nickel",
    "tin",
    "lead",
    "hydrogen", #######################################
    "antimony",
    "bismuth",
    "copper",
    "tungsten",
    "mercury",
    "silver",
    "platinum",
    "gold"
]








###########################
reaction = None
def runEquationFinder():
    try:
        
        res = []
        e = input('Reactants: ').lower().strip().split('+')
        print(len(e))
        if len(e) == 1:
            raise MyException('No reaction - 2 reactants should be specified.')
        for a in e:
            i = a.strip()
            comp = create_compound(i)
            if comp is None:
                raise MyException('Could not find reactant species "' + i + '".')
            else:
                res.append(comp[1])
        #try:
        A = res[0].interact_with(res[1])
        global reaction
        reaction = A
        #except:
            #raise MyException("XD")
        print(A.yay(0))
        print(A.yay(1))
        return A
    except KeyError:
        print('That does not seem to be a valid reactant list. Perhaps you made a typo? Anyways, try again.')
    except MyException as e:
        print(e)
    #except:
    #    print('Uh oh, something else went wrong with loading reactants!')


while True:
####
    print('Running Chemical Finder - made by Albert Agustin Amenabar ' + last_update)
    if testing_case:
        choice = '1'
    else:
        print('Do you want to figure out an equation (1), or an ionic compound formula (2)?')
        print('Misc: About (3), Exit (exit())')
        choice = input('-> ')
    if choice == '1':
        equation = None
        equation = runEquationFinder()
        if equation is None:
            continue
        move = len(input('Do you wish to proceed? Leave blank if not. -> ')) > 0
        if move:
            prompts = equation.list_number_prompts()
            error = True
            while error:
                try:
                    print("Which species has a known quantity? " + prompts[1])
                    known_str = input("-> ").strip()
                    known = None
                    for i in prompts[0]:
                        if known_str == i:
                            known = prompts[0][i]
                            error = False
                            break
                    if error:
                        raise MyException('Sorry, "' + known_str + '" is not a valid input. Please try again!')
                except MyException as e:
                    print(e)
            error = True
            while error:
                try:
                    print("What is this quantity? Type [number] [unit]. [unit] could be in atoms, mol (quantity); mg, g, kg (mass); mL, L, kL (volume); for now...")
                    quantity_for_known = input("-> ").strip()
                    quantity_for_known = quantity_for_known.split(' ')
                    qk_number = float(quantity_for_known[0])
                    qk_unit = quantity_for_known[1]
                    #check to see if unit is supported
                    for i in Units:
                        if qk_unit in Units[i]:
                            error = False
                            break
                    if error:
                        raise MyException('Sorry, "' + qk_unit + '" is not a valid or supported unit. Please try again!')
                except MyException as e:
                    print(e)
                except ValueError: #could not convert string to float: [input]
                    print('Sorry, "' + quantity_for_known[0] + '" is not a valid quantity. Please try again!')
            error = True
            while error:
                try:
                    print("Which species is to be found? " + prompts[1])
                    unknown_str = input("-> ").strip()
                    unknown = None
                    for i in prompts[0]:
                        if unknown_str == i:
                            unknown = prompts[0][i]
                            error = False
                            break
                    if error:
                        raise MyException('Sorry, "' + unknown_str + '" is not a valid input. Please try again!')
                except MyException as e:
                    print(e)
            error = True
            while error:
                try:
                    print("What is this unit? Again, [unit] could be in atoms, mol (quantity); mg, g, kg (mass); mL, L, kL (volume); for now...")
                    unit_for_unknown = input("-> ").strip()
                    for i in Units:
                        if unit_for_unknown in Units[i]:
                            error = False
                            break
                    if error:
                        raise MyException('Sorry, "' + unit_for_unknown + '" is not a valid or supported unit. Please try again!')
                except MyException as e:
                    print(e)
            print(equation, known, qk_number, qk_number)
            equation.unit = [known, Unit(equation, known, qk_number, qk_unit)]
            initial_unit = equation.unit[1]
            print('Initial known: ', initial_unit.display())
            converted = initial_unit.convert('mol')
            equation.unit[1] = converted
            print('Equivalent in mol: ', converted.display(0))
            destination = converted.reaction.molar_ratio(unknown)
            equation.unit[1] = destination
            print('Molar ratios of destination: ', destination.display(1))
            final = destination.convert(unit_for_unknown)
            print('RESULT:', final.display())
        else:
            continue
    elif choice == '2':
        name = input('What is your ionic compound? ').strip().lower()
        try:
            attempt = create_compound(name)
            if attempt is None:
                raise MyException("This is not a compound! Let's try again.")
            c = attempt[1]
            print('Ionic Compound: ', u'' + c.formula())
            print('Some properties: ')
            print('g/mol: ', round(c.molar_mass()*10000)/10000)
        except MyException as e:
            print(e)
        except:
            pass
            #print('Uh oh - something went wrong with loading the compound!')
            
    elif choice == '3':
        print(about)
    elif choice == 'exit()':
        break #Breaks out of the indefinite loop.
    else:
        print('''That wasn't any of the valid inputs! Let's try again.''')
####
print('Program has stopped.')
#r = create_compound('sodium')[1].interact_with(create_compound('chlorine')[1])
#u = Unit(r, [0, 0], 6900, 'mg')
exit()









first_case = True
reactants = [{},{}]
def run():
    print('Running Chemical Finder - made by Albert Agustin Amenabar')
    if testing_case:
        choice = '1'
    else:
        print('Do you want to figure out an equation (1), or an ionic compound formula (2)?')
        print('Misc: About (3)')
        choice = input('-> ')
    if choice == '1':
        if testing_case:
            prompt = default
        else:
            print('Enter ONLY 2 reactant names, separated by a +: ')
            prompt = input('-> ')
        reactants_input = prompt.strip().lower().split(' + ')
        global reactants
        reactants = [{},{}]
        #Important Data
        the_acid = -1 #same as False
        the_compound = -1
        # = True
        reaction = False
        if len(reactants_input) < 2:
            print('''No Reaction! You only gave one reactant - let's try again.''')
            return
        for i in range(len(reactants_input)):
            #Fetch
            reactants[i] = Species(reactants_input[i])
            l = reactants[i]
            if l.is_acid() and the_acid == -1:
                the_acid = i
            elif l.is_compound() and the_compound == -1:
                the_compound = i

        if the_acid > -1: #there is an acid and has position in arr
            #print('You have specified an acid.')
            other = reactants[1 - the_acid]
            if other.is_acid():
                print('No Reaction')
            elif other.is_compound():
                #print('lol', reactants[0].formula, reactants[1].formula)
                #print(other.is_base())
                if other.is_base():
                    print('The reaction is a general acid-base neutralisation.')
                    reactants[the_acid] = Compound(reactants[the_acid].name) #switch class
                    other = Compound(other.name) #switch class
                    print(acid_base(reactants[the_acid], other))
                    #acid-base neutralisation reaction.
                else: #non-base
                    reactants[the_acid] = Compound(reactants[the_acid].name) #switch class
                    other = Compound(other.name) #switch class
                    print(acid_base(reactants[the_acid], other))
                    #No reaction
            else:
                print('The reaction is acid-metal.')
                reactants[the_acid] = Compound(reactants[the_acid].name) #switch class
                other = Compound(other.name) #switch class
                print(acid_metal(reactants[the_acid], other))
                #acid-metal reaction. Implement reactivity chart later on.
            '''if reaction:
                for l in reactants:
                    print('reactants:', l.formula)
            else:
                print('No Reaction')'''
        elif the_compound > -1: #No acid present, but there is a compound.
            compound = reactants[the_compound]
            other = reactants[1 - the_compound]
            compound = Compound(compound.name) #switch class
            other = Compound(other.name) #switch class
            if other.is_compound():
                compound_is_more_reactive = compound.cation.is_more_reactive(other.cation) #Is the cation of one more reactive than the other? IF so displacement occurs. smth like that.
                other_is_more_reactive = other.cation.is_more_reactive(compound.cation) #Is the cation of one more reactive than the other? IF so displacement occurs. smth like that.
                print(compound_is_more_reactive, other_is_more_reactive)
                #if compound.cation.name
                if compound.cation.name == other.cation.name and compound.anion.name == other.anion.name:
                    return print('No reaction - You are just adding more of the same compound.')
                elif compound.cation.name == other.cation.name:
                    return print('No reaction - Both compounds have the same cation.')
                elif compound.anion.name == other.anion.name:
                    return print('No reaction - Both compounds have the same anion.')
                #DO A REACTIVE CHART CHECK HERE
                ########
                if compound_is_more_reactive:
                    print('The reaction is a compound double displacement reaction.')
                    print(double_displace(compound, other))
                elif other_is_more_reactive:
                    print('The reaction is a compound double displacement reaction.')
                    print(double_displace(compound, other))
                else:
                    print('No reaction - The other cation is less reactive.')
            else:
                is_more_reactive = True #Is the cation of one more reactive than the other? IF so displacement occurs. smth like that.
                #DO A REACTIVE CHART CHECK HERE
                ########
                if is_more_reactive:
                    print('The reaction is a compound single displacement reaction. (Rn assuming that the metal is more reactive than the cation.)')
                    compound = Compound(compound.name) #switch class
                    other = Compound(other.name) #switch class
                    return print(displace(compound, other))
                else:
                    print('No reaction - The other cation is less reactive.')
        else:
            print('No reaction')
    elif choice == '2':
        name = input('What is your ionic compound? ').strip().lower()
        if ' ' in name:
            print('Ionic Compound: ', u'' + create_compound(name))
        else:
            print('''This is not a compound! Let's try again.''')
    elif choice == '3':
        print(about)
    else:
        print('''That wasn't any of the valid inputs! Let's try again.''')

while (not testing_case) or first_case:
    run()
    first_case = False
