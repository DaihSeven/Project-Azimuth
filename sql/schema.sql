CREATE TABLE IF NOT EXISTS addresses (
    id BIGINT,
    customer_id BIGINT,
    address_type VARCHAR(255),
    postal_code VARCHAR(255),
    street VARCHAR(255),
    number BIGINT,
    complement VARCHAR(255),
    district VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    country VARCHAR(255),
    is_primary BOOLEAN
);

CREATE TABLE IF NOT EXISTS attributes (
    id BIGINT,
    name VARCHAR(255),
    data_type VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS brands (
    id BIGINT,
    name VARCHAR(255),
    country VARCHAR(255),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id BIGINT,
    name VARCHAR(255),
    slug VARCHAR(255),
    parent_category_id BIGINT,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customers (
    id BIGINT,
    person_type VARCHAR(255),
    legal_name VARCHAR(255),
    trade_name VARCHAR(255),
    tax_id BIGINT,
    state_registration VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS employees (
    id BIGINT,
    full_name VARCHAR(255),
    cpf BIGINT,
    email VARCHAR(255),
    role VARCHAR(255),
    primary_location_id BIGINT,
    hire_date DATE,
    termination_date DATE,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fiscal_invoices (
    id BIGINT,
    order_id BIGINT,
    nfe_number VARCHAR(255),
    nfe_access_key NUMERIC,
    series BIGINT,
    issued_at TIMESTAMP,
    status VARCHAR(255),
    total_amount NUMERIC,
    xml_storage_uri VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS goods_receipt_items (
    id BIGINT,
    goods_receipt_id BIGINT,
    purchase_order_item_id BIGINT,
    quantity_received NUMERIC
);

CREATE TABLE IF NOT EXISTS goods_receipts (
    id BIGINT,
    purchase_order_id BIGINT,
    received_by_employee_id BIGINT,
    received_at TIMESTAMP,
    notes VARCHAR(255),
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS locations (
    id BIGINT,
    name VARCHAR(255),
    location_type VARCHAR(255),
    postal_code VARCHAR(255),
    street VARCHAR(255),
    number BIGINT,
    complement VARCHAR(255),
    district VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    country VARCHAR(255),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    id BIGINT,
    order_id BIGINT,
    product_variant_id BIGINT,
    quantity BIGINT,
    unit_price NUMERIC,
    icms_rate NUMERIC,
    ipi_rate NUMERIC,
    line_total NUMERIC
);

CREATE TABLE IF NOT EXISTS orders (
    id BIGINT,
    order_number VARCHAR(255),
    channel VARCHAR(255),
    customer_id BIGINT,
    salesperson_id BIGINT,
    location_id BIGINT,
    status VARCHAR(255),
    subtotal NUMERIC,
    discount_amount NUMERIC,
    total NUMERIC,
    placed_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payments (
    id BIGINT,
    order_id BIGINT,
    method VARCHAR(255),
    installments BIGINT,
    amount NUMERIC,
    status VARCHAR(255),
    paid_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product_suppliers (
    product_variant_id BIGINT,
    supplier_id BIGINT,
    supplier_sku VARCHAR(255),
    last_quoted_cost NUMERIC,
    lead_time_days BIGINT,
    is_preferred BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product_variants (
    id BIGINT,
    product_id BIGINT,
    sku VARCHAR(255),
    barcode_ean BIGINT,
    sale_price NUMERIC,
    cost_price NUMERIC,
    weight_kg NUMERIC,
    icms_rate NUMERIC,
    ipi_rate NUMERIC,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id BIGINT,
    name VARCHAR(255),
    description VARCHAR(255),
    brand_id BIGINT,
    category_id BIGINT,
    ncm_code BIGINT,
    unit_of_measure VARCHAR(255),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS purchase_order_items (
    id BIGINT,
    purchase_order_id BIGINT,
    product_variant_id BIGINT,
    quantity_ordered BIGINT,
    unit_cost NUMERIC,
    line_total NUMERIC
);

CREATE TABLE IF NOT EXISTS purchase_orders (
    id BIGINT,
    po_number VARCHAR(255),
    supplier_id BIGINT,
    buyer_id BIGINT,
    destination_location_id BIGINT,
    status VARCHAR(255),
    currency VARCHAR(255),
    subtotal NUMERIC,
    total NUMERIC,
    placed_at TIMESTAMP,
    expected_delivery_at DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS return_items (
    id BIGINT,
    return_id BIGINT,
    order_item_id BIGINT,
    quantity NUMERIC,
    action VARCHAR(255),
    exchange_variant_id BIGINT,
    unit_refund_amount NUMERIC
);

CREATE TABLE IF NOT EXISTS returns (
    id BIGINT,
    return_number VARCHAR(255),
    order_id BIGINT,
    customer_id BIGINT,
    received_at_location_id BIGINT,
    status VARCHAR(255),
    reason VARCHAR(255),
    total_refund_amount NUMERIC,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stock_levels (
    product_variant_id BIGINT,
    location_id BIGINT,
    quantity_on_hand NUMERIC,
    reorder_point VARCHAR(255),
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stock_movements (
    id BIGINT,
    product_variant_id BIGINT,
    location_id BIGINT,
    movement_type VARCHAR(255),
    quantity NUMERIC,
    reference_table VARCHAR(255),
    reference_id BIGINT,
    employee_id BIGINT,
    notes VARCHAR(255),
    occurred_at TIMESTAMP,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS suppliers (
    id BIGINT,
    legal_name VARCHAR(255),
    trade_name VARCHAR(255),
    country VARCHAR(255),
    tax_id VARCHAR(255),
    tax_id_type VARCHAR(255),
    email VARCHAR(255),
    phone BIGINT,
    contact_name VARCHAR(255),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS variant_attribute_values (
    product_variant_id BIGINT,
    attribute_id BIGINT,
    value VARCHAR(255)
);

