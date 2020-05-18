from collections import Counter
from scipy import special
import matplotlib.pyplot as plt
import numpy as np
import os.path
import datetime


__name__ = "__alphabetic_sort__"


class AlphabeticSort:
    def __init__(self, path, path_save):
        """Initializes all values used"""

        # The paths
        self.path, self.path_save = path, path_save
        self.word_list, self.word_list, self.copy = [], [], []

        # The values for the word frequency plot
        self.labels, self.values, self.indsort = [], [], []
        self.bar_width, self.indexes = 0.35, []

        # The values for the zipf plot
        self.zipf_parameter = 2.
        self.values_z, self.indsort_z = [], []
        self.count, self.bins, self.ignored = None, 0, None
        self.x, self.y = [], []

        # The variables for the get_time() function
        self.date, self.time = "", ""
        self.time_h, self.time_m, self.time_s = 0, 0, 0
        self.date_y, self.date_m, self.date_d = "", "", ""
        self.format = ""

        # Set the counter
        self.cnt = Counter()
        self.counter, self.cnt_all = 0, 0
        self.frequency = {}

        # Define plot
        self.p = plt

        # Sets the special function of scipy
        self.s = special

        # Execute functions
        self.exec()

    def exec(self):
        """Executes all the functions in the right order"""
        # Sorts the words simply
        self.sort()

        # Removes unwanted strings
        self.remove_bracket_and_replace()
        self.remove_latex_objects()

        # Counts the words and sorts after occurrence
        self.counting()

        # Saves the data and the plot, which it creates
        self.get_time()
        self.create_folder()
        self.data()
        self.plot()
        self.zipfs_law()

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

    def create_folder(self):
        """Creates the folder if it does not already exist"""
        self.path_save = os.path.join(self.path_save, self.format)
        if not os.path.exists(self.path_save):
            os.makedirs(self.path_save)

    def sort(self):
        """Firstly sorts the data and then splits it"""
        with open(self.path, "r") as f:
            word_list = f.read()
        self.word_list = word_list.rsplit(" ")
        self.word_list.sort()
        return self.word_list

    def remove_bracket_and_replace(self):
        """Removes all the words with brackets and replaces them without brackets"""
        self.copy = self.word_list
        for word in self.copy:
            if (word[0] == "(") or (word[0] == "["):
                self.word_list[self.counter] = word[0:-1]
            self.counter += 1
        self.counter = 0

    def remove_latex_objects(self):
        """Deletes the latex objects, for more clarity"""
        self.copy = self.word_list
        for word in self.copy:
            if "\\" in word:
                del self.word_list[self.counter]
            if "$" in word:
                del self.word_list[self.counter]
            self.counter += 1
        self.counter = 0

    def counting(self):
        """Counts the occurrences of words in the list"""
        for word in self.word_list:
            self.count = self.frequency.get(word, 0)
            self.frequency[word] = self.count + 1
            self.cnt[word] += 1
            self.cnt_all += 1

    def plot(self):
        """Plots the list in form of a scatter plot and saves it"""

        # Plots the 10 most common occurrences of words
        for i in self.cnt.most_common(10):
            self.labels.append(i[0])
            self.values.append(i[1])

        # sort your values in descending order
        self.indsort = np.argsort(self.values)[::-1]

        # rearrange your data
        self.labels = np.array(self.labels)[self.indsort]
        self.values = np.array(self.values)[self.indsort]

        self.indexes = np.arange(len(self.labels))

        self.p.bar(self.indexes, self.values)

        # add labels
        self.p.xticks(self.indexes + self.bar_width, self.labels)
        # saves the plot
        self.p.savefig(os.path.join(self.path_save, "most_common_words" + ".png"))

    def data(self):
        """Saves the data in a .txt file"""
        with open(os.path.join(self.path_save, "raw_counted_data" + ".txt"), "w+") as f:
            f.writelines(f"The total number of words is {self.cnt_all}. The individual ones are:\n")
            for words in sorted(self.cnt.items(), key=lambda x: x[1], reverse=True):
                f.writelines(str(words) + "\n")
        f.close()

    def zipfs_law(self):
        """This checks if the words in the text are distributed according to zipfs law"""

        # limit the max. number of words with the most common function
        for i in self.cnt.most_common(len(self.word_list)):
            self.values_z.append(i[1])

        # rearrange your data
        self.values_z = np.array(self.values_z)

        # Calculates the Zipf distribution and plots it
        self.count, self.bins, self.ignored = plt.hist(self.values_z[self.values_z < 50], 50, normed=True)
        self.x = np.arange(1., 50.)
        self.y = self.x**(-self.zipf_parameter) / self.s.zetac(self.zipf_parameter)
        self.p.plot(self.x, self.y / max(self.y), linewidth=2, color='r')

        # saves the plot
        self.p.savefig(os.path.join(self.path_save, "zipfs_distribution" + ".png"))

if __name__ == "__alphabetic_sort__":
    pass


