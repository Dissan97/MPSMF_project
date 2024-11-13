import numpy as np
from matplotlib import pyplot as plt


def multiplot(data=None, cols=2, name='', plot_color='blue'):
    # preparing the subplots
    if data is None:
        data = {}
    num_plots = len(data)
    cols = 2
    rows = int(np.ceil(num_plots / cols))
    fig, axs = plt.subplots(rows, cols, figsize=(20, 6 * rows))
    axs = axs.flatten()
    i = 0

    for key in data:
        ax = axs[i]
        i += 1
        fig_name = f"{key} {name}"
        ax.plot(data[key], label=fig_name, color=plot_color)
        ax.set_xlabel('Date')
        ax.set_ylabel(name)
        ax.set_title(fig_name)

    for j in range(num_plots, len(axs)):
        axs[j].axis('off')

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show the plots
    plt.show()
