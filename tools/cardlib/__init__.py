"""Scene cards: the simple way to plan a film. See playbook/03-cards.md and recipes/CATALOG.md."""
from . import recipes_people, recipes_action, recipes_map, recipes_other, recipes_story  # noqa: F401  (registers the recipes)
from .core import RECIPES, CardError  # noqa: F401
from .compile import compile_project  # noqa: F401
