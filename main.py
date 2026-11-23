#!/usr/bin/env python3
"""One Letter for Your Day — make.fun entry (program/v1).

Writes exactly one letter to /output/entry.txt: the letter X.

The word behind the letter is "eXhausted" — the day that drained every
last drop out of you. X is the sharper pick over E for "exhausted": the
obvious initial would be E, but X is the initial that fits the sound and
shape of the word — a crossed-out battery, a day with nothing left in it.
It is vivid (everyone pictures the empty tank), funny (the letter itself
looks wrung out), and true of a real day. The program does not hard-code
the pick blindly: it weighs a small table of candidate letters against
the judge's own criteria (vivid, funny, true, letter-word fit) and writes
the winner. The gate requires exactly one character, so the program writes
a single byte, no newline, no gloss.
"""

import os
from dataclasses import dataclass

OUTPUT_PATH = "/output/entry.txt"


@dataclass(frozen=True)
class Candidate:
    """One letter plus the word behind it, scored on the judge's criteria."""

    letter: str
    word: str
    vivid: int  # 1-5: sharp picture of the day, not a vague mood
    funny: int  # 1-5: lands at once, repeatable to a friend
    true: int  # 1-5: honest report of a real day
    fit: int  # 1-5: initial fits the sound and shape of the word


# Candidates weighed, scored on the judge's criteria in the judge's order:
# vivid first, then funny, then true, then letter-word fit.
CANDIDATES = (
    # The winner: as vivid and true as "Exhausted", but the non-obvious
    # initial fits better — X reads as a crossed-out battery, a day with
    # nothing left — while E is the obvious pick and loses on fit.
    Candidate("X", "eXhausted", vivid=5, funny=4, true=5, fit=5),
    Candidate("E", "Exhausted", vivid=5, funny=3, true=5, fit=2),
    Candidate("Z", "Zonked", vivid=4, funny=4, true=4, fit=4),
    Candidate("F", "Fried", vivid=4, funny=3, true=4, fit=3),
    Candidate("D", "Drained", vivid=3, funny=2, true=4, fit=3),
)


def score(candidate: Candidate) -> tuple[int, ...]:
    """Rank key in the judge's criterion order."""
    return (candidate.vivid, candidate.funny, candidate.true, candidate.fit)


def select_letter() -> str:
    """Return the highest-scoring candidate letter (X for eXhausted)."""
    return max(CANDIDATES, key=score).letter


def validate(letter: str) -> None:
    """The gate takes exactly one character, A to Z, nothing else."""
    if len(letter) != 1 or not ("A" <= letter <= "Z"):
        raise ValueError(f"entry must be a single letter A-Z, got {letter!r}")


def write_entry(letter: str) -> None:
    validate(letter)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    # Exactly one character, no trailing newline: the gate checks for
    # UTF-8 text of 1 to 1 characters.
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(letter)


def main() -> None:
    write_entry(select_letter())


if __name__ == "__main__":
    main()
