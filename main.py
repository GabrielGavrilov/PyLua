import matplotlib.pyplot as plt




explicitly = 2
equivalent = 5
not_required = 3



certified = 0
not_certified = 0





first_pie_labels = ["Degree explicitly required", "Degree required or an equivalent diploma with experience", "Not required"]
first_pie_percentages = []

second_pie_labels = ["Certifications mentioned", "Certifications not mentioned"]
second_pie_percentages = []

def calc_first_pie_percentages():
        total = explicitly + equivalent + not_required
        first_pie_percentages.append(explicitly / total)
        first_pie_percentages.append(equivalent / total)
        first_pie_percentages.append(not_required / total)
        

def calc_second_pie_percentages():
        total = certified + not_certified
        second_pie_percentages.append(certified / total)
        second_pie_percentages.append(not_certified / total)


if __name__ == "__main__":
        calc_first_pie_percentages()

        # calc_second_pie_percentages()


        plt.tight_layout()
        plt.pie(first_pie_percentages, labels=first_pie_labels, autopct='%1.1f%%')
        plt.show()
        
        # plt.pie(second_pie_percentages, labels=second_pie_labels, autopct='%1.1f%%')
        # plt.show()