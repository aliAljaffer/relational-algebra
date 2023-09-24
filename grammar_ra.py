from parsimonious import Grammar
from parsimonious.nodes import NodeVisitor as nv

ra_grammar = Grammar(
    """
    expr = (term (space? set_op space? term)?) / term
    term = open_paren* operation open_bracket space? in_bracket space? closed_bracket space? open_paren in_paren closed_paren
    in_paren = expr / (word ("*" word)*) / word
    space = ~r"\s*"
    operation = "SELE_" / "PROJ_" / "INTE_" / "JOIN_"
    set_op = "U" / "-" / "X" / "INTE" / "*"
    in_bracket = (condition_statement) / (word ("," space? word)?)* / word
    condition_statement = word space? comparison_op space? word_or_num (space? logical space? condition_statement)*
    word_or_num = num* / word
    num = (int frac exp) / (int exp) / (int frac) / int
    int = "-"? ((digit1to9 digits) / digit)
    frac = "." digits
    exp = e digits
    digits = digit+
    e = "e+" / "e-" / "e" / "E+" / "E-" / "E"
    digit1to9 = ~"[1-9]"
    digit = ~"[0-9]"
    word = ~r"[\w]+"
    logical = "OR" / ","
    open_bracket = "{"
    closed_bracket = "}"
    open_paren = "("
    closed_paren = ")"
    comparison_op = "<=" / ">=" / "!=" / "<" / ">" / "="
    """
)


class RAVisitor(nv):
    def visit_expr(self, node, visited_children):
        """ Returns the overall output. """

    def visit_term(self, node, visited_children):
        """ Returns the overall output. """

    def visit_set_op(self, node, visited_children):
        """ Returns the overall output. """

    def visit_term(self, node, visited_children):
        """ Returns the overall output. """

    def visit_comparison_op(self, node, visited_children):
        """ Returns the overall output. """

    def visit_condition_statement(self, node, visited_children):
        """ Returns the overall output. """

    def visit_in_paren(self, node, visited_children):
        return

    def visit_in_bracket(self, node, visited_children):
        return

    def visit_operationn(self, node, visited_children):
        return

    def visit_logical(self, node, visited_children):
        return

    def visit_word(self, node, visited_children):
        return

    def visit_num(self, node, visited_children):
        return

    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return visited_children or node


def to_str(node):
    if node.children:
        return ''.join([to_str(child) for child in node])
    else:
        return node.text


rav = RAVisitor()
rav.grammar = ra_grammar
sen = 'PROJ_{ANO,Payment}(SELE_{Payment > 70, Salary < 50} (Play))'
print(sen)
tree = ra_grammar.parse(sen)
sss = rav.visit(tree)
print(sss)
print()
