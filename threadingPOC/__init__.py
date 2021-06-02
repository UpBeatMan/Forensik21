from timeit import timeit
from database import mydatabase
from threading import Thread

__version__ = '0.1.0'

# global variables
thread_count = 4

#  static test variables - count_query() result
row_count = 237

# table names
HISTORY = 'moz_formhistory'

# static for testing purposes
start_id = 1188


def main():
    dbms = mydatabase.MyDatabase(mydatabase.SQLITE, dbname='mydb.sqlite')
    dbms.count_query()

    # Rundung für den Test erst einmal irrelecant!
    each_thread = row_count//thread_count
    print(each_thread)

    # calculate table row ranges according to the thread numbers
    #def calc_borders(start, end, threads):
        # todo write seperator

    # thread 1 example
    beg_range = start_id
    end_range = start_id + (each_thread - 1)
    print(end_range)

    # using ranges for creating the thread logic


    def read_range(start, end):
        build = "SELECT * FROM {TBL_HST} WHERE id BETWEEN " + str(start) + " AND " + str(end) + ";"
        print(build)
        query = build.format(TBL_HST=HISTORY)
        dbms.print_all_data(query=query)

    read_range(beg_range, end_range)

    # timeit() normal vs threaded read access

    #dbms.print_all_data(mydatabase.HISTORY)
    #dbms.count_all_rows()


# run the programm
if __name__ == "__main__": main()

