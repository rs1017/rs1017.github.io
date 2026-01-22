
# API Response Parser Skill

This skill helps you parse, transform, and validate API responses efficiently.

## When to Use

Use this skill when you need to:
- Extract specific fields from complex JSON/XML API responses
- Convert API responses between formats (JSON ↔ XML ↔ CSV)
- Validate response schemas and data types
- Transform nested structures into flat tables
- Handle pagination and extract data from multiple pages
- Debug API responses by pretty-printing or analyzing structure

## How to Use

Simply describe what you want to do with the API response:

```
Parse this API response and extract user names and emails
```

```
Convert this JSON response to CSV format
```

```
Validate if this response matches the expected schema
```

## Capabilities

### 1. Field Extraction
Extract specific fields from nested JSON/XML structures.

**Example:**
```json
{
  "data": {
    "users": [
      {"id": 1, "profile": {"name": "Alice", "email": "alice@example.com"}},
      {"id": 2, "profile": {"name": "Bob", "email": "bob@example.com"}}
    ]
  }
}
```

Request: "Extract all names and emails"

Output:
```
Alice, alice@example.com
Bob, bob@example.com
```

### 2. Format Conversion
Convert between JSON, XML, CSV, and YAML formats.

### 3. Schema Validation
Check if response matches expected structure and data types.

### 4. Data Transformation
- Flatten nested structures
- Rename fields
- Filter by conditions
- Aggregate values
- Sort and group data

### 5. Pagination Handling
Extract and combine data from paginated responses.

### 6. Error Analysis
Identify and explain API error responses.

## Examples

### Example 1: Extract Product Info
```
API Response:
{
  "products": [
    {"id": 101, "details": {"name": "Laptop", "price": 999}},
    {"id": 102, "details": {"name": "Mouse", "price": 29}}
  ]
}

Request: "Create a table with ID, name, and price"

Output:
| ID  | Name   | Price |
|-----|--------|-------|
| 101 | Laptop | $999  |
| 102 | Mouse  | $29   |
```

### Example 2: Convert to CSV
```
Request: "Convert this JSON response to CSV"

Output CSV:
id,name,price
101,Laptop,999
102,Mouse,29
```

### Example 3: Validate Schema
```
Request: "Check if response has required fields: id, name, price"

Output: ✓ All required fields present
```

## Tips

- Provide the full API response for accurate parsing
- Specify the exact fields you need
- Mention the desired output format (table, CSV, JSON, etc.)
- For large responses, specify filtering criteria
- Include sample expected output for complex transformations

## Related Skills

- `json-validator` - Validate JSON schemas
- `data-transformer` - Advanced data transformations
- `csv-converter` - CSV file operations
- `api-client` - Make API requests
