
from src.parser.select_statement import SelectStatement
from src.parser.evaql.evaql_parser import evaql_parser


##################################################################
# TABLE SOURCES
##################################################################

def visitTableSources(self, ctx: evaql_parser.TableSourcesContext):
    table_list = []
    table_sources_count = len(ctx.tableSource())
    for table_sources_index in range(table_sources_count):
        table = self.visit(ctx.tableSource(table_sources_index))
        table_list.append(table)

    return table_list


def visitQuerySpecification(
        self, ctx: evaql_parser.QuerySpecificationContext):
    target_list = None
    from_clause = None
    where_clause = None
    # first child will be a SELECT terminal token
    for child in ctx.children[1:]:
        try:
            rule_idx = child.getRuleIndex()
            if rule_idx == evaql_parser.RULE_selectElements:
                target_list = self.visit(child)

            elif rule_idx == evaql_parser.RULE_fromClause:
                clause = self.visit(child)
                from_clause = clause.get('from', None)
                where_clause = clause.get('where', None)

        except BaseException:
            # stop parsing something bad happened
            return None

    # we don't support multiple table sources
    if from_clause is not None:
        from_clause = from_clause[0]

    select_stmt = SelectStatement(target_list, from_clause, where_clause)

    return select_stmt


def visitSelectElements(self, ctx: evaql_parser.SelectElementsContext):
    select_list = []
    select_elements_count = len(ctx.selectElement())
    for select_element_index in range(select_elements_count):
        element = self.visit(ctx.selectElement(select_element_index))
        select_list.append(element)

    return select_list


def visitFromClause(self, ctx: evaql_parser.FromClauseContext):
    from_table = None
    where_clause = None

    if ctx.tableSources():
        from_table = self.visit(ctx.tableSources())
    if ctx.whereExpr is not None:
        where_clause = self.visit(ctx.whereExpr)

    return {"from": from_table, "where": where_clause}