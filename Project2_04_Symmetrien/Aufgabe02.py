import itertools


class TolleListe:
    def __init__(self, list_input):
        self.list_original = []
        self.get_list_short(list_input)

        self.list_length = len(list_input)
        self.list_values = self.get_values()
        self.list_values_amount = len(self.list_values)

        self.list_norm = self.get_list_norm()

    def __repr__(self):
        return str(self.list_values)

    def __eq__(self, other):
        return self.list_norm == other.list_norm

    def get_list_norm(self):
        """
        All representatives share the same norm:
        [list of values] + [length of original list]
        """
        return self.list_values + [self.list_length]

    def get_list_original(self):
        """ returns original list """
        return self.list_original

    def get_list_short(self, list_input):
        """
        Creates list of lists -> [[value_0, pointer_0], ..., [value_n, pointer_n]]
        This will be the representation of given list
        """

        self.list_orig = [list_input[0:2]]
        index = self.list_orig[0][1]

        counter = 0
        while index != -1:

            self.list_orig.append([list_input[index], list_input[index + 1]])
            index = list_input[index + 1]

            counter += 1
            if counter > len(list_input):  # len(list_input)//2 sollte reichen
                raise ValueError("This list is not a TolleListe!")

    def get_values(self):
        """ Gives back a list of values from list_representation """
        return [each[0] for each in self.list_orig]

    def get_all_representations(self):
        """
        Get all possible representations:
        1) Create list with elements, that have to be permuted and substitute 0 with 'x'
        2) Create the permutation
        3) Add 0 after each permuted element that is not 0 (placeholder for pointer)
        4) Replace placeholder for pointer (or -1 at the end) and (if possible) 'x' with 0
        """

        part_begin = [self.list_values[0]] + [0]

        # 1) [all elements of list_values (except first)] + [free zeroes]
        # use list_value_substitute to substitute the value '0' with 'x'
        list_values_substitute = list(map(lambda x: 'x' if x == 0 else x, self.list_values))

        permutation_elements = list_values_substitute[1:] + [0] * (self.list_length - self.list_values_amount*2)
        permutation_elements_amount = len(permutation_elements)

        # 2) Create a list of tuples of all permutations
        all_permutations = list(itertools.permutations(permutation_elements, permutation_elements_amount))

        solution_step_one = []
        solution_final = []

        # 3) Add a zero after each element and add each permutation to solution if not already there (no doubles)
        for each in all_permutations:
            tmp_comb = list(each)

            for i, value in enumerate(tmp_comb):
                if tmp_comb[i] != 0:
                    tmp_comb.insert(i+1, 0)
            new_list = part_begin + tmp_comb

            if new_list not in solution_step_one:
                solution_step_one.append(new_list)

        # 4) Replace the placeholder-0 with the correct pointer to the next element (or -1 at the end)
        #    Replace substitute 'x' with 0

        for combination in solution_step_one:
            solution_part = combination[:]
            for i, each in enumerate(list_values_substitute):
                tmp_index = combination.index(each) + 1

                if i < len(list_values_substitute)-1:
                    solution_part[tmp_index] = combination.index(list_values_substitute[i+1])

                else:
                    solution_part[tmp_index] = -1

                # resubstitution from 'x' to 0
                if each == 'x':
                    solution_part[tmp_index-1] = 0
            solution_final.append(solution_part)

        return solution_final


def multiply_table():
    """ Shows a multiply table depending on list size and values """
    # TODO: Wie mit doppelten Elementen bzw. mit [1, 1] und [1, 1] (umgedreht) verfahren?
    # Aktuell: Es wird nur eine Variante gezählt

    def show_table():
        pass

    list_size = 2
    value_amount = 1

    tmp = [5,2, 5,4, 5,-1, 0, 0]

    tmp_list = TolleListe(tmp)

    print("Anzahl:", len(tmp_list.get_all_representations()))


if __name__ == '__main__':
    tmp_1 = [23, 5, 0, 1337, -1, 42, 3, 0]

    tmp_2 = [23, 6, 0, 1337, -1, 0, 42, 3]

    test_1 = TolleListe(tmp_1)
    test_2 = TolleListe(tmp_2)

    print(test_1 == test_2)

    multiply_table()