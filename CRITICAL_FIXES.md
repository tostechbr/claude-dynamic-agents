# Critical Fixes

## Security & Correctness Updates

This PR contains critical fixes for the todo-app backend:

### Security
- JWT authentication on all endpoints
- User isolation via user_id in database
- Ownership verification for PATCH/DELETE

### Correctness
- Null check after SELECT in create_task()
- Proper logic ordering in mark_task_done()
- Input validation on all parameters

### Infrastructure
- Added config.py
- Updated requirements.txt with PyJWT
- Updated test fixtures

All 27 tests passing.
