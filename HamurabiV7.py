import random

class Hammurabi:
    def __init__(self):
        self.rand = random.Random()
        
        # Custom Variables
        self.sanity_counter = 0
        self.sanity_dict = {
            1: "Your strategy is impeccable, yet..", 
            2: "That's a great plan, however...", 
            3: "Sure, if you think that’s best, but...", 
            4: "I'm not sure that's gonna work...",
            5: "This seems like a bad idea, becasue...",
            6: "You're leading us to disaster!",
            7: "This is madness. You can't continue like this!"
        }
        self.harvestRate = 0
        self.harvestedBushels = 0

        # Game Variables
        self.yearCounter = 1
        self.harvest_input = 0
        self.buy_input = 0
        self.land_value = 19
        self.lastYearLandValue = 19
        self.land_value_change = False
        self.starvationCounter = 0

        # User asset Variables
        self.population = 100
        self.storage_bushels = 2800
        self.bushel_storage_change = 0
        self.total_acres = 1000
        self.acres_planted = 0
        self.harvest_per_acre = 0
        self.bushels_of_grain = self.storage_bushels

        # Calculation variables
        self.plague_occurred = False
        self.plague_deaths = 0
        self.rat_infestation = False
        self.rat_chance = 0.40  # 40% chance of rats
        self.newPeople = 0

        # CONSTANT values - rules of the game
        self.starvation_limit = 45  # percent
        self.individual_food_needs = 20  # Constant per person
        self.farm_acres_per_person = 10  # Constant limit per person
        self.farm_cost = 2  # Constant bushels per person

    def main(self):
        self.playGame()

    def playGame(self):
        # Welcome to the game
        print("..................................... \n\n Welcome to the game of Hammurabi! \n\n.....................................\n\n ")
        print("Do not play lightly.\nLives are in your hands.\n")
        self.firstSummary()
        # Start the game
        while self.yearCounter <= 10:
            print(f"\n----------------------Year {self.yearCounter} of 10----------------------\n\n")
            # print(f"DEBUG: Population before actions: {self.population}")
            land_purchase = self.askHowManyAcresToBuy(self.land_value, self.storage_bushels)
            if not land_purchase:
                self.askHowManyAcresToSell(self.land_value, self.total_acres)
            self.askHowMuchGrainToFeedPeople(self.storage_bushels, self.population)
            # print(f"DEBUG: Population after feeding: {self.population}")
            self.askHowManyAcresToPlant(self.total_acres, self.population, self.storage_bushels)
            if self.starvationCounter == 0:
                self.newPeople = self.immigrants(self.population, self.total_acres, self.storage_bushels)
                self.population += self.newPeople
             # Check for uprising
            if self.uprising(self.population, self.starvationCounter):
                print("----------GAME OVER----------")
                print("The people have revolted due to excessive starvation.")
                print("-----------------------------\n")
                break
            self.grainEatenByRats(self.storage_bushels)
            self.plagueDeaths()
            self.newCostOfLand()
            # print(f"DEBUG: Population after planting: {self.population}")
            print("\n")
            self.yearCounter += 1
            self.yearCheck()

    def sanity_check(self):
        if self.sanity_counter <= 7:
            print(f"\nMaster...")
            print(self.sanity_dict.get(self.sanity_counter, ""))
        else:
            self.game_over()

    def game_over(self):
        print("----------GAME OVER----------")
        print("\nYour kingdom has exiled you\n")
        print("----------GAME OVER----------\n\n")


    def askHowManyAcresToBuy(self, price, bushels):
        while True:
            print("\nBuy Land?")
            print(f"The current price of land is {price} bushels per acre.")
            print(f"You have {self.storage_bushels} bushels at your disposal")
            try:
                buy_acres = int(input("How many acres would you like to buy? 0 is an option."))
                if buy_acres == 0:
                    return False
                if buy_acres * price > bushels:
                    self.sanity_check()
                    print("You don't have enough bushels, it is simple math.")
                    self.sanity_counter += 1
                    continue
                else:
                    original_acres = self.total_acres
                    self.total_acres += buy_acres
                    self.storage_bushels -= (buy_acres * price)
                    print(f"\nYou bought {buy_acres} acre(s) of land.")
                    print(f"Your land increased from {original_acres} to {self.total_acres} acres.")
                    return True
            except ValueError:
                self.sanity_check()
                print("Please enter a valid number.")

    def askHowManyAcresToSell(self, price, acresOwned):
        while True:
            print("\nSell Land?")
            try:
                print(f"The current value of land is {self.land_value} bushels per acre.")
                print(f"You have {acresOwned} acres at your disposal.")
                sell_acres = int(input("How many acres would you like to sell?"))
                if sell_acres == 0:
                    return
                if sell_acres > acresOwned:
                    print("You don't have enough land to sell that many acres.")
                    self.sanity_counter += 1
                    self.sanity_check()
                    continue
                else:
                    self.total_acres -= sell_acres
                    bushel_gain = price * sell_acres
                    self.storage_bushels += bushel_gain
                    print(f"\nYou sold {sell_acres} acres at {self.land_value} per acre.")
                    print(f"{bushel_gain} bushels gained. {self.storage_bushels} bushels in storage.")
                    print(f"You have {self.total_acres} acres now.")
                    return
            except ValueError:
                self.sanity_check()
                print("Please enter a valid number.")

    def askHowMuchGrainToFeedPeople(self, storage, people):
        print("\nFeed population?")
        try:
            while True:
                print(f"You have {storage} bushels to feed {people} people")
                bushelsFedToPeople = int(input("How many bushels do you want to give each person?"))
                total_distributed_bushels = bushelsFedToPeople * people
                if total_distributed_bushels > storage:
                    print(f"You only have {storage} bushels. You don't have {total_distributed_bushels} bushels.")
                    self.sanity_counter += 1
                    self.sanity_check()
                    continue
                elif total_distributed_bushels == (self.individual_food_needs * people):
                    self.storage_bushels -= total_distributed_bushels
                    print(f"\nYou served {total_distributed_bushels} bushels, all are Happy!")
                    print(f"You now have {self.storage_bushels} bushels left in storage.")
                    self.starvationCounter = self.starvationDeaths(people, total_distributed_bushels)
                else:
                    self.storage_bushels -= total_distributed_bushels
                    print(f"\nYou served {total_distributed_bushels} bushels to feed {self.population}")
                    print(f"You now have {self.storage_bushels} bushels left in storage.")
                    self.starvationCounter = self.starvationDeaths(people, total_distributed_bushels)
                return
        except ValueError:
            print("Please enter a valid number.")
            self.sanity_counter += 1
            self.sanity_check()

    def askHowManyAcresToPlant(self, acresOwned, population, bushels):
        print("\nHarvest your acres?")
        try:
            while True:
                print(f"You have {self.total_acres} acres at your disposal.")
                harvest_acres = int(input(f"How many acres would you like to plant? "))
                if harvest_acres == 0:
                    return
                self.harvestRate = random.randint(1, 6)
                
                # Check if the number of acres to plant is less than or equal to the acres owned
                if harvest_acres > acresOwned:
                    print("You don't have enough land to plant that many acres.")
                    self.sanity_counter += 1
                    self.sanity_check()
                    continue
                
                # Check if there are enough bushels to plant the acres
                if harvest_acres > bushels / 2:
                    print("You don't have enough bushels to plant that many acres.")
                    self.sanity_counter += 1
                    self.sanity_check()
                    continue
                
                # Check if there are enough people to work on the acres
                if harvest_acres > population * 10:
                    print("You don't have enough people to work on that many acres.")
                    self.sanity_counter += 1
                    self.sanity_check()
                    continue

                # If all conditions are met, calculate the harvest
                self.harvestedBushels = self.harvestRate * harvest_acres
                bushels += self.harvestedBushels
                self.storage_bushels = bushels
                print(f"\nHarvested {self.harvestedBushels} bushels at {self.harvestRate} per acre.")
                return
        except ValueError:
            print("Please enter a valid number.")
            self.sanity_counter += 1
            self.sanity_check()       

    def starvationDeaths(self, people, total_distributed_bushels):
        required_bushels = self.individual_food_needs * people  # Total food needed
        if total_distributed_bushels < required_bushels:
            shortfall = required_bushels - total_distributed_bushels  # Shortfall in bushels
            starvation_gap = (shortfall + self.individual_food_needs - 1) // self.individual_food_needs  # Proper rounding to calculate starvation
            if starvation_gap >= self.population:  # Ensure starvation gap does not exceed population
                starvation_gap = self.population
            self.population -= starvation_gap  # Reduce population by the number of starved people
            return starvation_gap
        return 0  # No starvation

    def plagueDeaths(self):
        if self.rand.randint(0, 99) < 15:
            plague_deaths = self.population // 2
            self.population -= plague_deaths
            self.plague_deaths = plague_deaths
            self.plague_occurred = True
        else:
            self.plague_deaths = 0
            self.plague_occurred = False
        return self.plague_deaths

    def newCostOfLand(self):
        price_change = self.rand.randint(17, 23)
        self.lastYearLandValue = self.land_value
        if price_change == self.land_value:
            self.land_value_change = False
        else:
            self.land_value = price_change
            self.land_value_change = True
        return self.land_value

    def grainEatenByRats(self, bushels):
        if self.rand.random() <= self.rat_chance:
            percentage = self.rand.randint(10, 30)
            self.bushel_storage_change = bushels * percentage // 100
            self.storage_bushels -= self.bushel_storage_change
            self.rat_infestation = True
        else:
            self.bushel_storage_change = 0
            self.rat_infestation = False
        return self.bushel_storage_change

    def immigrants(self, population, acresOwned, grainInStorage):
        newPeople = (20 * acresOwned + grainInStorage) // (100 * population) + 1
        print(f"DEBUG: Calculating immigrants: {newPeople} (20 * {acresOwned} + {grainInStorage}) // (100 * {population}) + 1")
        return newPeople

    def uprising(self, population, starved):
        return starved > 0.5 * population
    
    def yearCheck(self):
        if self.yearCounter >= 10:
            self.finalSummary()
            exit()
        else:
            self.printSummary()

    def printSummary(self):
        print(f"\n----------------------SUMMARY OF YEAR {self.yearCounter}----------------------")
        print("O great Hammurabi!")
        print(f"You are in year {self.yearCounter} of your ten year rule.")
        if self.plague_occurred:
            print("\n----------BAD NEWS: DEATH(S) by PLAGUE")
            print(f"In the previous year {self.plague_deaths} died of plague")
            print("-----------\n")
        else:
            print("\nYour kingdom remained untouched by plague.\n")
        if self.starvationCounter > 0:
            print("\n----------BAD NEWS: DEATH(S) by STARVATION")
            print(f"In the previous year {self.starvationCounter} people starved to death.\n")
        else:
            print("----------GOOD NEWS: ")
            print(f"\nIn the previous year 0 people starved to death.")    
        print(f"We harvested {self.harvestedBushels} bushels at {self.harvestRate} bushels per acre.")
        print(f"\n{self.newPeople} people entered the city.")
        if self.rat_infestation and self.bushel_storage_change > 0:
            print("\n-RATS!-RATS!-RATS!-RATS!-RATS!-RATS!-\n")  
            print(f"Rats destroyed {self.bushel_storage_change} bushels, leaving {self.storage_bushels} bushels in storage.")
        print(f"The city owns {self.total_acres} acres of land.")
        if self.land_value_change:
            print(f"\n--------PRICE CHANGE NOTICE: Last year's price: {self.lastYearLandValue}")
            print(f"Land is currently worth {self.land_value} bushels per acre.")
        else:
            print(f"Land is currently worth {self.land_value} bushels per acre.")
        if self.land_value > 21:
            print(f"\n----------SELL! SELL! SELL!----------")
        elif self.land_value < 18:
            print("----------BUY! BUY! BUY!----------\n")
        print(f"The population is {self.population}.")

    def firstSummary(self):
        print("O great Hammurabi!")
        print("In the previous year 0 people starved to death.")
        print("In the previous year 5 people entered the kingdom.")
        print("We harvested 3000 bushels at 3 bushels per acre.")
        print("Rats destroyed 200 bushels, leaving 2800 bushels in storage.")
        print("The city owns 1000 acres of land.")
        print("Land is currently worth 19 bushels per acre.\n")
        print("The population is 100.")

    def finalSummary(self):
        print("------------YOU WON!-----------")
        print()
        pass


if __name__ == "__main__":
    hammurabi = Hammurabi()
    hammurabi.main()
