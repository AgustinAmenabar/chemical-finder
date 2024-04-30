import math
about = '''
#ABOUT
This is an "original" project, made by Albert Agustin Amenabar!
It helps you find formulas of ionic compounds and acids from name, and even determine chemical equations for you.
As a bonus, you may get balanced equations!
#HISTORY
The latest entry is the last update to this program of the version you have.
4/9/2023: Started the project. Made a somewhat working system to find ionic compound formulas from their names, along with acids. Also tried implementing the typical acid-base reaction without balancing yet.
5/9/2023: Added a working balancing system, up to a coefficient limit (set to 10) due to efficiency limitations. Cleaned up code a lil' bit, added more ions and products, and implemented acid-metal reactions (they are easier).
6/9/2023: Implemented general single displacement reactions (does not yet take into account reactivities) and implemented more failsafe measures
'''
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
species = []
testing_case = False
default = 'sodium chloride + iron sulfate'#'hydrochloric acid + aluminium'
limit = 20 ##################################################LIMIT
#this is periodic table of ions
cation = {
    'hydrogen': ['H', 1, 0],
    'lithium': ['Li', 1],
    'sodium': ['Na', 1, -2.71],
    'potassium': ['K', 1, -2.94],
    'rubidium': ['Rb', 1],
    'cesium': ['Cs', 1],

    'beryllium': ['Be', 2],
    'magnesium': ['Mg', 2, -2.36],
    'calcium': ['Ca', 2, -2.87],
    'strontium': ['Sr', 2, -2.9],
    'barium': ['Ba', 2, -2.91],


    'chromium': ['Cr', 2, -0.74],
    'manganese': ['Mn', 2, -1.18],
    'iron': ['Fe', 2, -0.44],
    'cobalt': ['Co', 2, -0.28],
    'nickel': ['Ni', 2, -0.24],
    'copper': ['Cu', 2, 0.34],
    'zinc': ['Zn', 2, -0.76],
    'silver': ['Ag', 1, 0.8],
    'cadmium': ['Cd', 2, -0.4],
    'tin': ['Sn', 2, -0.14],
    'mercury': ['Hg', 2],
    'lead': ['Pb', 2, -0.13],
    'aluminium': ['Al', 3, -1.68],
    'gallium': ['Ga', 3, -0.56],


    'ammonium': ['N H4', 1],
}
anion = {
    'fluoride': ['F', 1],
    'chloride': ['Cl', 1],
    'bromide': ['Br', 1],
    'iodide': ['I', 1],
    'oxide': ['O', 2],
    'sulfide': ['S', 2],
    'nitride': ['N', 3],
    'azide': ['N3 ', 1],
    'phosphide': ['P', 3],
    'peroxide': ['O2', 2],
    'nitrite': ['N O2', 1],
    'nitrate': ['N O3', 1],
    'acetate': ['C H3 C O O', 1],
    'ethanoate': ['C H3 C O O', 1],
    'sulfite': ['S O3', 2],
    'sulfate': ['S O4', 2],
    'thiosulfate': ['S2 O3', 2],
    'bisulfate': ['H S O4', 1],
    'carbonate': ['C O3', 2],
    'bicarbonate': ['H C O3', 1],
    'phosphite': ['P O3', 3],
    'phosphate': ['P O4', 3],
    'chlorate': ['Cl O3', 1],
    'perchlorate': ['Cl O4', 1],
    'manganate': ['Mn O4', 2],
    'permanganate': ['Mn O4', 1],
    'hydroxide': ['O H', 1],
}
acid_name = {
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
    'perchloric': 'perchlorate',
}

product = {
    'hydrogen': 'H2',
    'water': 'H2 O',
    'carbon dioxide': 'C O2',
    'ammonia': 'N H3',
    'sulfur dioxide': 'S O2',
}

other_acids = {
    'carbon dioxide': 'C O2'
}

def unroman(value):
    n = 0
    if value == 'iv':
        return 4
    if value == 'ix':
        return 9
    for l in value:
        add = 0
        if l == 'i':
            add = 1
        elif l == 'v':
            add = 5
        elif l == 'x':
            add = 10
        n = n + add
    return n
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

