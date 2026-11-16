# Tennis Career Package

This package contains functions that allow the input of a tennis player to generate a plot of their career timeline, specifically the wins and losses of every match. 

The two main functions are: 
 - get_player_matches(): Downloads and processes a player's career match data into a pandas DataFrame.
 - plot_player_career(): Creates a scatter plot showing age differences between players and their opponents, with points colored according to wins and losses.

### Installation and Use

The package can be installed directly from GitHub using this command:

```{bash}
pip install git+https://github.com/UCB-stat159-f26/hw03-camilapippens.git
```

The package can be imported by adding the following at the top of python files:

```{python}
from tennis_career_pkg import get_player_matches, plot_player_career
```

For example, the functions in the package can be used as such:

#### Serena Williams

```{python}
	serena = get_player_matches("Serena Williams")
	print(serena.head())

	fig = plot_player_career(serena)
```

#### Rafael Nadal

```{python}
	rafael = get_player_matches("Rafael Nadal")
	print(rafael.head())
	
	fig = plot_player_career(rafael)
```

The plotting function returns a Matplotlib figure that can also be saved using:

```{python}
fig.savefig("serena_plot.png", dpi=300, bbox_inches="tight")
```


### Processing

The data is retrieved from tennisabstract.com js URLs. For example, https://www.tennisabstract.com/jsmatches/SerenaWilliamsCareer.js is the link for Serena Williams's data, and https://www.tennisabstract.com/jsmatches/RafaelNadalCareer.js is the link to Rafael Nadal's data.

The data for female players contains opponent dates of birth, whereas the data for male players simply contains the opponent's age. Thus, each player's calculated difference between opponent age was done differently for male and female players. 


### Player Birthdates

The package currently includes birthdates for Serena Williams and Rafael Nadal.

For other players, users must provide a birthdate using the optional birthdate argument:

```{python}
	player = get_player_matches(
	    "Victoria Azarenka",
	    birthdate="1989-07-31"
	)
```


### Testing

The package uses pytest for automated tests.

To run the tests, run the following command:

```{bash}
python -m pytest -v
```

Tests use the example female and male js match records located in the tests folder.

The tests check private functions: player name formatting, JavaScript parsing, opponent age calculations, and player age calculations.

### Personal Reflections

I thought it was very cool learning how to create a package so that others can use functions without having to create their own. Making packages seems like a very useful way to spread accessibility and just in general provide something so that someone doesn't have to entirely build functions from the ground up. Additionally, it's useful to refer back to if I create other useful packages to apply in any future projects.

Learning to include tests for functions and overall just make the package reproducible was also very cool. 