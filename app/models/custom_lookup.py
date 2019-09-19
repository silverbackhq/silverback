# Copyright 2019 Silverbackhq
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Third Party Library
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


@DateField.register_lookup
@DateTimeField.register_lookup
class YearEqLookup(Lookup):
    lookup_name = 'year_c_eq'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        params = lhs_params + rhs_params
        return 'EXTRACT(YEAR FROM DATE(%s)) = EXTRACT(YEAR FROM DATE(%s))' % (lhs, rhs), params


@DateField.register_lookup
@DateTimeField.register_lookup
class MonthEqLookup(Lookup):
    lookup_name = 'month_c_eq'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        params = lhs_params + rhs_params
        return 'EXTRACT(MONTH FROM DATE(%s)) = EXTRACT(MONTH FROM DATE(%s))' % (lhs, rhs), params
