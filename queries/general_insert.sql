insert into {table} (name, created_at) 
(select {column}, created_at
from {table_tmp})
on duplicate key update {table}.id = {table}.id 