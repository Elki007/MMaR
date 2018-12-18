from sympy.utilities.iterables import multiset_permutations
from math import factorial as fac
import sys



class TolleListe:
    def __init__(self, list_input, normalized=False):
        """
        Initialize a TolleListe with a representative or with the normalization form
        not normalized e.g.: [23,5,0,1337,-1,42,3,0]
        normalization form e.g.: [23,42,1337, 8] -> [value_1, ... , value_n, length]
        """
        if not normalized:
            self.created_as_norm = normalized
            self.list_original = list_input
            self.list_organized = self.transform_list_organized()

            self.list_length = len(list_input)
            self.list_values = [each[0] for each in self.list_organized]
            self.list_values_amount = len(self.list_values)

            self.list_norm = self.list_values + [self.list_length]

            self.all_representatives = self.calculate_all_representations()

        else:
            self.created_as_norm = normalized
            self.list_original = []  # no original representative if object was created in normalization form
            self.list_organized = []  # no organized form if object was created in normalization form

            self.list_length = list_input[-1]
            self.list_values = list_input[:-1]
            self.list_values_amount = len(self.list_values)

            self.list_norm = list_input

            self.all_representatives = self.calculate_all_representations()

    def __repr__(self):
        """ Return normalisation """
        return str(self.list_norm)

    def __eq__(self, other):
        """ Compares each normalisation """
        return self.list_norm == other.list_norm

    def get_list_norm(self):
        """
        All representatives share the same norm:
        [list of values] + [length of original list]
        """
        return self.list_norm

    def get_list_original(self):
        """ returns original list """
        return self.list_original

    def get_list_organized(self):
        """ Creates organized list of lists of given representative
        -> [[value_0, pointer_0], ..., [value_n, pointer_n]]"""
        return self.list_organized

    def get_values(self):
        """ Gives back a list of values from list_representation """
        return self.list_values

    def get_all_representations(self):
        """ Return every possible representative of this structure """
        return self.all_representatives

    def transform_list_organized(self):
        """
        Creates list of lists -> [[value_0, pointer_0], ..., [value_n, pointer_n]]
        This will be the representation of given list
        """

        if self.created_as_norm is False:
            tmp_list = [self.list_original[0:2]]
            index = tmp_list[0][1]

            counter = 0
            while index != -1:

                tmp_list.append([self.list_original[index], self.list_original[index + 1]])
                index = self.list_original[index + 1]

                counter += 1
                if counter > len(
                        self.list_original):  # len(list_input)//2 sollte reichen TODO: einmal darüber nachdenken
                    raise ValueError("This list is not a TolleListe!")
            return tmp_list
        else:
            return []

    def calculate_all_representations(self):
        """
        Get all possible representations:
        1) Creates a list with [values[1:], placeholder (for pointer)] and zeros if given, as basis for permutation
        2) Create the permutation
        3) Add first element of self.list_values and its pointer '0' and flatten the list so there is no list in a list
        4) Replace placeholder for pointer (or -1 at the end)
        """

        # 3 steps to final solution
        # solution_step_one = []  # will be initialized later
        solution_step_two = []
        # solution_step_three = []  # will be initialized later
        solution_final = []

        # 1) [element of list_values (except first), placeholder] + [free zeroes]
        permutation_elements = [[j, str(i + 1)] for i, j in enumerate(self.list_values[1:])]
        permutation_elements += [0] * (self.list_length - self.list_values_amount * 2)

        # In case there is just one element with a list size of 2
        # TODO: Adding zeros necessary?
        if permutation_elements == []:
            return [[self.list_values[0], -1]]

        # 2) Create a list of lists of all permutations
        #    0s are treated all the same (e.g. just one possibility for [0, 0, 0, 0])
        solution_step_one = list(multiset_permutations(permutation_elements))

        # 3) Add first element of self.list_values and its pointer '0'
        #    Flatten the list so there is no list in a list: [1,[2,3],2] -> [1,2,3,2]
        flatten = lambda *n: (e for a in n for e in (flatten(*a) if isinstance(a, (tuple, list)) else (a,)))

        first_value = [self.list_values[0]] + ['0']
        for each in solution_step_one:
            tmp = list(flatten(first_value, each))
            solution_step_two.append(tmp)

        # 4) Replace the placeholder with the correct pointer to the next element (or -1 at the end)
        for combination in solution_step_two:
            solution_step_three = list(combination)
            for i, each in enumerate(combination):
                if type(each) == str:
                    if int(each) + 1 < self.list_values_amount:
                        solution_step_three[i] = combination.index(str(int(each) + 1)) - 1
                    else:
                        solution_step_three[i] = -1
            solution_final.append(solution_step_three)

        return solution_final


