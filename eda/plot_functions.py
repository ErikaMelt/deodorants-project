import matplotlib.pyplot as plt
import seaborn as sns

# Set the style and color palette
sns.set_style("whitegrid")
color = "blend:#7AB,#EDA"
sns.set_palette(sns.color_palette(color))


def plot_sales_chart(df, title, save_title, x_var, y_var, label_names, x_label, y_label):
    
    # create the bar plot
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(x=x_var, y=y_var, data=df, palette=color)

    # add labels to the bars
    for i, v in enumerate(df[label_names]):
        ax.text(v + 1, i, str(v), color='black')


    # set the chart title and labels
    plt.title(title, fontweight='bold', fontsize=14)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)

    # save the plot as a PNG file
    plt.savefig(f'images/{save_title}', dpi=300, bbox_inches='tight')

    # show the plot
    return plt.show()


def plot_piechart(df, title, filename):
    # Create the pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    df.plot(kind='pie', y='Percent', ax=ax, autopct='%1.1f%%', startangle=90, shadow=False, legend=False)

    # Add title and legend
    ax.set_title(title, fontsize=14)
    ax.legend(df.index, loc='upper left', bbox_to_anchor=(1.0, 0.5))

    # Save the plot as an image file
    plt.savefig(f'images/{filename}', dpi=300, bbox_inches='tight')

    # Show the plot
    return plt.show()


def plot_box(df, cols_num, title='', figsize=(8,10), nrows=None, savefig=None):
    """
    Plots box plots for numerical columns in the DataFrame.

    Args:
        df (pandas DataFrame): The input DataFrame.
        cols_num (list): List of column names with numerical data.
        title (str): Title of the plot (default '').
        figsize (tuple): Size of the figure (default (8,10)).
        nrows (int): Number of rows for subplots (default None).
        savefig (str): Name of the output file to save the plot (default None).

    Returns:
        None.
    """

    if not nrows:
        nrows = len(cols_num)

    sns.set_palette(sns.color_palette(color))

    fig, ax = plt.subplots(nrows=nrows, ncols=1, figsize=figsize)
    fig.subplots_adjust(hspace=1)
    fig.suptitle(title)

    for i, col in enumerate(cols_num):
        sns.boxplot(x=col, data=df, ax=ax[i], palette=color)
        ax[i].set_title(col)

    if savefig:
        plt.savefig(f'images/{savefig}', dpi=300, bbox_inches='tight')

    plt.show()
    return 



def plot_scatter(df, col_x, col_y, title='', figsize=(8,6), savefig=None):
    """
    Plots a scatter plot between two columns in the DataFrame.

    Args:
        df (pandas DataFrame): The input DataFrame.
        col_x (str): Column name for the x-axis.
        col_y (str): Column name for the y-axis.
        title (str): Title of the plot (default '').
        figsize (tuple): Size of the figure (default (8,6)).
        savefig (str): Name of the output file to save the plot (default None).

    Returns:
        None.
    """

    sns.set_palette(sns.color_palette(color))

    plt.figure(figsize=figsize)
    sns.scatterplot(x=col_x, y=col_y, data=df, palette=color)
    plt.xlabel(col_x)
    plt.ylabel(col_y)
    plt.title(title)

    if savefig:
        plt.savefig(f'images/{savefig}', dpi=300, bbox_inches='tight')

    plt.show()
    return