def identify_ion_version(name):
    specifiesOxidation = False
    if '(' in name: #oxidation state of cation
        specifiesOxidation = True
        this_cation = cation[name.split('(')[0]][0].replace(' ','').translate(SUB)
        cNumber = unroman(name.split('(')[1].split(')')[0])
    else:
        this_cation = cation[name][0].replace(' ','').translate(SUB)
        cNumber = cation[name][1]
    return Cation(name, this_cation, cNumber)
    #Assume no oxidation states, just defaulting to the common one.
    if name in cation:
        return Cation(name, cation[name][0], cation[name][1], cation[name][2])
    elif name in anion:
        return Anion(name, anion[name][0], anion[name][1])
    else:
        return None
def identify_ions_of(name):
    name = name.split()
    specifiesOxidation = False
    if '(' in name[0]: #oxidation state of cation
        specifiesOxidation = True
        this_cation = cation[name[0].split('(')[0]][0].replace(' ','').translate(SUB)
        cNumber = unroman(name[0].split('(')[1].split(')')[0])
    else:
        this_cation = cation[name[0]][0].replace(' ','').translate(SUB)
        cNumber = cation[name[0]][1]
    this_anion = anion[name[1]][0].replace(' ','').translate(SUB)
    aNumber = anion[name[1]][1]
    #print(result)
    return {
        'cation': Cation(name[0].split('(')[0], this_cation, cNumber, cation[name[0].split('(')[0]][2]),
        'anion': Anion(name[1].split('(')[0], this_anion, aNumber),
    }
def ionic_compound(name):
    if 'acid' in name:
        ions = identify_ions_of_acid(name)
        return Compound(cation = ions['cation'], anion = ions['anion']).format()
    ions = identify_ions_of(name)
    return Compound(cation = ions['cation'], anion = ions['anion']).format()
def identify_ions_of_acid(name):
    name = name.split()
    name1 = 'hydrogen ' + acid_name[name[0]] #convert to IUPAC name
    return identify_ions_of(name1)
    
def form_acid(name):
    #name = name.split()
    ions = identify_ions_of_acid(name)
    return balance_charges(ions['cation'], ions['anion'])

def salt(r1, r2):
    #print('form', r2.cation, r1.anion)
    form = Compound(cation = r2.cation, anion = r1.anion)
    return form
def opposite_salt(r1, r2):
    #print('form', r2.cation, r1.anion)
    form = Compound(cation = r1.cation, anion = r2.anion)
    return form
def other_products(r1, r2):
    products = {
        'hydrogen hydroxide': ['water'], #typical acid-base
        'hydrogen oxide': ['water'], #acid-oxide
        'hydrogen carbonate': ['water', 'carbon dioxide'], #acid-carbonate
        'hydrogen bicarbonate': ['water', 'carbon dioxide'], #acid-bicarbonate
        'hydrogen sulfite': ['water', 'sulfur dioxide'], #acid-sulfite
        'ammonium hydroxide': ['water', 'ammonia'],
    }
    form = Compound(cation = r1.cation, anion = r2.anion)
    #print('forms')
    #print(r1.cation.formula, r2.cation.formula, form)
    prods = []
    for i in products[form.name]:
        prods.append(i)
    return prods#result should be an array of products joined ' + '

def format_equation(species, coefficients):
    Reactants = species[0]
    Products = species[1]
    nreactants = len(Reactants) #this wont change
    nproducts = len(Products) #this wont change
    ReactantCoefficients = coefficients[0]
    ProductCoefficients = coefficients[1]
    #print(Reactants, Products)
    #print(j.name, j.atom_count())
    reactant_display = []
    product_display = []
    reactant_format = []
    product_format = []
    for a in range(nreactants):
        if isinstance(Reactants[a], Compound):
            reactant_format.append(Reactants[a].format())
        else:
            reactant_format.append(Reactants[a].replace(' ','').translate(SUB))
    for a in range(nproducts):
        if isinstance(Products[a], Compound):
            product_format.append(Products[a].format())
        else:
            product_format.append(Products[a].replace(' ','').translate(SUB))
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
    return ' + '.join(reactant_display) + ' ---> ' + ' + '.join(product_display)

