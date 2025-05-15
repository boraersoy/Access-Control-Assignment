from typing import Set, List
from itertools import chain, combinations


class SecurityLabel:
    def __init__(self, categories: Set[str]):
        self.categories = categories

    def __le__(self, other: 'SecurityLabel') -> bool:
        return self.categories.issubset(other.categories)

    def __ge__(self, other: 'SecurityLabel') -> bool:
        return self.categories.issuperset(other.categories)

    def __eq__(self, other: 'SecurityLabel') -> bool:
        return self.categories == other.categories

    def __repr__(self):
        return f"{sorted(self.categories)}"


class Subject:
    def __init__(self, name: str, label: SecurityLabel):
        self.name = name
        self.label = label

    def __repr__(self):
        return f"Subject({self.name}, Label={self.label})"


class Object:
    def __init__(self, name: str, label: SecurityLabel):
        self.name = name
        self.label = label

    def __repr__(self):
        return f"Object({self.name}, Label={self.label})"


def can_read(subject: Subject, obj: Object) -> bool:
    return subject.label <= obj.label  # ⊆


def can_write(subject: Subject, obj: Object) -> bool:
    return subject.label >= obj.label  # ⊇


def powerset(s: Set[str]) -> List[Set[str]]:
    """Generate all subsets of the category set"""
    return [set(comb) for comb in chain.from_iterable(combinations(s, r) for r in range(len(s)+1))]


def generate_lattice(categories: Set[str]) -> List[SecurityLabel]:
    return [SecurityLabel(label) for label in powerset(categories)]


def show_lattice(labels: List[SecurityLabel]):
    print("Lattice Partial Order (Label A ⊆ Label B):")
    for a in labels:
        for b in labels:
            if a <= b and a != b:
                print(f"  {a} ⊆ {b}")
