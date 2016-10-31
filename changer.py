replacements = {'\"\"\"':'\"', ',,' : ','}

with open('../data/build-commiter-info-sorted3.csv') as infile, open('../data/build-commiter-info-sorted4.csv', 'w') as outfile:
    for line in infile:
        for src, target in replacements.iteritems():
            line = line.replace(src, target)
        outfile.write(line)