def displace(compound, metal):
    salt_product = salt(compound, metal)
    other_product = Compound(compound.cation.name)
    Reactants = [compound, metal]
    Products = [salt_product, other_product]
    a = balance(Reactants, Products)
    return format_equation([Reactants, Products], a)

def double_displace(compound1, compound2):
    salt1 = salt(compound1, compound2)
    salt2 = opposite_salt(compound1, compound2)
    Reactants = [compound1, compound2]
    Products = [salt1, salt2]
    a = balance(Reactants, Products)
    return format_equation([Reactants, Products], a)

def acid_metal(acid, metal):
    salt_product = salt(acid, metal)
    other_product = product['hydrogen']
    Reactants = [acid, metal]
    Products = [salt_product, other_product]
    a = balance(Reactants, Products)
    return format_equation([Reactants, Products], a)

def acid_base(acid, base):
    '''products = [
        salt,
        water,
    ]'''
    #print('acid and base:', acid.name, base.name)
    j = salt(acid, base)
    k = other_products(acid, base)
    r = acid.format() + ' + ' + base.format()
    Reactants = [acid, base]
    Products = [j]
    p = j.format()
    for i in k:
        #print('translate', product[i])
        Products.append(product[i])
        p = p + ' + ' + i.translate(SUB)
    a = balance(Reactants, Products)
    return format_equation([Reactants, Products], a)

def formatCompoundFromIons(cation, anion):
    return Compound(cation = cation, anion = anion)

def append_counts(count, new):
    total_atom_count = count
    for i in new:
        if i not in total_atom_count:
            total_atom_count[i] = new[i]
        else:
            total_atom_count[i] = total_atom_count[i] + new[i]
    return total_atom_count

def compare_counts(a, b):
    return a == b
def count_atoms_in(species, quantity = 1):
    species = species.split(' ')
    atom_count = {}
    for i in species:
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
        #cc = 
        if name not in atom_count:
            atom_count[name] = amount * quantity
        else:
            atom_count[name] = atom_count[name] + amount * quantity
    return atom_count



def balance(Reactants, Products):
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
    limit = 10 ##################################################LIMIT
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
                if isinstance(Reactants[reactantIndex], Compound):
                    reactant_count = append_counts(reactant_count, Reactants[reactantIndex].atom_count(ReactantCoefficients[reactantIndex]))
                else:
                    reactant_count = append_counts(reactant_count, count_atoms_in(Reactants[reactantIndex], ReactantCoefficients[reactantIndex]))
            product_count = {}
            for productIndex in range(nproducts):
                #print('check salt', Products[productIndex])
                if isinstance(Products[productIndex], Compound):
                    product_count = append_counts(product_count, Products[productIndex].atom_count(ProductCoefficients[productIndex]))
                else:
                    product_count = append_counts(product_count, count_atoms_in(Products[productIndex], ProductCoefficients[productIndex]))
            #print('COEFFICIENTS', ReactantCoefficients, ProductCoefficients)
            #print('IS IT EQUAL?', reactant_count, product_count)
            if compare_counts(reactant_count, product_count):
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
    return [ReactantCoefficients, ProductCoefficients]
class Species:
    def __init__(self, name):
        official = ''
        self.name = name
        sname = name.split()

        if 'acid' in name:
            #official = 'hydrogen ' + acid_name[sname[0]]
            i = identify_ions_of_acid(name)
            cIon = i['cation']
            aIon = i['anion']
            self.cation = cIon
            self.anion = aIon
        else:
            if self.is_compound():
                i = identify_ions_of(name)
                cIon = i['cation']
                aIon = i['anion']
                self.cation = cIon
                self.anion = aIon
            else: #If it is just a metal, ALWAYS assumes it will readily cationise
                i = identify_ion_version(name)
                self.cation = i
            '''if aIon.name == 'hydroxide' or aIon.name == 'oxide':
                self.pH = 'base'
            else:
                self.pH = 'neutral' '''
        #self.formula = formatCompoundFromIons(self.cation, self.anion)
    def is_compound(self):
        if ' ' in self.name:
            #print("SPACE WEHEE")
            return True
        else:
            return False
    def is_acid(self):
        if not self.is_compound():
            return False
        if 'acid' in self.name:
            #print("ACID WEHEE")
            return True
        elif self.cation.name in ['hydrogen', 'ammonium']:
            return True
        else:
            return False
    def is_base(self):
        name = self.anion.name
        #print(self.anion.name)
        if name in ['hydroxide', 'oxide', 'carbonate']:
            return True
        else:
            return False
