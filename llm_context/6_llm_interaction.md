# LLM Interaction Guide

This guide outlines best practices for interacting with the Gemini LLM to ensure effective collaboration.

## Context Management

*   **Context Window:** The LLM has a limited context window. Information at the beginning and end of the context is most prominent.
*   **Precise Context:** Use the CLI tools (`read_file`, `search_file_content`, etc.) to provide focused and relevant context.
*   **Iterative Prompts:** Break down large tasks into smaller, focused steps.
*   **`LLM_Context` Directory:** The files in this directory provide a high-level overview of the project.

## Context File Size

*   **Ideal Size:** 1-2 pages (500-1000 words).
*   **Maximum Size:** Avoid files larger than 10 pages (>5000 words).
*   **Focus:** Each file should cover a single, atomic concept.
