import random

class Combat:
    # this class handles the fighting between the characters

    @staticmethod
    def calculate_hit(attacker, defender) -> int:
        # figures out how much damage is dealt to a character
        base_damage = 20
        
        # hurt attackers hit weaker than if they have mor ehealth
        health_ratio = attacker.get_health() / attacker.get_max_health()
        
        # there is a random variation in hits
        damage = int(base_damage * health_ratio * random.uniform(0.8, 1.2))
        
        return max(5, damage)  # Minimum 5 damage

    @staticmethod
    def fight(attacker, defender, stamina_cost: int = 20):
        # Tries to attack someone and then there is a check if an attacker has enough energy
        if not attacker.use_stamina(stamina_cost):
            return False, 0
        
        damage = Combat.calculate_hit(attacker, defender)
        defender.take_damage(damage)
        
        return True, damage

    @staticmethod
    def can_fight(attacker, defender):
        # this checks if the characters are able to fight
        return (attacker.is_alive() and 
                defender.is_alive() and 
                attacker.get_stamina() >= 20)