class Ion:
    def __init__(self, name, formula, charge, potential = None):
        self.name = name
        self.formula = formula
        self.charge = charge
        self.potential = potential


class Cation(Ion):
    def __init__(self, name, formula, charge, potential = None):
        super().__init__(name, formula, charge, potential)
    def normalise(self):
        print(self.name)
        return Element(self.name)
    def is_more_reactive(self, other):
        print(other.name)
        if other.name in cation:
            print(self.potential, other.potential)
            if self.potential is None:
                p1 = -100
            else:
                p1 = cation[self.name][2]
            if other.potential is None:
                p2 = -100
            else:
                p2 = cation[other.name][2]
            return p1 < p2
        else:
            print('f')
            return False
class Anion(Ion):
    def __init__(self, name, formula, charge, potential = None):
        super().__init__(name, formula, charge, potential)
        
class Compound:
    def __init__(self, name='', cation='', anion=''):
        if len(name)>0:
            self.name = name
            if 'acid' in self.name:
                ions = identify_ions_of_acid(self.name)
                self.cation = ions['cation']
                self.anion = ions['anion']
            else:
                if self.is_compound(): #compound
                    
                    ions = identify_ions_of(self.name)
                    self.cation = ions['cation']
                    self.anion = ions['anion']
                else:
                    ions = identify_ion_version(self.name)
                    self.cation = ions
            #print(self)
        else:
            self.cation = cation
            self.anion = anion
            #print('cation and anion:', cation, anion)
            self.name = cation.name + ' ' + anion.name
    '''def number_of_cations(self):

    def number_of_anions(self):
    '''
    def is_compound(self):
        return ' ' in self.name
    def balanced_charges(self):
        c = self.cation.charge
        a = self.anion.charge
        cNumber2 = int(a / math.gcd(c, a))
        aNumber2 = int(c / math.gcd(c, a))
        return {
            'cation': cNumber2,
            'anion': aNumber2
        }

    def atom_count(self, amount = 1):
        if self.is_compound():
            #cation
            num_cations = self.balanced_charges()['cation']
            cation_atom_count = count_atoms_in(cation[self.cation.name.split('(')[0]][0], num_cations * amount)
            #anion
            num_anions = self.balanced_charges()['anion']
            anion_atom_count = count_atoms_in(anion[self.anion.name.split('(')[0]][0], num_anions * amount)
            total_atom_count = {}
            total_atom_count = append_counts(total_atom_count, cation_atom_count)
            total_atom_count = append_counts(total_atom_count, anion_atom_count)
            return total_atom_count
        else:#assume 1 as amount as no balance necessary
            return count_atoms_in(cation[self.cation.name.split('(')[0]][0], amount)

    def format(self):
        if not self.is_compound():
            return self.cation.formula.replace(' ','').translate(SUB)
        nums = self.balanced_charges()
        cNumber2 = nums['cation']
        aNumber2 = nums['anion']
        if cNumber2 == 1:
            cation_display = self.cation.formula
        else:
            if len(cation[self.cation.name.split('(')[0]][0].split(' ')) > 1:
                cation_display = '(' + self.cation.formula + ')' + str(cNumber2).translate(SUB)
            else:
                cation_display = self.cation.formula + str(cNumber2).translate(SUB)
        if self.is_compound():
            if aNumber2 == 1:
                anion_display = self.anion.formula
            else:
                if len(anion[self.anion.name.split('(')[0]][0].split(' ')) > 1:
                    anion_display = '(' + self.anion.formula + ')' + str(aNumber2).translate(SUB)
                else:
                    anion_display = self.anion.formula + str(aNumber2).translate(SUB)
            return cation_display + anion_display
        else:
            return cation_display

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
            print('Ionic Compound: ', u'' + ionic_compound(name))
        else:
            print('''This is not a compound! Let's try again.''')
    elif choice == '3':
        print(about)
    else:
        print('''That wasn't any of the valid inputs! Let's try again.''')

while (not testing_case) or first_case:
    run()
    first_case = False
