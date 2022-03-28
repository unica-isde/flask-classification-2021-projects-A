import matplotlib.pyplot as plt


def make_figure(labels, data):
    """
    This function returns a figure of a plot. The plot is built with labels and data inputs.
    """

    # make the plot
    fig, ax = plt.subplots()


    # fill plot
    ax.barh(labels, data, align='center')
    ax.invert_yaxis()  # labels read top-to-bottom

    ax.set_title('Output scores')

    # tight_layout automatically adjusts subplot params so that the subplot(s) fits in to the figure area.
    fig.tight_layout()

    return fig