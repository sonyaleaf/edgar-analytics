import sys
import csv

def main():
    # open input files and create/write to output file
    f_log = open(sys.argv[1],'rU')
    f_inact_pd = open(sys.argv[2])
    f_output = open(sys.argv[3],'w+')

    # define inactivity period as integer
    inactivity_period = int(f_inact_pd.read())

    # read log csv file and sum rows (not including first)
    log_reader = csv.reader(f_log)
    next(log_reader)
    row_count = sum(1 for row in log_reader)

    # define arrays for each field
    ip = []
    date = []
    time = []
    cik = []
    accession = []
    extention = []

    # restart reader at beginning of csv file
    f_log.seek(0)

    # determine index of each relevant field from first line in csv file
    first_row = next(log_reader)
    # first_row_list = first_row[0].split(',')
    # ^readme says fields are separated by commas, but above code doesn't work for provided test
    a = first_row.index('ip')
    b = first_row.index('date')
    c = first_row.index('time')
    d = first_row.index('cik')
    e = first_row.index('accession')
    f = first_row.index('extention')

    # restart reader at beginning of cvs file and move to second line
    f_log.seek(0)
    next(log_reader)

    # fill lists according to indices determined above
    for entry in log_reader:
        # entry = row[0].split(',')
        # ^readme says fields are separated by commas, but above code doesn't work for provided test
        ip.append(entry[a])
        date.append(entry[b])
        time.append(entry[c])
        cik.append(entry[d])
        accession.append(entry[e])
        extention.append(entry[f])

    # approach: count the number of times (n) the first time appears in the array, check the
    # first n entries of the ip array to see whether each ip address is unique
    # if an ip address is repeated count the number of times it's repeated - this is the
    # number of document requests in that second for the ip address
    # make "matrix" where the columns represent each time and are in chronological order,
    # each ip address appears only once in each column and the following entry in the column
    # is the number of document requests for that ip address at that time

    log_matrix = []
    i = 0
    while i < row_count:
        ip_2 = []
        log_matrix_list = []
        t = time[i]
        date_and_time = date[i] + " " + time[i]
        log_matrix_list.append(date_and_time)
        log_matrix_list.append(t)
        n = time.count(t)
        for j in range(i, i + n):
            if ip[j] not in ip_2:
                ip_2.append(ip[j])
                log_matrix_list.append(ip[j])
                log_matrix_list.append(ip[i:i+n].count(ip[j]))
        log_matrix.append(log_matrix_list)
        i = i + n

    # iterate log_matrix by time
    # check whether the inactivity period has passed for each ip address at each iteration
    # if it has write to sessionization.txt
    # when the end of the file is reached, go back in chronological order and write to sessionization.txt
    # adding the document requests for each ip address

    # convert times in log_matrix to seconds (including hours and minutes), 3600 s in hr, 60 s in min
    for k in range(0,len(log_matrix)):
        t = log_matrix[k][1]
        time_list = t.split(':')
        hours = int(time_list[0])
        mins = int(time_list[1])
        time_s = hours*3600 + mins*60 + int(time_list[2])
        log_matrix[k][1] = time_s

    for ip_address in ip:
        # keep only the unique entries in ip
        index = ip.index(ip_address)
        q = index + 1
        while q < len(ip):
            if ip_address == ip[q]:
                ip[q] = ""
            q = q + 1
        # write output for remaining ip addresses by iterating in order by ip (also chronological), tracking the number of times the ip address appears in the following
        # columns and adding the associated document requests (row following the ip address in log_matrix)
        col_ind = []
        ip_ind = []
        for p in range(0, len(log_matrix)):
            if ip_address in log_matrix[p]:
                col_ind.append(p)
                ip_ind.append(log_matrix[p].index(ip_address))
        

def t_diff(t_lrg,t_sm):
    t_diff = int(t_lrg)-int(t_sm)
    # calculate time difference when times don't fall on the same day (assuming consecutive days)
    if t_diff < 0:
        t_big = 86400 - t_lrg
        t_diff = t_sm + t_big
    return t_diff

if __name__ == "__main__":
    main()
