from django.db import models


class SQLSumCase(models.sql.aggregates.Aggregate):
    is_ordinal = True
    sql_function = 'SUM'
    sql_template = "%(function)s(CASE WHEN %(when)s THEN %(field)s ELSE 0 END)"

    def __init__(self, col, **extra):
        if isinstance(extra['when'], basestring):
            extra['when'] = "%s" % extra['when']

        if extra['when'] is None:
            extra['when'] = True

        super(SQLSumCase, self).__init__(col, **extra)


class SumCase(models.Aggregate):
    name = 'SUM'

    def add_to_query(self, query, alias, col, source, is_summary):
        aggregate = SQLSumCase(col, source=source, is_summary=is_summary, **self.extra)
        query.aggregates[alias] = aggregate


class SQLCountCase(models.sql.aggregates.Aggregate):
    is_ordinal = True
    sql_function = 'SUM'
    sql_template = "%(function)s(CASE WHEN %(when)s THEN 1 ELSE 0 END)"

    def __init__(self, col, **extra):
        if isinstance(extra['when'], basestring):
            extra['when'] = "%s" % extra['when']

        if extra['when'] is None:
            extra['when'] = True

        super(SQLCountCase, self).__init__(col, **extra)


class CountWhen(models.Aggregate):
    name = 'COUNT'

    def add_to_query(self, query, alias, col, source, is_summary):
        aggregate = SQLCountCase(col, source=source, is_summary=is_summary, **self.extra)
        query.aggregates[alias] = aggregate