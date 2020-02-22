


##### READ & WRITE ###

def read(filepath):
    def read_line(infile):
        line = infile.readline()
        return [int(val) for val in line.split(' ')]

    infile = open(filepath, 'r')

    n_books, n_libs, n_days = read_line(infile)  # LINE 1
    books = read_line(infile)  # LINE 2

    libs = []
    for id in range(0, n_libs):
        lnbooks, lsignup, lships = read_line(infile)  # LINE l1
        lbooks = read_line(infile)  # LINE l2: book ids
        assert lnbooks == len(lbooks), "book number must match"
        libs.append({'id': id, 'signup': lsignup, 'ships': lships, 'books': lbooks})

    infile.close()

    return n_books, n_libs, n_days, books, libs

def score(books, libs_to_scan):
    score = 0
    for libts in libs_to_scan:
        for b in libts['books']:
            score += books[b]
    return score

def write(libs_to_scan, outfilepath='output.txt'):
    outfile = open(outfilepath, 'w')
    outfile.writelines(f"{len(libs_to_scan)}\n")
    for lib_to_scan in libs_to_scan:
        outfile.writelines(f"{lib_to_scan['id']} {len(lib_to_scan['books'])}\n")
        outfile.writelines(" ".join([str(b) for b in lib_to_scan['books']]) + "\n")

    outfile.close()


### WORK

n_books, n_libs, n_days, books, libs = read('in/a_example.txt')

ts = [libs[0]]

print(f"Score is {score(books, ts)}")

write(ts, 'output_a.txt')