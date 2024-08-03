insert into orders (id, order_date, ship_date, shipping_id, customer_id, priority_id, created_at) 
(select order_id,
        CONCAT(RIGHT(order_date, 4), '-', SUBSTRING(order_date, 4, 2), '-', LEFT(order_date, 2)),
        CONCAT(RIGHT(ship_date, 4), '-', SUBSTRING(ship_date, 4, 2), '-', LEFT(ship_date, 2)),
        shipping.id,
        customer_id,
        priorities.id,
        orders_tmp.created_at
from orders_tmp
inner join shipping on orders_tmp.ship_mode = shipping.name
inner join priorities on orders_tmp.order_priority = priorities.name)
on duplicate key update orders.id = orders.id 
