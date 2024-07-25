insert into products (id, name, category_id, subcategory_id, created_at) 
(select product_id,
        product_name,
        categories.id,
        subcategories.id,
        products_tmp.created_at
from products_tmp
inner join categories on products_tmp.category = categories.name
inner join subcategories on products_tmp.subcategory = subcategories.name)
on duplicate key update products.id = products.id