"""
Custom Lookup
"""

from django.db.models import Lookup
from django.db.models.fields import DateField, DateTimeField


@DateField.register_lookup
@DateTimeField.register_lookup
class DateEqLookup(Lookup):
    lookup_name = 'date_c_eq'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        params = lhs_params + rhs_params
        return 'DATE(%s) = DATE(%s)' % (lhs, rhs), params


@DateField.register_lookup
@DateTimeField.register_lookup
class DateLtLookup(Lookup):
    lookup_name = 'date_c_lt'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        params = lhs_params + rhs_params
        return 'DATE(%s) < DATE(%s)' % (lhs, rhs), params


@DateField.register_lookup
@DateTimeField.register_lookup
class DateGtLookup(Lookup):
    lookup_name = 'date_c_gt'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        params = lhs_params + rhs_params
        return 'DATE(%s) > DATE(%s)' % (lhs, rhs), params


@DateField.register_lookup
@DateTimeField.register_lookup
class DateLtEqLookup(Lookup):
    lookup_name = 'date_c_lte'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        params = lhs_params + rhs_params
        return 'DATE(%s) <= DATE(%s)' % (lhs, rhs), params


@DateField.register_lookup
@DateTimeField.register_lookup
class DateGtEqLookup(Lookup):
    lookup_name = 'date_c_gte'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        params = lhs_params + rhs_params
        return 'DATE(%s) >= DATE(%s)' % (lhs, rhs), params


@DateField.register_lookup
@DateTimeField.register_lookup
class DateNoEqLookup(Lookup):
    lookup_name = 'date_c_noeq'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        params = lhs_params + rhs_params
        return 'DATE(%s) <> DATE(%s)' % (lhs, rhs), params
