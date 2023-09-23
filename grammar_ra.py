from parsimonious import Grammar

ra_grammar = Grammar(
    """
    expr = (term set_op term) / term
    term = operation open_bracket in_bracket comma? in_bracket? closed_bracket space? open_paren term? word? set_op? word? closed_paren
    space = ~r"[\s]*"
    operation = "SELE_" / "PROJ_"
    set_op = "U" / "-" / "+" / "INTE"
    in_bracket = condition_statement / word
    condition_statement = word space comparison_op space word_or_num
    comma = ~r"[,]"
    word_or_num = word / num
    num = ~r"[\d]+"
    word = ~r"[\w]+"
    open_bracket = "{"
    closed_bracket = "}"
    open_paren = "("
    closed_paren = ")"
    comparison_op = "<=" / ">=" / "!=" / "<" / ">" / "="
    """
)

print(ra_grammar.parse(
    'PROJ_{ANO,Payment}(SELE_{Payment > 70} (Play))'))
