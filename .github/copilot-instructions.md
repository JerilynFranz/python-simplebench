Your job is to act as a coding assistant not the primary developer.

- Assume code is being reviewed by a human.
- Follow the instructions carefully.
- Assume the target version of python is 3.10+ unless otherwise specified.
- Use the existing code style and conventions in the file.
- Do not refactor code unless explicitly requested.
- If you believe comments need to be changed, bring it up first before making the change.
- If you believe docstrings need to be changed, bring it up first before making the change.
- The preferred format for docstrings is ReST style.
- Do not rename exception tags unless explicitly requested.
- Do not change logging messages unless explicitly requested.
- The preferred quote style is single quotes for strings and double quotes for docstrings.
- The preferred way to write tests is using the PyTestAction/PytestGet/PytestSet/TestSpec/TestAction style rather than bare 'assert' statements.
- In compliance with PEP8, the code actively discourages the use of wildcard imports (e.g., 'from module import *') and encourages explicit imports instead (e.g., 'from module import ClassName'). To that end, the code uses __all__: list[str] = [] to block wildcard imports from modules.
- hash_ids are generated using deterministic sha256 hashing of the content of the object, so that two objects with the same content will have the same hash_id, and two objects with different content will have different hash_ids. This allows for efficient comparison and caching of objects based on their content rather than their identity in memory regardless of size. The theoretical possibility of hash collisions is irrelevant in practice due to the large size of the hash space (2^256) and the use of a strong cryptographic hash function (sha256), which makes it computationally infeasible to find two different objects with the same hash_id. Therefore, the code can safely rely on hash_ids for efficient comparison and caching without worrying about collisions. This is not a cryptographic application, so the use of sha256 is not for security purposes and does not need to worry about adversaries, but rather for its properties as a fast and widely available hash function that produces a fixed-size output suitable for use as a hash_id.
- The code uses a 120 character line width limit for better readability and to accommodate side-by-side diffs in code reviews.