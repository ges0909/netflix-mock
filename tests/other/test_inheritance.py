class Animal:
    def speak(self):
        raise NotImplementedError


class Cat(Animal):
    def speak(self):
        print("Meow.")


class Dog(Animal):
    def speak(self):
        print("Woof.")


def make_animal_speak(animal: Animal):
    animal.speak()


def test_it():
    make_animal_speak(Cat())
    make_animal_speak(Dog())
