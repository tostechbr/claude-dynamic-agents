---
name: postgres-patterns
description: "Use when designing schemas, writing migrations, optimizing queries, or reviewing PostgreSQL database work"
---

# PostgreSQL Patterns

## Schema Design Principles

```sql
-- Always use UUIDs for public-facing IDs
-- Always include created_at / updated_at
-- Always define NOT NULL unless nullable is intentional

CREATE TABLE users (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email       TEXT NOT NULL UNIQUE,
  password    TEXT NOT NULL,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

## Indexing Strategy

```sql
-- Index foreign keys (always)
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Index columns used in WHERE, ORDER BY, GROUP BY
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);

-- Partial index for common filtered queries
CREATE INDEX idx_users_active ON users(email) WHERE deleted_at IS NULL;

-- Composite index: order matters — most selective column first
CREATE INDEX idx_posts_user_status ON posts(user_id, status);
```

## Soft Delete Pattern

```sql
ALTER TABLE posts ADD COLUMN deleted_at TIMESTAMPTZ;

-- View that hides deleted records
CREATE VIEW active_posts AS
  SELECT * FROM posts WHERE deleted_at IS NULL;

-- Query with soft delete filter
SELECT * FROM posts WHERE deleted_at IS NULL AND user_id = $1;
```

## Migrations (with timestamps)

```sql
-- migrations/001_create_users.sql
-- Always: reversible, idempotent, non-destructive first

-- UP
CREATE TABLE IF NOT EXISTS users (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email      TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- DOWN
DROP TABLE IF EXISTS users;
```

## Common Query Patterns

```sql
-- Pagination (keyset — better than OFFSET for large tables)
SELECT * FROM posts
WHERE created_at < $1  -- cursor
ORDER BY created_at DESC
LIMIT 20;

-- Upsert
INSERT INTO user_settings (user_id, key, value)
VALUES ($1, $2, $3)
ON CONFLICT (user_id, key)
DO UPDATE SET value = EXCLUDED.value, updated_at = NOW();

-- Aggregation with filter
SELECT
  DATE_TRUNC('day', created_at) AS day,
  COUNT(*) AS total
FROM events
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY 1
ORDER BY 1;
```

## JSON/JSONB

```sql
-- Use JSONB for structured metadata (indexed, queryable)
ALTER TABLE products ADD COLUMN metadata JSONB;

-- Query inside JSONB
SELECT * FROM products WHERE metadata->>'category' = 'electronics';

-- Index a JSONB field
CREATE INDEX idx_products_category ON products((metadata->>'category'));
```

## Key Principles

- Use `UUID` as primary key — never expose sequential integers to clients
- Always define `NOT NULL` unless a column is intentionally nullable
- Index every foreign key column
- Use `TIMESTAMPTZ` (not `TIMESTAMP`) — always store timezone-aware timestamps
- Use keyset pagination over `OFFSET` for tables larger than 10k rows
- Avoid `SELECT *` in application queries — list columns explicitly
- Run `EXPLAIN ANALYZE` before deploying any new query
