from tabulate import tabulate

from goblincommander.creature_groups import CreatureGroup


def print_creature_group(group: CreatureGroup) -> None:
    row_data = [[creature.name, type(creature).__name__, creature.adjective,
                 str(creature.stats.beef.value),
                 str(creature.stats.cunning.value),
                 str(creature.stats.quickness.value),
                 f"{creature.stats.reputation.value:3.2f}"] for creature in group.members
                if not creature.is_commander]
    print(tabulate(row_data,
                   headers=["Name", "Type", "Adjective", "Beef", "Cunning", "Quickness", "Reputation"],
                   floatfmt=("", "", "", ".0f", ".0f", ".0f", "3.2f")))
    print()
    print(tabulate([["Averages",
                     str(group.get_avg_beef()),
                     str(group.get_avg_cunning()),
                     str(group.get_avg_quickness()),
                     str(group.get_avg_reputation())]],
                   headers=["", "Beef", "Cunning", "Quickness", "Reputation"],
                   tablefmt="plain",
                   floatfmt="3.2f"))
    print("\n*Averages include your stats")