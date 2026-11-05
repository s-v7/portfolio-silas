from __future__ import annotations

from ai.core.exceptions import ConfigurationError

START = "<!-- ai-generated:start -->"
END = "<!-- ai-generated:end -->"
ANCHOR = '<br clear="right"/>\n'


def merge_block(cur: str, gen: str) -> str:
    """Put generated text between markers: replace the old block or insert a new one."""
    body = gen.strip()
    if not body:
        raise ConfigurationError("The generated text is empty.")

    if START in body or END in body:
        raise ConfigurationError("The generated text contains the block markers.")

    block = f"{START}\n{body}\n{END}"
    num_start, num_end = cur.count(START), cur.count(END)

    if (num_start, num_end) == (1, 1):
        if cur.index(START) > cur.index(END):
            raise ConfigurationError("The block markers are out of order.")

        head, rest = cur.split(START, 1)
        tail = rest.split(END, 1)[1]

        return head + block + tail

    if num_start or num_end:
        raise ConfigurationError("The block markers are unbalanced.")

    if cur.count(ANCHOR) != 1:
        raise ConfigurationError("The insertion anchor was not found exactly once.")

    return cur.replace(ANCHOR, ANCHOR + "\n" + block + "\n")
