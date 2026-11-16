import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_player_career(matches):
	"""Plot a player's career matches by age difference."""
	wins = matches[matches["Win/Lose"] == "W"]
	losses = matches[matches["Win/Lose"] == "L"]

def _style_axes(ax, matches):
    """Format plot axes."""
    ax.xaxis.tick_top()
    ax.axhline(0, color="gray", linewidth=1)
    ax.grid(True, color="lightgray", linewidth=0.8)
    ax.tick_params(axis="both", colors="gray", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.text(0, 1.04, "Player age:",
        transform=ax.transAxes,
        color="gray", fontsize=9)
    ax.set_ylabel("Age Difference")

def plot_player_career(matches):
    """Plot age differences throughout a player's career."""
    fig, ax = plt.subplots(figsize=(14, 8))

    wins = matches[matches["Win/Lose"] == "W"]
    losses = matches[matches["Win/Lose"] == "L"]

    ax.scatter(wins["Age"], wins["AgeDiff"],
               color="deepskyblue", alpha=0.6, s=15,
               label="Won")
    ax.scatter(losses["Age"], losses["AgeDiff"],
               color="darkviolet", alpha=0.6, s=15,
               label="Lost")

    player = matches.attrs.get("player", "Player")
    ax.set_title(f"{player.title()} Career Matches", pad=100)
    _style_axes(ax, matches)
    ax.legend(
	    loc="upper center",
	    bbox_to_anchor=(0.5, 1.15),
	    ncol=2,
	    frameon=False
	)
    return fig