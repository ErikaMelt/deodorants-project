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
