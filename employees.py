"""
Student information for this assignment:

Replace <FULL NAME> with your name.
On my/our honor, Alexandru Aghinitei and <FULL NAME>, this
programming assignment is my own work and I have not provided this code to
any other student.

I have read and understand the course syllabus's guidelines regarding Academic
Integrity. I understand that if I violate the Academic Integrity policy (e.g.
copy code from someone else, have the code generated by an LLM, or give my
code to someone else), the case shall be submitted to the Office of the Dean of
Students. Academic penalties up to and including an F in the course are likely.

UT EID 1: asa3964
UT EID 2:
"""

from abc import ABC, abstractmethod
import random

# Constants provided by the assignment
DAILY_EXPENSE = 60
HAPPINESS_THRESHOLD = 50
MANAGER_BONUS = 1000
TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD = 50
PERM_EMPLOYEE_PERFORMANCE_THRESHOLD = 25
RELATIONSHIP_THRESHOLD = 10
INITIAL_PERFORMANCE = 75
INITIAL_HAPPINESS = 50
PERCENTAGE_MAX = 100
PERCENTAGE_MIN = 0
SALARY_ERROR_MESSAGE = "Salary must be non-negative."


class Employee(ABC):
    """Abstract base class representing a generic employee in the system."""

    def __init__(self, name, manager, salary, savings):
        self.relationships = {}
        self.savings = savings
        self.is_employed = True
        self.__name = name
        self.__manager = manager
        self.performance = INITIAL_PERFORMANCE
        self.happiness = INITIAL_HAPPINESS
        self.salary = salary
    
    @abstractmethod
    def work(self):
        pass
    
    @property
    def manager(self):
        return self.__manager
    
    @property
    def name(self):
        return self.__name
    
    @property
    def salary(self):
        return self.__salary
    
    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError(SALARY_ERROR_MESSAGE)
        self.__salary = value
        
    @property
    def performance(self):
        return self.__performance
    
    @performance.setter
    def performance(self, value):
        if value < PERCENTAGE_MIN:
            self.__performance = PERCENTAGE_MIN
        elif value > PERCENTAGE_MAX:
            self.__performance = PERCENTAGE_MAX
        else:
            self.__performance = value
            
    @property
    def happiness(self):
        return self.__happiness
    
    @happiness.setter
    def happiness(self, value):
        if value < PERCENTAGE_MIN:
            self.__happiness = PERCENTAGE_MIN
        elif value > PERCENTAGE_MAX:
            self.__happiness = PERCENTAGE_MAX
        else:
            self.__happiness = value
        
    
    def interact(self, other):
        if other.name not in self.relationships:
            self.relationships[other.name] = 0
        
        if self.relationships[other.name] > RELATIONSHIP_THRESHOLD:
            if self.happiness + 1 > PERCENTAGE_MAX:
                self.happiness = PERCENTAGE_MAX
            else:
                self.happiness += 1

        elif self.happiness >= HAPPINESS_THRESHOLD and other.happiness >= HAPPINESS_THRESHOLD:
            self.relationships[other.name] += 1

        else:
            self.relationships[other.name] -= 1
            if self.happiness - 1 < PERCENTAGE_MIN:
                self.happiness = PERCENTAGE_MIN
            else:
                self.happiness -= 1
                  
    def daily_expense(self):
        self.savings -= DAILY_EXPENSE
        if self.happiness - 1 < PERCENTAGE_MIN:
            self.happiness = PERCENTAGE_MIN
        else:
            self.happiness -= 1            
    def __str__(self) -> str:
        return (f"{self.__name}\n"
                f"\tSalary: ${self.salary}\n"
                f"\tSavings: ${self.savings}\n"
                f"\tHappiness: {self.happiness}%\n"
                f"\tPerformance: {self.performance}%")
  
class Manager(Employee):
    def work(self):
        random_number = random.randint(-5, 5)
        self.performance += random_number
        
        if self.performance < PERCENTAGE_MIN:
            self.performance = PERCENTAGE_MIN
        elif self.performance > PERCENTAGE_MAX:
            self.performance = PERCENTAGE_MAX
        
        if random_number <= 0:
            if self.happiness - 1 < PERCENTAGE_MIN:
                self.happiness = PERCENTAGE_MIN
            else:
                self.happiness -= 1
            for key in self.relationships:
                self.relationships[key] -= 1
        else:
            if self.happiness + 1 > PERCENTAGE_MAX:
                self.happiness = PERCENTAGE_MAX
            else:
                self.happiness += 1


class TemporaryEmployee(Employee):
    def work(self):
        random_number = random.randint(-15, 15)
        self.performance += random_number
        
        if self.performance < PERCENTAGE_MIN:
            self.performance = PERCENTAGE_MIN
        elif self.performance > PERCENTAGE_MAX:
            self.performance = PERCENTAGE_MAX

        if random_number <= 0:
            if self.happiness - 2 < PERCENTAGE_MIN:
                self.happiness = PERCENTAGE_MIN
            else:
                self.happiness -= 2
        else:
            if self.happiness + 1 > PERCENTAGE_MAX:
                self.happiness = PERCENTAGE_MAX
            else:
                self.happiness += 1
            
    def interact(self, other):
        super().interact(other)
        
        if isinstance(other, Manager):
            if other.happiness > HAPPINESS_THRESHOLD and self.performance >= TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD:
                self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                self.salary //= 2
                if self.salary <= 0:
                    self.is_employed = False
                else:
                    if self.happiness - 5 < PERCENTAGE_MIN:
                        self.happiness = PERCENTAGE_MIN
                    else:
                        self.happiness -= 5


class PermanentEmployee(Employee):
    def work(self):
        random_number = random.randint(-10, 10)
        
        self.performance += random_number
        if self.performance < PERCENTAGE_MIN:
            self.performance = PERCENTAGE_MIN
        elif self.performance > PERCENTAGE_MAX:
            self.performance = PERCENTAGE_MAX

        if random_number >= 0:
            if self.happiness + 1 > PERCENTAGE_MAX:
                self.happiness = PERCENTAGE_MAX
            else:
                self.happiness += 1
            
    def interact(self, other):
        super().interact(other)
        
        if isinstance(other, Manager):
            if other.happiness > HAPPINESS_THRESHOLD and self.performance >= PERM_EMPLOYEE_PERFORMANCE_THRESHOLD:
                self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                if self.happiness - 1 < PERCENTAGE_MIN:
                    self.happiness = PERCENTAGE_MIN
                else:
                    self.happiness -= 1