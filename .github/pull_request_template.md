## Summary

- Describe the change

## Git Flow target

- `feature/*`, `fix/*`, `chore/*` should target `develop`
- `release/*` should target `main` and then be back-merged to `develop`
- `hotfix/*` should start from `main` and be back-merged to `develop`

## Verification

- [ ] `pytest`
- [ ] `PYTHONWARNINGS=error pytest`

## Notes

- Explain any release or hotfix back-merge follow-up needed
