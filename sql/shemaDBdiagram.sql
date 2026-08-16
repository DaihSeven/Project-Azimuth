// DIAGRAMA ER LH NAUTICAL (24 TABELAS COM Foreign Keys)


Table addresses {
  id bigint [pk]
  customer_id bigint
  address_type varchar
  postal_code varchar
  street varchar
  number bigint
  complement varchar
  district varchar
  city varchar
  state varchar
  country varchar
  is_primary boolean
}

Table attributes {
  id bigint [pk]
  name varchar
  data_type varchar
}

Table brands {
  id bigint [pk]
  name varchar
  country varchar
  is_active boolean
  created_at timestamp
  updated_at timestamp
}

Table categories {
  id bigint [pk]
  name varchar
  slug varchar
  parent_category_id bigint
  is_active boolean
  created_at timestamp
  updated_at timestamp
}

Table customers {
  id bigint [pk]
  person_type varchar
  legal_name varchar
  trade_name varchar
  tax_id bigint
  state_registration varchar
  email varchar
  phone varchar
  is_active boolean
  created_at timestamp
  updated_at timestamp
}

Table employees {
  id bigint [pk]
  full_name varchar
  cpf bigint
  email varchar
  role varchar
  primary_location_id bigint
  hire_date date
  termination_date date
  is_active boolean
  created_at timestamp
  updated_at timestamp
}

Table fiscal_invoices {
  id bigint [pk]
  order_id bigint
  nfe_number varchar
  nfe_access_key numeric
  series bigint
  issued_at timestamp
  status varchar
  total_amount numeric
  xml_storage_uri varchar
  created_at timestamp
  updated_at timestamp
}

Table goods_receipt_items {
  id bigint [pk]
  goods_receipt_id bigint
  purchase_order_item_id bigint
  quantity_received numeric
}

Table goods_receipts {
  id bigint [pk]
  purchase_order_id bigint
  received_by_employee_id bigint
  received_at timestamp
  notes varchar
  created_at timestamp
}

Table locations {
  id bigint [pk]
  name varchar
  location_type varchar
  postal_code varchar
  street varchar
  number bigint
  complement varchar
  district varchar
  city varchar
  state varchar
  country varchar
  is_active boolean
  created_at timestamp
  updated_at timestamp
}

Table order_items {
  id bigint [pk]
  order_id bigint
  product_variant_id bigint
  quantity bigint
  unit_price numeric
  icms_rate numeric
  ipi_rate numeric
  line_total numeric
}

Table orders {
  id bigint [pk]
  order_number varchar
  channel varchar
  customer_id bigint
  salesperson_id bigint
  location_id bigint
  status varchar
  subtotal numeric
  discount_amount numeric
  total numeric
  placed_at timestamp
  created_at timestamp
  updated_at timestamp
}

Table payments {
  id bigint [pk]
  order_id bigint
  method varchar
  installments bigint
  amount numeric
  status varchar
  paid_at timestamp
  created_at timestamp
  updated_at timestamp
}

Table product_suppliers {
  product_variant_id bigint [pk]
  supplier_id bigint [pk]
  supplier_sku varchar
  last_quoted_cost numeric
  lead_time_days bigint
  is_preferred boolean
  created_at timestamp
  updated_at timestamp
}

Table product_variants {
  id bigint [pk]
  product_id bigint
  sku varchar
  barcode_ean bigint
  sale_price numeric
  cost_price numeric
  weight_kg numeric
  icms_rate numeric
  ipi_rate numeric
  is_active boolean
  created_at timestamp
  updated_at timestamp
}

Table products {
  id bigint [pk]
  name varchar
  description varchar
  brand_id bigint
  category_id bigint
  ncm_code bigint
  unit_of_measure varchar
  is_active boolean
  created_at timestamp
  updated_at timestamp
}

Table purchase_order_items {
  id bigint [pk]
  purchase_order_id bigint
  product_variant_id bigint
  quantity_ordered bigint
  unit_cost numeric
  line_total numeric
}

