# Genetic Algorithm for String Guessing

This project implements a genetic algorithm to guess a target string. The algorithm evolves a population of candidate strings over multiple generations, aiming to converge to the specified target.

## Files

- **genetic.py**: This file contains the core logic for the genetic algorithm. 

    - The `Genetic` class represents individuals in the genetic algorithm. It has the following methods:
        - `__init__(self, chromosome=None, target=None)`: Initializes an individual with a chromosome (a string) and a target string.
        - `create_gnomes(self)`: Creates a string of gnomes (random characters) with the same length as the target.
        - `_create_gnomes(self)`: Creates a single gnome (random character).
        - `generation(self, parent)`: Generates a new individual by combining genes from two parents.
        - `get_fitness(self)`: Calculates the fitness score of an individual based on the number of mismatches with the target.

- **guess_sents.py**: This file manages the overall genetic algorithm process.

    - The `guess_sents` class has the following methods:
        - `__init__(self, target)`: Initializes the genetic algorithm with a target string.
        - `get_target(self)`: Initializes the population, evolves generations, and prints the progress until the target string is found.
        - `show(self)`: Prints the current generation, the best-guessed string, its chromosome, and fitness score.

- **info.py**: This file contains configuration parameters.

    - `population_size`: The number of individuals in each generation.
    - `gens`: The set of characters that can be used in the strings.

- **test.py**: A sample script demonstrating how to use the genetic algorithm to guess a target string.

## Usage

To run the genetic algorithm, follow these steps:

1. Ensure you have Python installed on your machine.

2. Open a terminal or command prompt.

3. Navigate to the project directory.

4. Run the `test.py` script:

   ```bash
   python test.py
   ```

5. View the output, which shows the evolution of generations and the best-guessed string.

## Configuration

You can adjust the configuration parameters in the `info.py` file:

- **population_size**: The number of individuals in each generation.
- **gens**: The set of characters that can be used in the strings.

## Customization

Feel free to customize the genetic algorithm for your specific use case:

- Modify the fitness function in the `Genetic` class for a more tailored evaluation of candidate strings.

- Experiment with different population sizes, mutation rates, and selection strategies.
## see result for test


```python
from guess_sents import guess_sents

a = guess_sents("this ia a test for this code")
a.get_target()

```

and outpot is :  

