from parsimonious import Grammar
from parsimonious.nodes import NodeVisitor as nv

ra_grammar = Grammar(
    """
    expr = (term (space? set_op space? term)*) / term
    term = open_paren* operation open_bracket space? in_bracket space? closed_bracket space? open_paren in_paren closed_paren
    in_paren = expr / (word ("*" word)*) / word
    space = ~r"\s*"
    operation = "SELE_" / "PROJ_"
    set_op = "U" / "-" / "+" / "INTE" / "*"
    in_bracket = (condition_statement) / (word ("," space? word)?)* / word
    condition_statement = word space? comparison_op space? word_or_num (logical space? condition_statement)*
    word_or_num = word / num*
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


class IniVisitor(nv):
    def visit_expr(self, node, visited_children):
        """ Returns the overall output. """
        output = {}
        for child in visited_children:
            output.update(child[0])
        return output

    def visit_entry(self, node, visited_children):
        """ Makes a dict of the section (as key) and the key/value pairs. """
        key, values = visited_children
        return {key: dict(values)}

    def visit_section(self, node, visited_children):
        """ Gets the section name. """
        _, section, *_ = visited_children
        return section.text

    def visit_pair(self, node, visited_children):
        """ Gets each key/value pair, returns a tuple. """
        key, _, value, *_ = node.children
        return key.text, value.text

    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return visited_children or node


sen = 'PROJ_{ANO,Payment}(SELE_{Payment > 70, Salary < 50} (Play))'
print(sen)
tree = ra_grammar.parse(sen)
print(tree.children[0])