Table purchase_orders {
  id bigint [pk]
  po_number varchar
  supplier_id bigint
  buyer_id bigint
  destination_location_id bigint
  status varchar
  currency varchar
  subtotal numeric
  total numeric
  placed_at timestamp
  expected_delivery_at date
  created_at timestamp
  updated_at timestamp
}

Table return_items {
  id bigint [pk]
  return_id bigint
  order_item_id bigint
  quantity numeric
  action varchar
  exchange_variant_id bigint
  unit_refund_amount numeric
}

Table returns {
  id bigint [pk]
  return_number varchar
  order_id bigint
  customer_id bigint
  received_at_location_id bigint
  status varchar
  reason varchar
  total_refund_amount numeric
  created_at timestamp
  updated_at timestamp
}

Table stock_levels {
  product_variant_id bigint [pk]
  location_id bigint [pk]
  quantity_on_hand numeric
  reorder_point varchar
  updated_at timestamp
}

Table stock_movements {
  id bigint [pk]
  product_variant_id bigint
  location_id bigint
  movement_type varchar
  quantity numeric
  reference_table varchar
  reference_id bigint
  employee_id bigint
  notes varchar
  occurred_at timestamp
  created_at timestamp
}

Table suppliers {
  id bigint [pk]
  legal_name varchar
  trade_name varchar
  country varchar
  tax_id varchar
  tax_id_type varchar
  email varchar
  phone bigint
  contact_name varchar
  is_active boolean
  created_at timestamp
  updated_at timestamp
}

Table variant_attribute_values {
  product_variant_id bigint [pk]
  attribute_id bigint [pk]
  value varchar
}

// FOREIGN KEYS

// Clientes e Endereços
Ref: addresses.customer_id > customers.id

// Produtos, Marcas, Atributos e Categorias
Ref: categories.parent_category_id > categories.id
Ref: products.brand_id > brands.id
Ref: products.category_id > categories.id
Ref: product_variants.product_id > products.id
Ref: variant_attribute_values.product_variant_id > product_variants.id
Ref: variant_attribute_values.attribute_id > attributes.id

// Fornecedores e Compras (Procurement)
Ref: product_suppliers.product_variant_id > product_variants.id
Ref: product_suppliers.supplier_id > suppliers.id
Ref: purchase_orders.supplier_id > suppliers.id
Ref: purchase_orders.buyer_id > employees.id
Ref: purchase_orders.destination_location_id > locations.id
Ref: purchase_order_items.purchase_order_id > purchase_orders.id
Ref: purchase_order_items.product_variant_id > product_variants.id
Ref: goods_receipts.purchase_order_id > purchase_orders.id
Ref: goods_receipts.received_by_employee_id > employees.id
Ref: goods_receipt_items.goods_receipt_id > goods_receipts.id
Ref: goods_receipt_items.purchase_order_item_id > purchase_order_items.id

// Vendas, Pedidos e Pagamentos
Ref: employees.primary_location_id > locations.id
Ref: orders.customer_id > customers.id
Ref: orders.salesperson_id > employees.id
Ref: orders.location_id > locations.id
Ref: order_items.order_id > orders.id
Ref: order_items.product_variant_id > product_variants.id
Ref: payments.order_id > orders.id
Ref: fiscal_invoices.order_id > orders.id

// Devoluções
Ref: returns.order_id > orders.id
Ref: returns.customer_id > customers.id
Ref: returns.received_at_location_id > locations.id
Ref: return_items.return_id > returns.id
Ref: return_items.order_item_id > order_items.id
Ref: return_items.exchange_variant_id > product_variants.id

// Estoque e Logística
Ref: stock_levels.product_variant_id > product_variants.id
Ref: stock_levels.location_id > locations.id
Ref: stock_movements.product_variant_id > product_variants.id
Ref: stock_movements.location_id > locations.id
Ref: stock_movements.employee_id > employees.id