```bash
loop is  : 2
generation: <genetic.genetic object at 0x7fbeddeea8f0>  password:  t sthoda i ssh ohtt rt  ise  Fitness: 20
loop is  : 3
generation: <genetic.genetic object at 0x7fbeddef8220>  password: taie  a sccit  eth ctts   te  Fitness: 18
loop is  : 4
generation: <genetic.genetic object at 0x7fbeddee8c70>  password: thideca a  sstaiit hhtsshst   Fitness: 16
loop is  : 5
generation: <genetic.genetic object at 0x7fbeddee8c70>  password: thideca a  sstaiit hhtsshst   Fitness: 16
loop is  : 6
generation: <genetic.genetic object at 0x7fbeddeea410>  password: ahie ia s cftt shh sti   tie  Fitness: 15
loop is  : 7
generation: <genetic.genetic object at 0x7fbeddef8fa0>  password: this oa h fft afit tsisttoie  Fitness: 13
loop is  : 8
generation: <genetic.genetic object at 0x7fbeddef8fa0>  password: this oa h fft afit tsisttoie  Fitness: 13
loop is  : 9
generation: <genetic.genetic object at 0x7fbeddef9900>  password: tsis iafa tfet  oh stis  sis  Fitness: 12
loop is  : 10
generation: <genetic.genetic object at 0x7fbeddee9ae0>  password: this  a h fitt  oi t isttoie  Fitness: 11
loop is  : 11
generation: <genetic.genetic object at 0x7fbeddee8580>  password: th s ia h tet  ffs aisstcode  Fitness: 10
loop is  : 12
generation: <genetic.genetic object at 0x7fbeddee8580>  password: th s ia h tet  ffs aisstcode  Fitness: 10
loop is  : 13
generation: <genetic.genetic object at 0x7fbeddee8580>  password: th s ia h tet  ffs aisstcode  Fitness: 10
loop is  : 14
generation: <genetic.genetic object at 0x7fbeddee8c10>  password: this ia s  es  ffs heistctde  Fitness: 9
loop is  : 15
generation: <genetic.genetic object at 0x7fbeddef8e80>  password: chis ia    est foe tsis cths  Fitness: 8
loop is  : 16
generation: <genetic.genetic object at 0x7fbeddee9390>  password: chie ia    est fos tois cohe  Fitness: 7
loop is  : 17
generation: <genetic.genetic object at 0x7fbeddee9390>  password: chie ia    est fos tois cohe  Fitness: 7
loop is  : 18
generation: <genetic.genetic object at 0x7fbeddeead10>  password: ch s ia   sest foo tiis code  Fitness: 6
loop is  : 19
generation: <genetic.genetic object at 0x7fbeddee8250>  password: this ia   te   fos this c de  Fitness: 5
loop is  : 20
generation: <genetic.genetic object at 0x7fbeddee8250>  password: this ia   te   fos this c de  Fitness: 5
loop is  : 21
generation: <genetic.genetic object at 0x7fbeddee8250>  password: this ia   te   fos this c de  Fitness: 5
loop is  : 22
generation: <genetic.genetic object at 0x7fbeddee8250>  password: this ia   te   fos this c de  Fitness: 5
loop is  : 23
generation: <genetic.genetic object at 0x7fbeddee8250>  password: this ia   te   fos this c de  Fitness: 5
loop is  : 24
generation: <genetic.genetic object at 0x7fbeddeea860>  password: this oa t test foo this code  Fitness: 3
loop is  : 25
generation: <genetic.genetic object at 0x7fbeddeea860>  password: this oa t test foo this code  Fitness: 3
loop is  : 26
generation: <genetic.genetic object at 0x7fbeddeea860>  password: this oa t test foo this code  Fitness: 3
loop is  : 27
generation: <genetic.genetic object at 0x7fbeddeead10>  password: this i  a test foi this code  Fitness: 2
loop is  : 28
generation: <genetic.genetic object at 0x7fbeddeead10>  password: this i  a test foi this code  Fitness: 2
loop is  : 29
generation: <genetic.genetic object at 0x7fbeddeead10>  password: this i  a test foi this code  Fitness: 2
loop is  : 30
generation: <genetic.genetic object at 0x7fbeddeead10>  password: this i  a test foi this code  Fitness: 2
loop is  : 31
generation: <genetic.genetic object at 0x7fbeddeead10>  password: this i  a test foi this code  Fitness: 2
loop is  : 32
generation: <genetic.genetic object at 0x7fbeddeead10>  password: this i  a test foi this code  Fitness: 2
loop is  : 33
generation: <genetic.genetic object at 0x7fbeddeead10>  password: this i  a test foi this code  Fitness: 2
loop is  : 34
generation: <genetic.genetic object at 0x7fbeddeead10>  password: this i  a test foi this code  Fitness: 2
loop is  : 35
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 36
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 37
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 38
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 39
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 40
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 41
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 42
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 43
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 44
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 45
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 46
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 47
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 48
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 49
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 50
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 51
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 52
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 53
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 54
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 55
generation: <genetic.genetic object at 0x7fbeddef99c0>  password: this ia a test foa this code  Fitness: 1
loop is  : 55
generation: <genetic.genetic object at 0x7fbeddef84c0>  password: this ia a test for this code  Fitness: 0

```
## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- The genetic algorithm implementation is inspired by [genetic algorithms on GeeksforGeeks](https://www.geeksforgeeks.org/genetic-algorithms/).

