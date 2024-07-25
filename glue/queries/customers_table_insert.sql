insert into customers (id, name, created_at) 
(select customer_id,
        customer_name,
        created_at
from customers_tmp)
on duplicate key update customers.id = customers.id