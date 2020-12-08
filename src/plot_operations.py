"""
this module plots the weather  data fetched from database
include methods:
generate_box_plot is to draw box plot from year to year
generate_line_plot is to draw line plot from a specific month from a chosen year
"""
import matplotlib.pyplot as plt

from common import is_number
from db_operations import DBOperations
from scrape_weather import WeatherScraper


class PlotOperations:
    """
    this class is to box plot and line plot
    weather mean temperatures of year to year or specific month respectively
    """

    def __init__(self):
        self.box_plot_path_saving_dict = {}
        self.line_plot_path_saving_dict = {}

    def generate_box_plot(self, start_year: int, end_year: int) -> dict:
        """
        :param end_year: starting year for box plotting
        :param start_year: ending year for line plotting
        :return: returns the generated box plot images' saving paths class instance
        """

        my_db = DBOperations('weather.sqlite')
        years_data_list = []
        for current_year in range(start_year, end_year + 1):
            years_data_list.extend(my_db.fetch_data(current_year))

        monthly_weather_data = {}  # format: [1:[Jan temps],2:[Feb temps],..,12:[Dec temps]]
        for month in range(1, 13):
            if month not in monthly_weather_data:
                monthly_weather_data[month] = []

        for item in years_data_list:
            if is_number(item[5]):
                monthly_weather_data[int(item[1][5:7])] = float(item[5])

        # TODO: wait to cleaning before submit the project
        # for current_year in range(start_year, end_year + 1):
        #     for month in range(1, 13):
        #         monthly_list = my_db.fetch_data(current_year, month)
        #         if month not in monthly_weather_data:
        #             monthly_weather_data[month] = []
        #         for item in monthly_list:
        #             if is_number(item[5]):
        #                 monthly_weather_data[month].append(float(item[5]))

        plot_title = 'Monthly Temperature Distribution for: ' + str(start_year) + ' to ' + str(end_year)
        # print(monthly_weather_data)
        plt.boxplot(monthly_weather_data.values(), sym="o", whis=1.5)
        plt.xlabel('Month')
        plt.ylabel('Temperature (Celsius)')
        plt.title(plot_title)
        save_path = str(start_year) + '_to_' + str(end_year) + '.png'
        plt.savefig(save_path)
        self.box_plot_path_saving_dict[str(start_year) + '-' + str(end_year)] = save_path
        plt.show()

        return self.box_plot_path_saving_dict

    def generate_line_plot(self, specific_year: int, specific_month: int) -> dict:
        """
        :param specific_month: the chosen month for line plotting
        :param specific_year: the chosen year for line plotting
        :return: returns the generated line plot images' saving paths class instance
        """
        month_string_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        my_db = DBOperations('weather.sqlite')
        specific_timestamp = []  # 2020-12-01
        specific_month_data = []

        month_data = my_db.fetch_data(specific_year, specific_month)
        for item in month_data:
            if is_number(item[5]):
                specific_timestamp.append(float(item[1][-2:]))
                specific_month_data.append(float(item[5]))
        # print(specific_year, '-', specific_month, ':', specific_month_data)

        plt.plot(specific_timestamp, specific_month_data)
        plt.xlabel('Day')
        plt.ylabel('Temperature (Celsius)')
        plot_title = 'Daily Temperature Distribution for: ' + month_string_list[specific_month - 1] + ' ' + str(
            specific_year)
        plt.title(plot_title)
        save_path = str(specific_year) + '-' + str(specific_month) + '.png'
        plt.savefig(save_path)
        self.line_plot_path_saving_dict[str(specific_year) + '-' + str(specific_month)] = save_path
        plt.show()

        return self.line_plot_path_saving_dict


if __name__ == '__main__':
    my_scraper = WeatherScraper()
    for year in range(2018, 2020 + 1):
        my_scraper.start_scraping('', year)

    mydb = DBOperations('weather.sqlite')
    mydb.initialize_db()
    mydb.purge_data()
    mydb.save_data(my_scraper.weather)

    my_plot = PlotOperations()
    my_plot.generate_box_plot(2018, 2020)
    my_plot.generate_line_plot(2018, 5)
    my_plot.generate_line_plot(2020, 12)
