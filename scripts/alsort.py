import collections
from scipy
import matplotlib.pyplot as plt
import numpy as np
import os.path
import datetime
from logger import Logger


__name__ = "__alphabetic_sort__"


class AlphabeticSort:
    def __init__(self, path, path_save, plot_cutoff=10, z_cutoff=100):
        """Initializes all values used"""

        # Sets the paths
        self.path, self.path_save = path, path_save
        self.word_list, self.word_list_sorted, self.copy = [], [], []

        # Initializes the logger
        self.log = Logger(os.path.abspath(os.path.dirname(__file__)))

        # Gets the text
        self.text, self.formatted, self.chars = "", "", ""
        self.bar_width = 0.35

        try:
            self.cutoff = int(plot_cutoff)
            self.z_cut = int(z_cutoff)

        except ValueError as e:
            self.log.log(e)

        # The values for the word frequency plot
        self.labels, self.values, self.indsort = [], [], []
        self.indexes = []

        # The variables for the get_time() function
        self.date, self.time = "", ""
        self.time_h, self.time_m, self.time_s = 0, 0, 0
        self.date_y, self.date_m, self.date_d = "", "", ""
        self.format = ""

        # Set the counter
        self.cnt = collections.Counter()
        self.counter, self.cnt_all = 0, 0
        self.frequency = {}

        # Define plot
        self.p = plt

        # Execute functions
        self.startup()

    def startup(self):
        """Executes all the functions in the right order"""

        # Gets the data for saving
        self.get_time()
        self.create_folder()

        # Saves the plots and the data
        self.save()

    def save(self):
        """Calculates the plots and saves them"""
        self.data()
        self.plot(self.cutoff)
        self.zipfs_law(self.z_cut)

    def create_folder(self):
        """Creates the folder if it does not already exist"""
        self.path_save = os.path.join(self.path_save, self.get_time())
        if not os.path.exists(self.path_save):
            os.makedirs(self.path_save)

        return self.path_save

    def get_time(self):
        """Gets the daytime as well as the date"""

        # Gets the date and sets the right format
        self.date_y = datetime.datetime.now().year
        self.date_m = datetime.datetime.now().month
        self.date_d = datetime.datetime.now().day

        if self.date_y < 10:
            self.date_y = "0" + str(self.date_y)
            if self.date_m < 10:
                self.date_m = "0" + str(self.date_m)
                if self.date_d < 10:
                    self.date_d = "0" + str(self.date_d)

        self.date = f"{self.date_y}{self.date_m}{self.date_d}"

        # Gets the time and sets the right format
        self.time_h = datetime.datetime.now().hour
        self.time_m = datetime.datetime.now().minute
        self.time_s = datetime.datetime.now().second
        self.time = f"{self.time_h}{self.time_m}{self.time_s}"

        # Joined format
        self.format = self.date + self.time

        return self.format

    def format_text(self, path):
        """This brings the text into a form that can be easily evaluated"""
        self.chars = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~0123456789\n"

        with open(path, "r") as f:
            self.text = f.read()
            f.close()

        self.formatted = str.maketrans("", "", self.chars)
        return self.text.translate(self.formatted)

    def sort(self):
        """Firstly sorts the data and then splits it"""
        self.word_list = self.format_text(self.path)
        self.word_list = self.word_list.lower()
        self.word_list = self.word_list.rsplit(" ")

        self.word_list.sort()
        return self.word_list

    def counting(self):
        """Counts the occurrences of words in the list"""
        for word in self.sort():
            self.cnt[word] += 1
            self.cnt_all += 1
        return self.cnt, self.cnt_all

    def plot(self, plot_n):
        """Plots the list in form of a scatter plot and saves it"""

        # Plots the 10 most common occurrences of words

        for i in self.counting()[0].most_common(plot_n):
            self.labels.append(i[0])
            self.values.append(i[1])

        # Rearrange your data

        self.labels = np.array(self.labels)
        self.values = np.array(self.values)

        self.indexes = np.arange(len(self.labels))

        self.p.bar(self.indexes, self.values)

        # Add labels
        self.p.xticks(self.indexes + self.bar_width, self.labels)

        # Saves the plot
        self.p.savefig(os.path.join(self.path_save, "most_common_words" + ".png"))

    def data(self):
        """Saves the data in a .txt file"""
        with open(os.path.join(self.path_save, "raw_counted_data" + ".txt"), "w+") as f:
            f.writelines(f"The total number of words is {self.counting()[1]}. The individual ones are:\n")
            for words in sorted(self.counting()[0].items(), key=lambda x: x[1], reverse=True):
                f.writelines(str(words) + "\n")
        f.close()

    def zipfs_law(self, zipf_n):
        """This checks if the words in the text are distributed according to zipfs law"""

        self.zipf_x = np.array(0, 50, dtype=int)

        # Saves the plot
        self.p.savefig(os.path.join(self.path_save, "zipfs_distribution" + ".png"))


if __name__ == "__alphabetic_sort__":
    pass


