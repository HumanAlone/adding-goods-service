-- 2.1
SELECT 
    c.name AS client_name,
    SUM(oi.quantity * p.price) AS total_sum
FROM clients c
JOIN orders o ON c.id = o.client_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
GROUP BY c.id
ORDER BY total_sum DESC;

-- 2.2
SELECT 
    cat_parent.name AS category_name,
    COUNT(cat_child.id) AS first_level_children_count
FROM categories cat_parent
LEFT JOIN categories cat_child ON cat_parent.id = cat_child.parent_id
WHERE cat_parent.parent_id IS NULL
GROUP BY cat_parent.id
ORDER BY cat_parent.name;

-- 2.3.1
CREATE VIEW IF NOT EXISTS top_5_products_last_month AS
WITH RECURSIVE category_path AS (
    SELECT id, name, parent_id, id AS root_id, name AS root_name
    FROM categories
    WHERE parent_id IS NULL
    
    UNION ALL
    
    SELECT c.id, c.name, c.parent_id, cp.root_id, cp.root_name
    FROM categories c
    JOIN category_path cp ON c.parent_id = cp.id
)
SELECT 
    p.name AS product_name,
    cp.root_name AS top_level_category,
    SUM(oi.quantity) AS total_sold_units
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
LEFT JOIN category_path cp ON p.category_id = cp.id
WHERE o.created_at >= date('now', '-1 month')
GROUP BY p.id, cp.root_id
ORDER BY total_sold_units DESC
LIMIT 5;

-- 2.3.2
/**

Рекурсивный CTE выполняется для всех категорий каждый раз, при большом количестве вложенных категорий - это затратно

Варианты решения:

- Добавить root_category_id в таблицу products
- Создать недостающие индексы, например, created_at для таблицы orders
- Партиционировать orders по месяцам
- Вынос аналитики в отдельную БД, например, ClickHouse
- Кэширование результатов запроса в Redis

**/
