# Lessons Learned

This file tracks patterns, corrections, and lessons learned during development to prevent repeating mistakes.

## Initial Setup (2026-02-06)

### Repository Organization
- **Lesson:** Always verify file existence before attempting to move/rename operations
- **Context:** During initial repository reorganization, assumed papers/ directory existed based on exploration, but it wasn't present on disk
- **Solution:** Check with ls/git status before file operations, handle missing files gracefully

### Planning Approach
- **Lesson:** Comprehensive upfront planning prevents ambiguity during implementation
- **Context:** Created detailed plan covering directory structure, tech stack, database schema, API design, and implementation phases
- **Solution:** Always use plan mode for non-trivial tasks with 3+ steps or architectural decisions

---

## Future Lessons

Add new lessons here as the project progresses. Format:
- **Lesson:** Brief description of the pattern or mistake
- **Context:** What happened and why
- **Solution:** How to prevent or handle it in the future
