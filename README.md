# sistema_bancario

## Description 

The package sistema_bancario is used to:
- Simulate a banking system and save the generated data to a tuple, using the function "simular_sistema".
- Continue the simulation of the bank account system saved and passed to the function "continuar_simulacao".

It is a simple banking system simulator, with the possibility of creating users and accounts. Also, it allows for depositing and withdrawing money from the user's main account. The supported language is Portuguese (BR).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install sistema_bancario.

```bash
pip install sistema_bancario
```

## Usage

```python
from sistema_bancario import sistema_bancario
saved = sistema_bancario.simular_sistema()
resume = sistema_bancario.continuar_simulacao(saved)
```

## Author
Wesley Oliveira

## License
[MIT](https://choosealicense.com/licenses/mit/)