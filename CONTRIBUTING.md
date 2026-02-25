# Contributing

## Branch naming

- `feat/<short-topic>`
- `fix/<short-topic>`
- `chore/<short-topic>`

## Commit convention

Use Conventional Commits:

- `feat:` new capability
- `fix:` bug fix
- `refactor:` internal refactor without behavior change
- `test:` test updates
- `docs:` documentation
- `chore:` tooling/dependency changes

Examples:

```text
feat(memory): add semantic search fallback when qdrant is unavailable
fix(health): return dependency-level status for db/redis/qdrant
```

## Pull request checklist

- [ ] Pass `make lint`
- [ ] Pass `make test`
- [ ] Update README/docs when behavior changes
- [ ] Include tests for key path changes
