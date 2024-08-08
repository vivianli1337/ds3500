# Import the libraries
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import textwrap


class Visualizations:
    def __init__(self, data, stop_words):
        """Initialize Visualizations"""
        self.data = data
        self.stop_words = stop_words

    def wordcount_sankey(self, word_list):
        """ Generate a Sankey diagram visualizing word frequencies in the text data.
            Args:
                word_list (list): A list of additional words to include in the Sankey diagram.
            Returns:
                None
        """
        labels = list(self.data["word_count"].keys()) + word_list
        source = []
        target = []
        value = []

        # Set source & target colors
        source_colors = ["royalblue"] * len(self.data["word_count"])
        target_colors = ["dodgerblue"] * len(word_list)

        # Iterate through word counts of each label and create source, target, and value lists
        for i, label in enumerate(self.data["word_count"].keys()):
            for word in word_list:
                source.append(i)
                target.append(len(self.data["word_count"]) + word_list.index(word))
                value.append(self.data["word_count"][label].get(word, 0))

        # Create HTML labels with custom font properties
        label_html = [f'<span style="font-size: 14px; font-weight: bold;">{label}</span>' for label in labels]

        # Create Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=label_html,
                color=source_colors + target_colors
            ),
            link=dict(
                source=source,
                target=target,
                value=value
            )
        )])

        fig.update_layout(title_text="Text-to-Word Sankey Diagram")
        fig.show()

    def word_cloud_subplots(self):
        """ Generate subplots of word clouds for each text entry in the data.
            Returns:
                    None
        """
        # Layout of the plots
        num_plots = len(self.data["clean_text"])
        rows = (num_plots + 4) // 5
        cols = min(5, num_plots)

        fig = plt.figure(figsize=(20, 6 * rows))

        # Iterate through clean text data and create word clouds in subplots
        for i, (label, text) in enumerate(self.data["clean_text"].items()):
            wordcloud = WordCloud(width=800, height=800, background_color='white', stopwords=self.stop_words,
                                  min_font_size=10, colormap='winter').generate(text)
            ax = fig.add_subplot(rows, cols, i + 1)
            ax.imshow(wordcloud, interpolation='bilinear')

            # Wrap the title
            wrapped_title = "\n".join(textwrap.wrap(label, width=38))
            ax.set_title(wrapped_title, fontsize=10)

            ax.axis("off")

        # Adjust spacing and layout
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.75, wspace=0.1, hspace=0.1)  # Adjust spacing
        plt.tight_layout()
        plt.show()

    def word_frequency_overlay(self):
        """ Generate a bar plot comparing the top 15% word frequencies across different text entries.
            Returns:
                None
        """
        fig = go.Figure()

        # Iterate through word counts of each label and create bar plots
        for label, word_count in self.data["word_count"].items():
            total_words = sum(word_count.values())
            sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
            percent = int(len(sorted_word_count) * 0.15)
            top_words = sorted_word_count[:percent]

            # Extract words and their frequencies
            words = [word[0] for word in top_words if word[0] not in self.stop_words]
            frequencies = [word[1] / total_words * 100 for word in top_words]

            # Add bar trace to the plot
            fig.add_trace(go.Bar(
                x=words,
                y=frequencies,
                name=label,
                width=0.9  # Adjust the width of the bars as desired (e.g., 0.5 for wider bars)
            ))

        # Layout of the plot
        fig.update_layout(
            title='Top 15% Word Frequency Comparison',
            xaxis_title='Word',
            yaxis_title='Frequency (%)',
            legend_title='Text legend',
            font=dict(size=12),
            legend=dict(
                traceorder='normal',
                x=0,
                y=-1.3,
                bordercolor='rgba(0, 0, 0, 0.5)',
                borderwidth=1,
                itemwidth=100
            )
        )

        # Display the plot
        fig.show()
