import sys
from collections import deque

from crossword import *


class CrosswordCreator:
    def __init__(self, crossword):
        self.crossword = crossword
        self.domains = {var: self.crossword.words.copy() for var in self.crossword.variables}

    def letter_grid(self, assignment):
        letters = [[None] * self.crossword.width for _ in range(self.crossword.height)]
        for variable, word in assignment.items():
            for (i, j), letter in zip(variable.cells, word):
                letters[i][j] = letter
        return letters

    def print(self, assignment):
        for row, letters in zip(self.crossword.structure, self.letter_grid(assignment)):
            print("".join((letter or " ") if cell else "█" for cell, letter in zip(row, letters)))

    def save(self, assignment, filename):
        from PIL import Image, ImageDraw, ImageFont

        cell, border, inner = 100, 2, 4
        letters = self.letter_grid(assignment)
        img = Image.new(
            "RGBA", (self.crossword.width * cell, self.crossword.height * cell), "black"
        )
        font = ImageFont.load_default(size=80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if not self.crossword.structure[i][j]:
                    continue
                x, y = j * cell, i * cell
                draw.rectangle(
                    [x + border, y + border, x + cell - border, y + cell - border],
                    fill="white",
                )
                if letters[i][j]:
                    draw.text(
                        (x + cell / 2, y + cell / 2 - inner),
                        letters[i][j],
                        fill="black",
                        font=font,
                        anchor="mm",
                    )
        img.save(filename)

    def solve(self):
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        for var in self.domains:
            self.domains[var] = {w for w in self.domains[var] if len(w) == var.length}

    def revise(self, x, y):
        """Make x arc consistent with y. Return True if x's domain changed."""
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return False
        i, j = overlap
        y_letters = {w[j] for w in self.domains[y]}
        kept = {w for w in self.domains[x] if w[i] in y_letters}
        revised = len(kept) != len(self.domains[x])
        self.domains[x] = kept
        return revised

    def ac3(self, arcs=None):
        if arcs is None:
            arcs = [(x, y) for x in self.domains for y in self.crossword.neighbors(x)]
        queue = deque(arcs)
        while queue:
            x, y = queue.popleft()
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                queue.extend((z, x) for z in self.crossword.neighbors(x) - {y})
        return True

    def assignment_complete(self, assignment):
        return set(assignment) == self.crossword.variables

    def consistent(self, assignment):
        if len(set(assignment.values())) != len(assignment):
            return False
        for var, word in assignment.items():
            if len(word) != var.length:
                return False
            for n in self.crossword.neighbors(var) & assignment.keys():
                i, j = self.crossword.overlaps[var, n]
                if word[i] != assignment[n][j]:
                    return False
        return True

    def order_domain_values(self, var, assignment):
        """Least-constraining value first."""
        free = self.crossword.neighbors(var) - assignment.keys()

        def ruled_out(word):
            count = 0
            for n in free:
                i, j = self.crossword.overlaps[var, n]
                # срезы не падают, если слово неподходящей длины
                count += sum(w[j : j + 1] != word[i : i + 1] for w in self.domains[n])
            return count

        return sorted(self.domains[var], key=ruled_out)

    def select_unassigned_variable(self, assignment):
        """Minimum remaining values, ties broken by highest degree."""
        unassigned = self.crossword.variables - assignment.keys()
        return min(
            unassigned,
            key=lambda v: (len(self.domains[v]), -len(self.crossword.neighbors(v))),
        )

    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for word in self.order_domain_values(var, assignment):
            assignment[var] = word
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            del assignment[var]
        return None


def main():
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    structure, words = sys.argv[1], sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    creator = CrosswordCreator(Crossword(structure, words))
    assignment = creator.solve()

    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
