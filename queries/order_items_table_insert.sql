insert into order_items (id, product_id, order_id, sales, quantity, discount, profit, shipping_cost, created_at) 
(select row_id,
        product_id,
        order_id,
        sales,
        quantity,
        discount,
        profit,
        shipping_cost,
        created_at
from order_items_tmp)
on duplicate key update order_items.id = order_items.id 
