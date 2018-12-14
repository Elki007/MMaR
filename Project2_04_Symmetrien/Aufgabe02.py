from sympy.utilities.iterables import multiset_permutations
from math import factorial as fac


class TolleListe:
    def __init__(self, list_input, normalized=False):
        """ Initialize a TolleListe with an representative or with the normalization form"""
        if normalized is False:
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
        return str(self.list_norm)

    def __eq__(self, other):
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
        1) Creates a list with elements and placeholder (for pointer) and zeros if given
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
        if permutation_elements == []:
            return [[self.list_values[0], -1]]

        # 2) Create a list of lists of all permutations
        #    0s are treated all the same (e.g. just one possibility for [0, 0, 0, 0])
        solution_step_one = list(multiset_permutations(permutation_elements))

        # 3) Add first element of self.list_values and its pointer '0'
        #    Flatten the list so there is no list in a list
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


def multiply_table(value_amount=5, list_size=10, short=False):
    """ Shows a multiply table depending on list size and values """

    # TODO: n! / (n - k)!

    # Aktuell: Es wird nur eine Variante gezählt

    def show_table():
        pass

    table = []

    for i in range(1, value_amount + 1):
        table.append([])
        for j in range(2, list_size):
            if j < i * 2:
                table[-1].append(0)
            else:
                if not short:
                    tmp_norm = [0] * i + [j]
                    tmp_tolleliste = TolleListe(tmp_norm, normalized=True)
                    table[-1].append(len(tmp_tolleliste.get_all_representations()))
                else:
                    tmp_calculation = fac(j) // fac(j-i)
                    table[-1].append(tmp_calculation)

    for each in table:
        print(each)


if __name__ == '__main__':
    # tmp_1 = [23,42,1337,8]
    # tmp_1 = [23, 2, 45, 4, 7, -1, 0, 0, 0, 0]
    # tmp_2 = [23, 6, 0, 1337, -1, 0, 42, 3]

    # test_1 = TolleListe(tmp_1)
    # test_2 = TolleListe(tmp_2)

    # alll = test_1.get_all_representations()

    # print(len(alll))
    # for each in alll:
    #    print(each)

    multiply_table(10, 20, short=True)
