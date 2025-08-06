from enum import Enum
import math
from levels import xp_to_level, level_to_xp


ACTIONS = 4


class Material(Enum):
    OAK = "Oak"
    WILLOW = "Willow"
    MAPLE = "Maple"
    YEW = "Yew"
    MAGIC = "Magic"
    REDWOOD = "Redwood"


class Axe(Enum):
    BRONZE = "Bronze"
    IRON = "Iron"
    STEEL = "Steel"
    BLACK = "Black"
    MITHRIL = "Mithril"
    ADAMANT = "Adamant"
    RUNE = "Rune"
    DRAGON = "Dragon"


class Item(Enum):
    SHORTBOW = "Shortbow"
    LONGBOW = "Longbow"
    STAFF = "Staff"


class Action(Enum):
    ADD = "Add"
    BUILD = "Build"
    FLETCH = "Fletch"
    CUT = "Cut"


WC_CHANCE = {
    Material.OAK: {
        Axe.BRONZE: [32, 100],
        Axe.IRON: [48, 150],
        Axe.STEEL: [64, 200],
        Axe.BLACK: [72, 225],
        Axe.MITHRIL: [80, 250],
        Axe.ADAMANT: [96, 300],
        Axe.RUNE: [112, 350],
        Axe.DRAGON: [120, 375],
    },
    Material.WILLOW: {
        Axe.BRONZE: [16, 50],
        Axe.IRON: [24, 75],
        Axe.STEEL: [32, 100],
        Axe.BLACK: [36, 112],
        Axe.MITHRIL: [40, 125],
        Axe.ADAMANT: [48, 150],
        Axe.RUNE: [56, 175],
        Axe.DRAGON: [60, 187],
    },
    Material.MAPLE: {
        Axe.BRONZE: [8, 25],
        Axe.IRON: [12, 37],
        Axe.STEEL: [16, 50],
        Axe.BLACK: [18, 56],
        Axe.MITHRIL: [20, 62],
        Axe.ADAMANT: [24, 75],
        Axe.RUNE: [28, 87],
        Axe.DRAGON: [30, 93],
    },
    Material.YEW: {
        Axe.BRONZE: [4, 12],
        Axe.IRON: [6, 19],
        Axe.STEEL: [8, 25],
        Axe.BLACK: [9, 28],
        Axe.MITHRIL: [10, 31],
        Axe.ADAMANT: [12, 37],
        Axe.RUNE: [14, 44],
        Axe.DRAGON: [15, 47],
    },
    Material.MAGIC: {
        Axe.BRONZE: [2, 6],
        Axe.IRON: [3, 9],
        Axe.STEEL: [4, 12],
        Axe.BLACK: [5, 13],
        Axe.MITHRIL: [5, 15],
        Axe.ADAMANT: [6, 18],
        Axe.RUNE: [7, 21],
        Axe.DRAGON: [7, 22],
    },
    Material.REDWOOD: {
        Axe.BRONZE: [2, 6],
        Axe.IRON: [3, 9],
        Axe.STEEL: [4, 12],
        Axe.BLACK: [4, 14],
        Axe.MITHRIL: [5, 15],
        Axe.ADAMANT: [6, 18],
        Axe.RUNE: [7, 21],
        Axe.DRAGON: [7, 30],
    },
}

FLETCHING_STUFF = {
    Material.OAK: {
        "Items": {Item.SHORTBOW: 16.5, Item.LONGBOW: 25},
        Action.BUILD: 12.5,
        Action.ADD: 51.5,
        Action.CUT: 37.5,
    },
    Material.WILLOW: {
        "Items": {Item.SHORTBOW: 33.3, Item.LONGBOW: 41.5},
        Action.BUILD: 31.5,
        Action.ADD: 126,
        Action.CUT: 67.5,
    },
    Material.MAPLE: {
        "Items": {Item.SHORTBOW: 50, Item.LONGBOW: 58.3},
        Action.BUILD: 51,
        Action.ADD: 201,
        Action.CUT: 100,
    },
    Material.YEW: {
        "Items": {Item.SHORTBOW: 67.5, Item.LONGBOW: 75},
        Action.BUILD: 82,
        Action.ADD: 326,
        Action.CUT: 175,
    },
    Material.MAGIC: {
        "Items": {Item.SHORTBOW: 83.3, Item.LONGBOW: 91.5},
        Action.BUILD: 156,
        Action.ADD: 620,
        Action.CUT: 250,
    },
    Material.REDWOOD: {
        "Items": {Item.STAFF: 10.5},
        Action.BUILD: 222,
        Action.ADD: 725,
        Action.CUT: 380,
    },
}


def con_xp(starting_lvl, totem_count):
    starting_xp = level_to_xp(starting_lvl)
    curr_xp = starting_xp
    curr_lvl = starting_lvl
    for i in range(totem_count):
        curr_xp = curr_xp + curr_lvl
        curr_lvl = xp_to_level(curr_xp)

    return curr_xp - starting_xp


def calc_totem_xp(material, item):
    return (
        (FLETCHING_STUFF[material]["Items"][item] * ACTIONS)
        + (FLETCHING_STUFF[material][Action.ADD] * ACTIONS)
        + (FLETCHING_STUFF[material][Action.BUILD] * ACTIONS)
    )


def calc_chance(axe: Axe, log: Material, level: int):

    top = (
        math.floor(
            (WC_CHANCE[log][axe][0] * ((99 - level) / 98))
            + (WC_CHANCE[log][axe][1] * ((level - 1) / 98))
            + 0.5
        )
        + 1
    )
    return top / 256


def calc_time(logs_needed: int, axe: Axe, log: Material, level: int):
    return (logs_needed / (calc_chance(axe, log, level) / 2.4)) / 3600
