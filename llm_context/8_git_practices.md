# Git Practices for Gemini LLM

This document outlines the specific Git practices that the Gemini LLM should adhere to when interacting with the project's repository.

---

## 1. Granular Commits

*   **Commit Related Changes Only:** When performing tasks, group related file changes into a single commit. Avoid committing unrelated changes together.
*   **Avoid `git add .`:** Never use `git add .` to stage all changes. Instead, explicitly stage individual files or groups of related files using `git add <file1> <file2> ...` or `git add <directory>/`. This ensures that only intended changes are included in a commit.

---

## 2. Commit Message Guidelines

*   **Descriptive and Concise:** Commit messages should clearly and concisely describe the purpose of the changes.
*   **Conventional Commits (Recommended):** Follow the Conventional Commits specification (e.g., `feat:`, `fix:`, `docs:`, `refactor:`) for commit messages. This provides a structured format for commit history.
*   **Focus on "Why":** Emphasize *why* a change was made, rather than just *what* was changed.

---

## 3. Review and Confirmation

*   **Review Changes Before Committing:** Always review staged changes using `git diff --staged` before creating a commit.
*   **Propose Commit Message:** Always propose a draft commit message to the user for review and confirmation before committing.