def permutation_table(value_amount=5, list_size=10, short=False):
    """
    Shows a multiply table depending on list size and values
    short=False --> Calculate every representation with the algorithm
    short=True  --> Calculate the amount of representations in a combinatoric way
    """

    def show_table(table):
        """ Show the table with its values """

        # calculate space between rows -> largest number in row + 2 spaces
        space_between_row = [0]*(len(table[0])+1)

        for row in table:
            for i, column in enumerate(row):
                if len(str(column))+2 > space_between_row[i]:
                    space_between_row[i] = len(str(column))+2

        # create table head
        table_head = "x_ |"
        for column_index in range(len(table[0])):
            abstand = (space_between_row[column_index] - (len(str(column_index+2))+2)) // 2
            ungerade = 0 if (space_between_row[column_index] - (len(str(column_index+2))+2)) % 2 == 0 else 1
            table_head += " "*abstand + "_" + str(column_index+2) + "_" + " "*abstand + " "*ungerade + "|"
        table_head += "  <- size of list"

        print(table_head)

        # create table row
        for i, column in enumerate(table):
            table_row = str(i + 1) + "  |" if i+1 < 10 else str(i+1) + " |"

            for j, row in enumerate(column):
                abstand = (space_between_row[j] - len(str(row))) // 2
                ungerade = 0 if (space_between_row[j] - len(str(row))) % 2 == 0 else 1
                table_row += " "*abstand + str(row) + " "*abstand + " "*ungerade + "|"
            print(table_row)
        print("^\nAmount of values")

    #####
    # Calculation of the table
    #####

    table = []

    for i in range(1, value_amount + 1):
        table.append([])
        # calculate with creating new TolleListe objects
        if not short:
            for j in range(2, list_size + 1):
                if j < i * 2:
                    table[-1].append(0)
                else:
                    tmp_norm = [0] * i + [j]
                    tmp_tolleliste = TolleListe(tmp_norm, normalized=True)
                    table[-1].append(len(tmp_tolleliste.get_all_representations()))
        # calculate with combinatoric: n! / (n-k)!
        else:
            for j in range(1, list_size):
                if j+1 < i * 2:
                    table[-1].append(0)
                else:
                    n, k = j-i, i-1
                    tmp_calculation = fac(n) // fac(n-k)
                    table[-1].append(tmp_calculation)

    show_table(table)


def aufgabe2_1(beispiel):
    """
    Example for exercise 2_1:
        Betrachten Sie das obige Beispiel mit 3 Listenelementen und 8 Speicherplätzen. Schreiben Sie ein Programm,
        das alle äquivalenten Repräsentation der gleichen Liste erzeugt. Ihr Programm sollte auch für längere Listen
        funktionieren, man muss aber aufpassen, da der Aufwand sehr schnell steigt.
    """

    if beispiel == 1:
        list_example = [23, 5, 0, 1337, -1, 42, 3, 0]
    elif beispiel == 2:
        list_example = [23, 5, 0, 1337, -1, 42, 3, 0, 0, 0, 0, 0, 0, 0]
    else:
        list_example = [0, 5, 0, 0, -1, 0, 3, 0, 0]

    symmetry_list = TolleListe(list_example)

    print(f"Number of representatives: {len(symmetry_list.get_all_representations())}\n")

    for each in symmetry_list.get_all_representations():
        print(each)


def aufgabe2_2_falsch(list_example=[23, 5, 0, 1337, -1, 42, 3, 0]):
    """
    F A L S C H !
    Example for exercise 2_2:
        Zunächst eine Theorieaufgabe: Bestimmen Sie die Struktur der Symmetriegruppe. Welche Transformationen sind
        möglich, und was machen diese (prinzipiell)?
        Visualisieren Sie die Gruppenstruktur, indem Sie eine Multiplikationstabelle berechnen.
    """
    # Transformationen:
    # - Verschiebungen

    symmetry_list = TolleListe(list_example)

    print(f"Struktur der Symmetriegruppe von {list_example} is --> {symmetry_list.get_list_norm()}\n")

    permutation_table(14, 43, short=True)


