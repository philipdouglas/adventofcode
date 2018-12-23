from copy import deepcopy

SPELLS =         ["Magic Missile", "Drain", "Shield", "Poison", "Recharge"]
COSTS =          {"Magic Missile":53, "Drain":73, "Shield":113, "Poison":173, "Recharge":229}
CAST_DAMAGES =   {"Magic Missile":4, "Drain":2, "Shield":0, "Poison":0, "Recharge":0}
EFFECT_DAMAGES = {"Poison":3}
HEALS =          {"Magic Missile":0, "Drain":2, "Shield":0, "Poison":0, "Recharge":0}
ARMOR_BOOSTS =   {"Shield":7}
MANA_BOOSTS =    {"Recharge":101}
DURATIONS =      {"Shield":6, "Poison":6, "Recharge":5}

memo_cache = {}

def apply_effects(hero_hp, boss_hp, boss_damage, hero_armor, hero_mana, timers):
    if timers["Shield"] > 0:
        hero_armor = ARMOR_BOOSTS["Shield"]
    else:
        hero_armor = 0
    if timers["Poison"] > 0:
        boss_hp -= EFFECT_DAMAGES["Poison"]
    if timers["Recharge"] > 0:
        hero_mana += MANA_BOOSTS["Recharge"]
    for status in timers:
        timers[status] = max(0, timers[status]-1)
    return hero_hp, boss_hp, boss_damage, hero_armor, hero_mana, timers

def play_boss(hero_hp, boss_hp, boss_damage, hero_armor, hero_mana, mana_spent, timers, hard_mode = False):
    hero_hp, boss_hp, boss_damage, hero_armor, hero_mana, timers = apply_effects(hero_hp, boss_hp, boss_damage, hero_armor, hero_mana, timers)
    if hero_hp <= 0: return float('inf')
    if boss_hp <= 0: return mana_spent
    return play_hero(hero_hp - max(1, boss_damage - hero_armor), boss_hp, boss_damage, hero_armor, hero_mana, mana_spent, timers, hard_mode)

def play_hero(hero_hp, boss_hp, boss_damage, hero_armor, hero_mana, mana_spent, timers, hard_mode = False):
    memo_key = (hero_hp, boss_hp, boss_damage, hero_armor, hero_mana, mana_spent, tuple(timers), hard_mode)
    if memo_key in memo_cache: return memo_cache[memo_key]

    if hard_mode: hero_hp -=1

    hero_hp, boss_hp, boss_damage, hero_armor, hero_mana, timers = apply_effects(hero_hp, boss_hp, boss_damage, hero_armor, hero_mana, timers)
    if hero_hp <= 0: return float('inf')
    if boss_hp <= 0: return mana_spent

    min_mana_spent = float('inf')

    for spell in SPELLS:
        if hero_mana >= COSTS[spell]:
            if spell in timers and timers[spell]>0: continue
            new_timers = deepcopy(timers)
            if spell in new_timers:
                new_timers[spell] = DURATIONS[spell]
            pb = play_boss(hero_hp + HEALS[spell], boss_hp - CAST_DAMAGES[spell], boss_damage, hero_armor, hero_mana - COSTS[spell], mana_spent + COSTS[spell], new_timers, hard_mode)
            min_mana_spent = min(min_mana_spent, pb)
    memo_cache[memo_key] = min_mana_spent
    return memo_cache[memo_key]

def main():
    hero_hp = 50
    hero_armor = 0
    hero_mana = 500

    mana_spent = 0

    boss_hp = 71
    boss_damage = 10

    timers = {"Shield":0, "Poison": 0, "Recharge":0}

    print ("Answer to part 1: {}".format(play_hero(hero_hp, boss_hp, boss_damage, hero_armor, hero_mana, mana_spent, timers, False)))
    print ("Answer to part 2: {}".format(play_hero(hero_hp, boss_hp, boss_damage, hero_armor, hero_mana, mana_spent, timers, True)))

if __name__ == "__main__":
    main()
