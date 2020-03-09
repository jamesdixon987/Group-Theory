class FinGroup:
    def __init__(self, elements):

        self.elements = elements

        def get_inverse(element):
            for other in self.elements:
                if self.operation(other, element) == self.identity:
                    return other

            raise ValueError(element)

    @classmethod
    def _get_identity(cls, elements, operation):
        for element in elements:
            if (cls._is_identity(element, elements, operation)):
                return element

        raise ValueError()

    @classmethod
    def _is_identity(cls, identity, elements, operation) -> bool:
        for element in elements:
            if not operation(identity, element) == element:
                return False

        return True


class GroupElement:
            def __init__(self, element):
                self.element = element

            def __eq__(self, other):
                return self.element == other.element

            def __str__(self):
                return f"Group element: {str(element)}"

            def __pow__(element, power):
                if (power == 0):
                    return self.id
                elif power > 0:
                    return element * pow(element, power - 1)
                else:
                    return self._inverses[pow(element, -power)]