def aufgabe2_2():
    """
    Example for exercise 2_2:
        Zunächst eine Theorieaufgabe: Bestimmen Sie die Struktur der Symmetriegruppe. Welche Transformationen sind
        möglich, und was machen diese (prinzipiell)?
        Visualisieren Sie die Gruppenstruktur, indem Sie eine Multiplikationstabelle berechnen.
    """

    def show_table(table):
        """ Prints cayley table """
        print("\nCayley table:")
        for row in table:
            for element in row:
                print(str(element) + "".ljust(4), end='')
            print()
        print()

    def neutral_element_into_cayley_table():
        fixed_coordinates = []

        # neutral elements
        for i in range(value_count-2):
            cayley_table[i][i] = neutral_element
            fixed_coordinates.append((i, i))
        cayley_table[value_count-2][value_count-1] = neutral_element
        fixed_coordinates.append((value_count-2, value_count-1))
        cayley_table[value_count-1][value_count-2] = neutral_element
        fixed_coordinates.append((value_count-1, value_count-2))

        # elements in first row
        for i in range(1, value_count):
            cayley_table[0][i] = values_to_fill_in[i-1]
            fixed_coordinates.append((0, i))

        # elements in first column
        for i in range(1, value_count):
            cayley_table[i][0] = values_to_fill_in[i-1]
            fixed_coordinates.append((i, 0))

        return fixed_coordinates

    def check_table_has_no_spaces(table):
        """
        returns True -> table contains no spaces
        returns False -> table contains spaces
        """
        for row in table:
            if '-' in row:
                return False
        return True

    def check_row_and_column(table, x, y):
        row = table[y]
        column = [table[y][x] for y in range(value_count)]
        lines_to_check = [row] + [column]

        for line in lines_to_check:
            values_should_be_used = values[:]
            for each in line:
                if each in values_should_be_used:
                    values_should_be_used.pop(values_should_be_used.index(each))
                elif each == '-':
                    pass
                else:
                    return False
        return True

    def check_table_numbers(table):
        """
        returns True -> every value is just one time in line (horizontally or vertically)
        returns False ->  more of the same value in line (horizontally or vertically)
        """
        # create lines -> horizontally, vertically
        lines_to_check = [row for row in table]  # horizontal
        lines_to_check += [[table[j][i] for j in range(value_count)] for i in range(value_count)]  # vertical

        # proof each line if all elements of values are represented in each line)
        # better approach but what about double values?
        """
        for line in lines_to_check:
            if not all(element in line for element in values):
                return False
        """

        # proof each line if all elements of values are represented in each line)
        # first naive implementation:
        for line in lines_to_check:
            values_should_be_used = values[:]
            for each in values:
                if each in line:
                    values_should_be_used.pop(values_should_be_used.index(each))
            if len(values_should_be_used) > 0:
                return False
        return True

    def find_empty_location(table):
        for y in range(value_count):
            for x in range(value_count):
                if table[y][x] == '-':
                    return x, y
        return False

    def calculate_table(table, x=0, y=0):
        """ Backtracking to solve cayley table """

        # solution
        if check_table_has_no_spaces(table):
            print("NO WAY")
            return True

        # get next empty space
        x, y = find_empty_location(table)
        print("places:", (x, y))

        if (x, y) == (4, 1):
            pass

        for element in values_to_fill_in:
            if table[y][x] == '-' and (x, y) not in fixed_fields:
                table[y][x] = element

                # does it fit? work with it, otherwise replace it with '-'
                if check_row_and_column(table, x, y):
                    # find next x,y
                    x, y = find_empty_location(table)

                    # same problem with one more element
                    if calculate_table(table, x, y):
                        return True
                    else:
                        if (x, y) not in fixed_fields:
                            table[y][x] = '-'

                else:
                    if (x, y) not in fixed_fields:
                        table[y][x] = '-'
            else:
                print("WHAT", (x, y))

        return False

    #####
    # Data example
    #####
    list_example = [23, 5, 0, 1337, 7, 42, 3, 2, 9, 7, -1]  #, 0, 4, -1]

    #####
    # Get data from given list of representative
    #####
    symmetry_list = TolleListe(list_example)

    values = symmetry_list.get_values()
    value_count = len(values)

    neutral_element = values[0]

    #####
    # Calculation of cayley table
    #####

    cayley_table = [['-' for _ in range(value_count)] for _ in range(value_count)]

    # fill in neutral elements and neutral-multiplications
    values_to_fill_in = values[1:]  # is used in calculate_table
    fixed_fields = neutral_element_into_cayley_table()  # is used in calculate_table
    print("Fixed fields:", fixed_fields)
    print("Values to fill in:", values_to_fill_in)
    show_table(cayley_table)

    # example
    """
    cayley_table = [[23, 42, 1337],
                    [42, 1337, 23],
                    [1337, 23, 42]]
    """

    calculate_table(cayley_table)
    print("DEBUG type of final_table:", type(cayley_table))
    if type(cayley_table) is list:
        show_table(cayley_table)


def aufgabe2_3():
    """
    Example for exercise 2_3:
        1) Gegeben seien zwei beliebige Repräsentanten von Listen. Wie bestimmt man, ob diese die
           gleiche Liste darstellen?
        2) Kann man einen schnelleren Algorithmus finden, wenn man davon ausgeht, dass man sehr viele
           Listenrepräsentanten in ihre zugehörigen Gruppen gleicher Darstellungen einordnen möchte?
           (Tipp: Normalisierung)
    """
    # 1) Wir vergleichen beide Normalformen miteinander (möglich mit '==' durch __eq__())
    # 2) Schneller als? Wir nutzen Dictionaries und als key bspw. ein Tupel der Normalform.
    pass


if __name__ == '__main__':
    sys.setrecursionlimit(3500)
    """ Testläufe sind beispielhaft in den Funktionen aufgabe* zu finden """

    #aufgabe2_1(1)
    #aufgabe2_2_falsch()
    aufgabe2_2()
    #aufgabe2_2()
    #aufgabe2_3()  # just comments
    pass


