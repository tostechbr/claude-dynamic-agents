---
name: security-patterns
description: "Use when an agent writes, reviews, or audits code that handles authentication, authorization, user input, or sensitive data"
---

# Security Patterns

## Authentication

### JWT (recommended for stateless APIs)

```python
# Token structure
{
  "sub": "user_id",
  "exp": timestamp,   # short-lived: 15 min
  "iat": timestamp,
  "type": "access"    # distinguish from refresh
}

# Refresh token: long-lived (7-30 days), stored as HTTP-only cookie
# Access token: short-lived, returned in response body
```

Rules:
- Sign with `HS256` (symmetric) or `RS256` (asymmetric for multi-service)
- Never put sensitive data in JWT payload — it's base64, not encrypted
- Rotate refresh tokens on each use (rotation + reuse detection)
- Store refresh tokens in DB to enable revocation

### Password hashing

```python
# Use bcrypt or argon2 — NEVER md5/sha1/sha256 for passwords
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
```

---

## Input Validation

Always validate at system boundaries (API endpoints, file uploads, webhooks):

```python
# Use Pydantic for schema enforcement
class UserCreate(BaseModel):
    email: EmailStr           # validates format
    password: str = Field(min_length=8, max_length=128)
    username: str = Field(regex=r'^[a-zA-Z0-9_]+$')  # no special chars
```

Rules:
- Fail fast with clear error messages
- Never trust client-provided IDs for authorization checks
- Validate file uploads: type, size, extension

---

## SQL Injection Prevention

```python
# ALWAYS use parameterized queries
# WRONG
query = f"SELECT * FROM users WHERE email = '{email}'"

# CORRECT (SQLAlchemy)
result = await db.execute(select(User).where(User.email == email))
```

---

## Authorization

```python
# Check ownership before returning data
async def get_document(doc_id: UUID, current_user: User, db: AsyncSession):
    doc = await db.get(Document, doc_id)
    if doc.owner_id != current_user.id:
        raise HTTPException(status_code=403)  # not 404 — 404 leaks existence
    return doc
```

Rules:
- Return 403 (not 404) when user lacks permission to a known resource
- Return 404 when resource doesn't exist OR user shouldn't know it exists
- Enforce authorization at every layer (endpoint + service + DB)

---

## Rate Limiting

Apply on all public endpoints, stricter on auth endpoints:

```python
# Auth endpoints: 5 req/min per IP
# Public API: 100 req/min per token
# Expensive ops (file upload, search): 10 req/min
```

---

## Secret Management

- NEVER hardcode API keys, tokens, or passwords in source code
- Read from environment variables at startup
- Fail loud if required secrets are missing:

```python
SECRET_KEY = os.environ["SECRET_KEY"]  # raises KeyError if missing — good
```

---

## Error Messages

```python
# WRONG — leaks implementation details
raise HTTPException(detail=f"User {email} not found in table users")

# CORRECT — generic, safe
raise HTTPException(status_code=401, detail="Invalid credentials")
```

---

## Security Review Checklist

Before marking code complete:
- [ ] No hardcoded secrets
- [ ] All user inputs validated with schema
- [ ] SQL uses parameterized queries
- [ ] Authorization checks on every protected endpoint
- [ ] Rate limiting applied
- [ ] Error messages don't leak internal state
- [ ] Passwords hashed with bcrypt/argon2
- [ ] JWT tokens expire and are properly validated
