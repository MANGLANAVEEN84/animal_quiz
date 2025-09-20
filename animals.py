import random
from typing import List, Tuple

# Basic A-Z animal list. You can expand or localize as needed.
ANIMALS: List[str] = [
    "Alligator", "Ant", "Ape", "Armadillo",
    "Bear", "Bee", "Buffalo", "Butterfly",
    "Cat", "Camel", "Cheetah", "Chicken", "Cow",
    "Deer", "Dog", "Dolphin", "Duck",
    "Eagle", "Elephant",
    "Fox", "Frog",
    "Giraffe", "Goat", "Goose",
    "Horse", "Hippopotamus",
    "Iguana",
    "Jaguar",
    "Kangaroo", "Koala",
    "Lion", "Leopard", "Llama",
    "Monkey", "Moose",
    "Newt",
    "Octopus", "Otter", "Owl",
    "Penguin", "Panda", "Parrot", "Pig",
    "Quail",
    "Rabbit", "Raccoon", "Rat", "Rhinoceros",
    "Sheep", "Shark", "Snake", "Squirrel",
    "Tiger", "Turkey", "Turtle",
    "Urial",
    "Vulture",
    "Wolf", "Walrus", "Whale",
    "Xerus",  # African ground squirrel
    "Yak",
    "Zebra",
]


def get_random_question() -> Tuple[str, List[str]]:
    """
    Returns a tuple of (target_animal, options_list).
    options_list has exactly 3 unique animal names including the correct one, shuffled.
    """
    correct = random.choice(ANIMALS)
    distractors = set()
    while len(distractors) < 2:
        cand = random.choice(ANIMALS)
        if cand != correct:
            distractors.add(cand)
    options = [correct] + list(distractors)
    random.shuffle(options)
    return correct, options


def normalize_name(name: str) -> str:
    """Normalize animal name for filenames/keys."""
    return name.strip().lower().replace(" ", "_")


# Compatibility helper used by some environments/tests
# Returns the list of animals

def get_animal_list() -> List[str]:
    return list(ANIMALS)
