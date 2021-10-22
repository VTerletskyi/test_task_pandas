from os.path import realpath

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class DrawingPlots:

    def __init__(self, end_point):
        self.end_point = end_point

    def download_json(self):
        data = requests.get(self.end_point).json()
        df = pd.DataFrame(data)
        df.to_json("data_from_s3.json")

    def draw_plots(self):
        self.download_json()

        df = pd.read_json("data_from_s3.json")

        # Checking the correctness of the count corners
        df["right_count_cor"] = df["gt_corners"] == df["rb_corners"]
        right_count_corners = df.groupby(["right_count_cor"]).agg(count=("right_count_cor", "count")).reset_index()
        plt.pie(np.array(right_count_corners["count"]), labels=right_count_corners["right_count_cor"].to_list())
        plt.title("Pie chart about count corners in the room and in the model")
        plt.savefig('plots/check_corners.png')

        # Display deviations, if there is only one graph on the graph, then the coincidence is 100%
        df = df.sort_values("gt_corners", ascending=False)
        df.plot(x="name", y=["gt_corners", "rb_corners"])
        plt.title("The deviation between the angles 'gt_corners', 'rb_corners'")
        plt.savefig('plots/dev_corners.png')

        # Showed the deviation on the mean
        df = df.sort_values("mean", ascending=False)
        df.plot(x="name", y=["mean", "max", "min"])
        plt.savefig('plots/dev_mean.png')

        # Showed the deviation on the floor.
        df = df.sort_values("floor_mean", ascending=False)
        df.plot(x="name", y=["floor_mean", "floor_max", "floor_min"])
        plt.savefig('plots/dev_floor.png')

        # Showed the deviation on the ceiling.
        df = df.sort_values("ceiling_mean", ascending=False)
        df.plot(x="name", y=["ceiling_mean", "ceiling_max", "ceiling_min"])
        plt.savefig('plots/dev_ceiling.png')

        plt.show()
        return realpath("plots")


if __name__ == '__main__':
    url = "https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json"
    DrawingPlots(url).draw_plots()
