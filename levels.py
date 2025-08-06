def xp_to_level(xp):
    """Calculates the level in RuneScape based on the given experience."""

    level = 0
    total_xp = 0

    while total_xp < xp:
        level += 1
        total_xp += int(level + 300 * 2 ** (level / 7)) / 4
    if xp == 0:
        return 1
    return level


def level_to_xp(level):
    """Calculates the experience required for a given level in RuneScape."""

    total_xp = 0

    for i in range(1, level):
        total_xp += int(i + 300 * 2 ** (i / 7)) / 4

    return int(total_xp)


"""
xp = 100000
level = xp_to_level(xp)
print(f"Level for {xp} XP: {level}")

level = 87
xp = level_to_xp(level)
print(f"XP required for level {level}: {xp}")
"""
