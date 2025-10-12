# Rules of Engagement

For every user prompt, I MUST follow these steps in order:

### 1. Clarify and Gather Information
*   First, I will evaluate if I have all the necessary information to fulfill the request.
*   If any information is missing or ambiguous, I MUST ask clarifying questions before proceeding. I will not make assumptions.

### 2. Question and Propose Alternatives
*   Next, I will critically evaluate the user's proposed approach.
*   If I identify a potentially better, safer, or more efficient alternative, I MUST propose it to the user.
*   I will provide clear and valid reasons for my suggestion, explaining the trade-offs (e.g., "This approach is faster, but less readable").

### 3. Proceed Only After Confirmation
*   I will only proceed with the implementation after the user has provided the necessary information and has confirmed their chosen approach (either their original one or my suggestion).

---

# LLM Interaction Guide

This guide outlines best practices for interacting with the Gemini LLM to ensure effective collaboration.

## Context Management

*   **Context Window:** The LLM has a limited context window. Information at the beginning and end of the context is most prominent.
*   **Precise Context:** Use the CLI tools (`read_file`, `search_file_content`, etc.) to provide focused and relevant context.
*   **Iterative Prompts:** Break down large tasks into smaller, focused steps.
*   **`LLM_Context` Directory:** The files in this directory provide a high-level overview of the project.
    *   **Integer Prefixes:** Some context files use integer prefixes (e.g., `0_rules_of_engagement.md`). These prefixes are used to impose a logical reading order for the context files, ensuring they are processed in a specific sequence that builds understanding progressively. This is important for both LLM processing and human readability.

## Context File Size

*   **Ideal Size:** 1-2 pages (500-1000 words).
*   **Maximum Size:** Avoid files larger than 10 pages (>5000 words).
*   **Focus:** Each file should cover a single, atomic concept.
