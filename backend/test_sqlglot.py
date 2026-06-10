import sqlglot
from sqlglot import exp

sql = "SELECT restaurant_name AS name, count(votes) FROM t_dataset GROUP BY restaurant_name;"
parsed = sqlglot.parse_one(sql, read="postgres")

print("Columns found:")
for c in parsed.find_all(exp.Column):
    print("Column name:", c.name, "| Full representation:", repr(c))
