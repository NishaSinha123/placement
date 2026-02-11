<!-- ---

# 🏪 Vending Machine API – Specification

## 🔧 Global Configuration

```yaml
MAX_SLOTS: integer (configured at app startup)
MAX_ITEMS_PER_SLOT: integer (optional enhancement)
SUPPORTED_DENOMINATIONS: [1, 2, 5, 10, 20, 50, 100]
CURRENCY: "INR"
```

---

# 📦 Data Models

## Slot

```json
{
  "id": "bigint (default)",
  "code": "string (e.g. A1, B2)",
  "capacity": 10,
  "current_item_count": 5,
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

---

## Item

```json
{
  "id": "bigint (default)",
  "name": "Coke",
  "price": 40,
  "slot_id": "bigint",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

---

# 1️⃣ Add Slot

### POST `/slots`

Creates a new slot.

### Request

```json
{
  "code": "A1",
  "capacity": 10
}
```

### Validation Rules

* Cannot exceed `MAX_SLOTS`
* `code` must be unique
* capacity > 0

### Response (201)

```json
{
  "id": "uuid",
  "code": "A1",
  "capacity": 10,
  "current_item_count": 0
}
```

### Errors

* `400` → Slot limit reached
* `409` → Slot code already exists

---

# 2️⃣ View All Slots

### GET `/slots`

### Response

```json
[
  {
    "id": "uuid",
    "code": "A1",
    "capacity": 10,
    "current_item_count": 5
  }
]
```

---

# 3️⃣ Remove Slot

### DELETE `/slots/{slot_id}`

### Rules

* Cannot delete if slot contains items (optional strict rule)

### Response

```json
{
  "message": "Slot removed successfully"
}
```

---

# 4️⃣ Add Item to Slot

### POST `/slots/{slot_id}/items`

Adds a new item type into the slot.

### Request

```json
{
  "name": "Coke",
  "price": 40,
  "quantity": 5
}
```

### Rules

* Slot must exist
* quantity > 0
* total items must not exceed slot capacity
* price > 0

### Response

```json
{
  "id": "uuid",
  "name": "Coke",
  "price": 40,
  "quantity": 5
}
```

---

# 5️⃣ Bulk Add Items to Slot

### POST `/slots/{slot_id}/items/bulk`

### Request

```json
{
  "items": [
    {
      "name": "Pepsi",
      "price": 35,
      "quantity": 5
    },
    {
      "name": "Sprite",
      "price": 30,
      "quantity": 3
    }
  ]
}
```

### Rules

* Total new quantity must not exceed slot capacity

### Response

```json
{
  "message": "Items added successfully",
  "added_count": 2
}
```

---

# 6️⃣ View Items of a Slot

### GET `/slots/{slot_id}/items`

### Response

```json
[
  {
    "id": "uuid",
    "name": "Coke",
    "price": 40,
    "quantity": 5
  }
]
```

---

# 7️⃣ View Single Item

### GET `/items/{item_id}`

### Response

```json
{
  "id": "uuid",
  "name": "Coke",
  "price": 40,
  "quantity": 5,
  "slot_id": "uuid"
}
```

---

# 8️⃣ Update Price for an Item

### PATCH `/items/{item_id}/price`

### Request

```json
{
  "price": 45
}
```

### Rules

* price > 0

### Response

```json
{
  "message": "Price updated successfully"
}
```

---

# 9️⃣ Remove Items from Slot (Partial Removal)

### DELETE `/slots/{slot_id}/items/{item_id}`

Removes quantity or entire item.

### Query Param (Optional)

```
?quantity=2
```

### Behavior

* If quantity provided → subtract
* If no quantity → delete item entirely

### Response

```json
{
  "message": "Item(s) removed successfully"
}
```

---

# 🔟 Bulk Remove Items / Empty Slot

### DELETE `/slots/{slot_id}/items`

### Optional Body

```json
{
  "item_ids": ["uuid1", "uuid2"]
}
```

### Behavior

* If body provided → remove specific items
* If no body → empty slot completely

### Response

```json
{
  "message": "Slot cleared successfully"
}
```

---

# 1️⃣1️⃣ Full View (Slots + Items)

### GET `/slots/full-view`

### Response

```json
[
  {
    "id": "uuid",
    "code": "A1",
    "capacity": 10,
    "items": [
      {
        "id": "uuid",
        "name": "Coke",
        "price": 40,
        "quantity": 5
      }
    ]
  }
]
```

---

# 1️⃣2️⃣ Purchase Item

This is where the fun logic lives.

### POST `/purchase`

### Request

```json
{
  "item_id": "uuid",
  "cash_inserted": 50
}
```

---

## Business Rules

* Item must exist
* quantity > 0
* cash_inserted >= price
* Change = cash_inserted - price
* Decrement quantity by 1
* Transaction must be atomic

---

## Response

```json
{
  "item": "Coke",
  "price": 40,
  "cash_inserted": 50,
  "change_returned": 10,
  "remaining_quantity": 4,
  "message": "Purchase successful"
}
```

---

## Error Cases

### 400 – Insufficient Cash

```json
{
  "error": "Insufficient cash",
  "required": 40,
  "inserted": 30
}
```

---

### 400 – Out of Stock

```json
{
  "error": "Item out of stock"
}
```

---

---

# Bonus 

Add:

### 🎯 GET `/purchase/change-breakdown`

Return denomination-wise change:

```json
{
  "change": 70,
  "denominations": {
    "50": 1,
    "20": 1
  }
}
```

Implement greedy algorithm for denomination breakdown.

--- -->

# 🏪 Vending Machine API – Specification

## 🔧 Global Configuration

```yaml
MAX_SLOTS: integer (configured at app startup)
MAX_ITEMS_PER_SLOT: integer (optional enhancement)
SUPPORTED_DENOMINATIONS: [1, 2, 5, 10, 20, 50, 100]
CURRENCY: "INR"
```

---

# 📦 Data Models

## Slot

```json
{
  "id": "bigint",
  "code": "string (e.g. A1, B2)",
  "capacity": 10,
  "current_item_count": 5,
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

---

## Item

```json
{
  "id": "bigint",
  "name": "Coke",
  "price": 40,
  "slot_id": "bigint",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

---

# 1️⃣ Add Slot

### POST `/slots`

### Request

```json
{
  "code": "A1",
  "capacity": 10
}
```

### Validation Rules

* Cannot exceed `MAX_SLOTS`
* `code` must be unique
* capacity > 0

### Response (201)

```json
{
  "id": 1,
  "code": "A1",
  "capacity": 10,
  "current_item_count": 0
}
```

### Errors

* 400 → Slot limit reached
* 409 → Slot code already exists

---

# 2️⃣ View All Slots

### GET `/slots`

```json
[
  {
    "id": 1,
    "code": "A1",
    "capacity": 10,
    "current_item_count": 5
  }
]
```

---

# 3️⃣ Remove Slot

### DELETE `/slots/{slot_id}`

```json
{
  "message": "Slot removed successfully"
}
```

---

# 4️⃣ Add Item to Slot

### POST `/slots/{slot_id}/items`

```json
{
  "name": "Coke",
  "price": 40,
  "quantity": 5
}
```

### Response

```json
{
  "id": 1,
  "name": "Coke",
  "price": 40,
  "quantity": 5
}
```

---

# 5️⃣ Bulk Add Items

### POST `/slots/{slot_id}/items/bulk`

```json
{
  "items": [
    {
      "name": "Pepsi",
      "price": 35,
      "quantity": 5
    },
    {
      "name": "Sprite",
      "price": 30,
      "quantity": 3
    }
  ]
}
```

```json
{
  "message": "Items added successfully",
  "added_count": 2
}
```

---

# 6️⃣ View Items of Slot

### GET `/slots/{slot_id}/items`

```json
[
  {
    "id": 1,
    "name": "Coke",
    "price": 40,
    "quantity": 5
  }
]
```

---

# 7️⃣ View Single Item

### GET `/items/{item_id}`

```json
{
  "id": 1,
  "name": "Coke",
  "price": 40,
  "quantity": 5,
  "slot_id": 1
}
```

---

# 8️⃣ Update Price

### PATCH `/items/{item_id}/price`

```json
{
  "price": 45
}
```

```json
{
  "message": "Price updated successfully"
}
```

---

# 9️⃣ Remove Items

### DELETE `/slots/{slot_id}/items/{item_id}`

```json
{
  "message": "Item(s) removed successfully"
}
```

---

# 🔟 Bulk Remove / Empty Slot

### DELETE `/slots/{slot_id}/items`

```json
{
  "item_ids": [1, 2]
}
```

```json
{
  "message": "Slot cleared successfully"
}
```

---

# 1️⃣1️⃣ Full View

### GET `/slots/full-view`

```json
[
  {
    "id": 1,
    "code": "A1",
    "capacity": 10,
    "items": [
      {
        "id": 1,
        "name": "Coke",
        "price": 40,
        "quantity": 5
      }
    ]
  }
]
```

---

# 1️⃣2️⃣ Purchase

### POST `/purchase`

```json
{
  "item_id": 1,
  "cash_inserted": 50
}
```

```json
{
  "item": "Coke",
  "price": 40,
  "cash_inserted": 50,
  "change_returned": 10,
  "remaining_quantity": 4,
  "message": "Purchase successful"
}
```

---

# Bonus

### GET `/purchase/change-breakdown`

```json
{
  "change": 70,
  "denominations": {
    "50": 1,
    "20": 1
  }
}
```
