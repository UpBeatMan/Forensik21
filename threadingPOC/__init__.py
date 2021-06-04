from statistics import mean
from timeit import Timer
from database import mydatabase
from threading import Thread

__version__ = '0.1.0'

# global variables
thread_count = 4

th_low = 2
th_medium = 4
th_high = 8
th_extreme = 16

# table names
HISTORY = 'moz_formhistory'

# count_query() result - static test variable
row_count = 235

# first id in table - static test variable
start_id = 1190


def main():
    dbms = mydatabase.MyDatabase(mydatabase.SQLITE, dbname='mydb.sqlite')
    dbms.count_query()

    def each_thread(rows, th_cat):
        # Rundung nach unten für den Test erst einmal irrelecant!
        each_th = (rows) // th_cat
        print("With ", th_cat, " each thread handles ", each_th, ".")
        return each_th

    print("Thread_count 4 is the default!")
    each_thread(row_count, th_low)
    each_thread(row_count, th_medium)
    each_thread(row_count, th_high)
    each_thread(row_count, th_extreme)

    def end_range(rows, entry):
        max_range = entry + (rows - 1)
        print("End row of all threads: ", max_range, "\n")
        return max_range

    max_range = end_range(row_count, start_id)

    # Functions
    # calculate table row ranges according to the thread numbers
    def calc_borders(entry, rows, threads):
        # todo write seperator
        last_entry = entry
        for thread in range(threads):
            if last_entry == entry:
                next_border = last_entry + (rows // threads) - 1
            else:
                next_border = last_entry + (rows // threads)

            # print("Thread number: ", thread)
            # print("Begin range: ", last_entry)
            # print("End range: ", next_border, "\n")

            # read_range(last_entry, next_border)
            t = Thread(target=read_range, args=(last_entry, next_border))
            t.start()

            last_entry = next_border + 1

    def read_range(start, end):
        build = "SELECT * FROM {TBL_HST} WHERE id BETWEEN " + str(start) + " AND " + str(end) + ";"
        # print(build)
        query = build.format(TBL_HST=HISTORY)
        dbms.print_all_data(query=query)


    # first try - not working yet! --> static variable row_count for test
    # dbms.count_all_rows()

    # dbms.print_all_data(mydatabase.HISTORY)

    # timeit() normal vs threaded read access
    # calc_borders(start_id, row_count, thread_count)
    # read_range(start_id, max_range)

    # Testläufe
    i = 10

    # Ergebnislisten
    results0 = []
    results1 = []

    # Testfunktionen - not working!
    # function0 = "calc_borders(start_id, row_count, thread_count)"
    # function1 = "read_range(start_id, end_range)"

    def test_case0(iterations_i, result_list, th_cat):
        for loop in range(iterations_i):
            # with threading module
            t = Timer(lambda: calc_borders(start_id, row_count, th_cat))
            time = t.timeit(number=1)
            print("Zeitmessung mit ", th_cat, " Threads in ns - Durchlauf ", loop + 1, ": ", time)
            result_list.append(time)
        return result_list

    def test_case1(iterations_i, result_list):
        for loop in range(iterations_i):
            # with threading module

            t = Timer(lambda: read_range(start_id, max_range))
            time = t.timeit(number=1)
            print("Zeitmessung ohne Threading in ns - Durchlauf ", loop + 1, ": ", time)
            result_list.append(time)
        return result_list

    def show_results(iterations_i, result_list):
        # print("\n")
        print(result_list)
        mean_value = mean(result_list)
        # plain_val = "%f" % mean_value
        # print(plain_val)
        print("Durchschnittswert über ", iterations_i, "Testläufe: ", mean_value, "\n")

    # print("Mit Threading und Aufteilen der Lesezugriffe.")
    test_case0(i, results0, th_low)
    show_results(i, results0)

    # print("Ohne Threading und Aufteilen der Lesezugriffe.")
    test_case1(i, results1)
    show_results(i, results1)

    # for loop in range(i):
    #     # with threading module
    #     # print("\nZeitmessung mit Threading in ns - Durchlauf ", loop + 1, ": ")
    #     wt = Timer(lambda: calc_borders(start_id, row_count, thread_count))
    #     time0 = wt.timeit(number=1)
    #     # print(time0)
    #     results0.append(time0)
    #
    # print("\n")
    # print(results0)
    # mean_value0 = mean(results0)
    # plain_val0 = "%f" % mean_value0
    # print(plain_val0)
    # print("Durchschnittswert über ", i, "Testläufe: ", mean_value0)
    #
    #
    # results1 = []
    #
    # for loop in range(i):
    #     # print(" \n Zeitmessung ohne Threading in ns: ", loop + 1, ": ")
    #     ot = Timer(lambda: read_range(start_id, end_range))
    #     time1 = ot.timeit(number=1)
    #     # print(time1)
    #     results1.append(time1)
    #
    # print("\n")
    # print(results1)
    # mean_value1 = mean(results1)
    # plain_val1 = "%f" % mean_value1
    # print(plain_val1)
    # print("Durchschnittswert über ", i, "Testläufe: ", mean_value1)

# run the programm
if __name__ == "__main__": main()

