import random
from typing import Dict, List

gameplay = True

class Hammurabi:
    def __init__(self):
        self.rand = random.Random()

        #---------------------#---------------------
        # Game Variables
        #---------------------#---------------------

        # Custom variables
        # sanity counter
        self.sanity_counter = 0
        self.sanity_dict = {1: "Your strategy is impeccable", 
                            2: "That's a great plan", 
                            3: "Sure, if you think that’s best", 
                            4: "I'm not sure that's gonna work, but okay",
                            5: "This seems like a bad idea, but as you wish",
                            6: "You're leading us to disaster",
                            7: "This is madness. You can't continue anymore"}
        
        # Main variables
        self.yearCounter = 1
        self.harvest_input = 0
        self.buy_input = 0
        self.land_value = 19

        # User asset Variables
        self.population = 100
        self.storage_bushels = 2800
        self.total_acres = 1000

        # Calculation variables
        self.plague_chance = 0  # max 15%
        self.plague = False
        self.starvation = False
        self.uprising = False
        self.new_people = False
        self.harvest_chance = 1  # min 1, max 6
        self.new_harvest = self.harvest_chance * self.harvest_input

        self.rat_chance = 0.40  # max percent
        self.rat_meals = 0.10  # min 10%, max 30%
        self.harvest_loss = False

        # CONSTANT values - rules of the game
        self.starvation_limit = 45 # percent
        self.individual_food_needs = 20  # Constant per person
        self.farm_acres_per_person = 10  # Constant limit per person
        self.farm_cost = 2  # Constant bushels per person
    
    def main(self):
        self.playGame()

    def playGame(self):
        #start loop for while true
        while self.yearCounter <= 10:
            print(f"---------Year {self.yearCounter} of 10----------")
            # statements go after the declarations
            land_purchase = self.askHowManyAcresToBuy(self.land_value, self.storage_bushels)
            if not land_purchase:
                self.askHowManyAcresToSell(self.land_value, self.total_acres)
            self.askHowMuchGrainToFeedPeople(self.storage_bushels, self.population)
            
            # self.starvationDeaths(self.population, self.bushelsFedToPeople)
            # self.update_game_state()
            print("\n")
            self.yearCounter += 1
    # other methods go here
    def printSummaryOfYear():
        pass

    #---------------------#---------------------
    # Custom Gameplay 
    #---------------------#---------------------
    def sanity_check(self):
        if self.sanity_counter <= 6:
            print(self.sanity_dict.get(self.sanity_counter, ""))
        else:
            self.game_over()
            
    def game_over():
        print("Your kingdom has exiled you.\n")
        print("----------GAME OVER----------\n\n")
        exit()       
 
    #---------------------#---------------------
    # Primary Gameplay 
    #---------------------#---------------------
    
        # impliment a sanity check with try excpet
        # keep a counter going to check santity of ruler
        # if santity passes threshold, set santity to False, end game


    def askHowManyAcresToBuy(self, price, bushels):
        
        while True:
            print("\nBuy Land?")
            print(f"The current price of land is {price} bushels per acre.")
            print(f"You have {self.storage_bushels} bushels at your disposal")
            try: 
                buy_acres= int(input(f"How many acres would you like to buy? 0 is an option."))
                # if choosing not to sell, it's 0
                if buy_acres == 0:
                    return False
                    # self.askHowManyAcresToSell(price, self.total_acres)
                else:
                    # calculation logic
                    # if not enough to spend
                    if buy_acres * price > (bushels):
                        self.sanity_check()
                        print("You don't have enough bushels, it is simple math.")
                        # santity check
                        self.sanity_counter += 1
                        continue 
                    # if enough to spend
                    else:
                        original_acres = self.total_acres
                        self.total_acres += buy_acres # increase land
                        self.storage_bushels -= (buy_acres * price) # decrease bushels
                        print(f"\nYou bought {buy_acres} acre(s) of land.")
                        # confirm purchase reciept
                        print(f"Your land increased from {original_acres} to {self.total_acres} acres.")
                        return True
                    # check if santity threshold is passed
                    
            except ValueError:
                self.sanity_check()
                print("Please enter a valid number.")

             
    def askHowManyAcresToSell(self, price, acresOwned):
        while True:
            print("\nSell Land?")
            try:
                print(f"The current value of land is {self.land_value} bushels per acre.")
                print(f"You have {self.total_acres} acres at your disposal.")
                sell_acres = int(input(f"How many acres would you like to sell?"))
                if sell_acres == 0:
                    return
                        # self.askHowMuchGrainToFeedPeople(self.storage_bushels, self.population)
                # if not enough to spend
                if sell_acres > acresOwned:
                    self.sanity_check() #self.total_acres:
                    print("You don't have enough land to sell that many acres.")
                    self.sanity_counter += 1
                    continue
                    # if enough to spend
                else:
                    # assignment value updates
                    self.total_acres -= sell_acres
                    bushel_gain = price * sell_acres
                    self.storage_bushels += bushel_gain
                    
                    print(f"\nYou sold {sell_acres} acres at {self.land_value} per acre.")
                    print(f"{bushel_gain} bushes gained. {self.storage_bushels} bushels in storage.")
                    print(f"You have {self.total_acres} acres now.")
                    return
                
            except ValueError:
                self.sanity_check()
                print("Please enter a valid number.")
        
    def askHowMuchGrainToFeedPeople(self, storage, people):
        print("\nFeed population?")
        try: 
            while True:
                # assignment value
                required_bushels = 20 * people #2000
                print(f"You have {storage} bushels to feed {people} people")
                # assignment value from user #15
                bushelsFedToPeople = int(input("How many bushels do you want to give each person?"))
                # assignment calculation #1500
                total_distributed_bushels = bushelsFedToPeople * people
                # logic statement a
                if total_distributed_bushels > storage:
                    print(f"You only have {storage} bushels. You don't have {total_distributed_bushels} bushels.")
                    # assignment
                    self.sanity_counter += 1
                # logic statement b    
                elif required_bushels > total_distributed_bushels:
                    print("\n----------Not enough to feed each!----------\n")
                    print(f"You fed only {bushelsFedToPeople} bushels to each person.")
                    # assignment calculation #25 gap
                    starvation_gap = round((required_bushels - total_distributed_bushels) / self.individual_food_needs)
                    # update variable
                    self.storage_bushels -= total_distributed_bushels
                    #----------------------
                    # method to check uprising # 45% can't die
                    self.starvation_limit # 45
                    if starvation_gap < (self.starvation_limit / 100) * self.population:
                        fed_people = round(self.population - starvation_gap)
                        print(f"You have fed {fed_people} people. {starvation_gap} people have starved to death.")
                        # update population
                        people = fed_people
                        self.population = people
                        print(f"You now only have {self.population} people in your kingdom." )
                    else:
                        print(f"More than 45% of your people starved, that's {starvation_gap} people.\nNow your people are uprising.")
                        self.game_over()
                        
                else:
                    # feed them
                    self.storage_bushels -= total_distributed_bushels
                    print(f"You gave out {total_distributed_bushels} bushels to feed {self.population} HAPPY people.")
                    print(f"You now have {self.storage_bushels} bushels left in storage.")
                break
        except ValueError:
            self.sanity_check()
            print("Please enter a valid number.")

    
    #def starvationDeaths(population, bushelsFedToPeople):
        
    def askHowManyAcresToPlan(acresOwned, population, bushels):
            # self.sanity_check()
        pass




    #---------------------#---------------------
    # Secondary Gameplay Calculation Methods
    # KEEP IN ORDER OF CALCULATION
    #---------------------#---------------------
    def calc_people_plague():
        pass
    def calc_people_starve():
        pass
    def calc_people_arrival():
        pass
    def calc_harvest():
        pass
    def calc_rats():
        pass
    def calc_land_rate():

        pass






#---------------------#---------------------
# Main  
#---------------------#---------------------
if __name__ == "__main__":
    print("..................................... \n\n Welcome to the game of Hamurabi! \n\n.....................................\n\n ")
    print("Do not play lightly.\nLives are in your hands.\n")

    print("In the previous year 0 people starved to death.")
    print("In the previous year 5 people entered the kingdom.")
    print("The population is now 100.")
    print("We harvested 3000 bushels at 3 bushels per acre.")
    print("Rats destroyed 200 bushels, leaving 2800 bushels in storage.")
    print("The city owns 1000 acres of land.")
    print("Land is currently worth 19 bushels per acre.\n")

    hammurabi = Hammurabi()
    hammurabi.main()
#while True: pass
# while gameplay == True: 

    #pass


