import os
import platform

from gsodquery import calvin, gsodmaps, joe, jason
from gsodtools import getdb


def display_main_menu():
    '''Main menu'''

    print('GSOD Query Tool, select queries below:\n')

    print('Calvin\'s Queries')
    print('1. Temp vs pressure graph')
    print('2. US average percipitation per year')
    print('3. US average temp per month\n')

    print('Joe\'s Queries')
    print('4. Top 20 maximum gust recorded')
    print('5. Top 20 maximum temperature recorded')
    print('6. Top 20 minimum temperature recorded')
    print('7. Top 20 maximum precipitation recorded\n')

    print('Jason\'s Queries')
    print('8. Latitude, elevation vs mean temperature')
    print('9. Mean atmospheric pressure vs mean wind speed')
    print('A. Mean temperature vs snow depth')
    print('B. Relative humidity vs visbility\n')

    print('Bucky\'s Queries')
    print('C. Temperature data on map over time')
    print('D. Hurricane Ida trace, with humidity and sea level pressure\n')

    print('Q. Quit\n\n')


def main():
    database = getdb.get_db().gsod

    while True:

        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

        display_main_menu()
        choice = input('Enter your choice: ').lower()

        if choice == '1':
            calvin.temp_pressure(database)
        elif choice == '2':
            calvin.avr_precipitation(database)
        elif choice == '3':
            calvin.avr_temp(database)
        elif choice == '4':
            joe.max_gust(database)
        elif choice == '5':
            joe.max_temp(database)
        elif choice == '6':
            joe.min_temp(database)
        elif choice == '7':
            joe.max_precip(database)
        elif choice == '8':
            jason.lat_elev_temp(database)
        elif choice == '9':
            jason.slp_wind(database)
        elif choice == 'a':
            jason.temp_snowdepth(database)
        elif choice == 'b':
            jason.rh_visibility(database)
        elif choice == 'c':
            gsodmaps.temperature_query(database)
        elif choice == 'd':
            gsodmaps.typhoon_query(database)
        elif choice == 'q':
            break
        else:
            print('Invalid choice, try again.')

        input('Press enter to continue...')


if __name__ == '__main__':
    main()
