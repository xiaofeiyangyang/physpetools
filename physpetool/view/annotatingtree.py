import os
from physpetool.database.dbpath import getlocaldbpath
from physpetool.utils.checkinputfile import checkFile, removeEmptyStr
from physpetool.utils.colorconvert import random_color

dbpath = getlocaldbpath()


def readIputFile(inputfile):
    org_name = []
    with open(inputfile) as f:
        for name in f:
            each_name = name.strip()
            org_name.append(each_name)

    org_name_check = removeEmptyStr(org_name)
    return org_name_check


def readTaxDb():
    orgpath = os.path.join(dbpath, "organism.txt")
    organism_list = []
    with open(orgpath) as f:
        for org in f:
            each_org = org.strip().split('\t')
            organism_list.append([each_org[1], each_org[-1]])
    return organism_list


def matchInput(input_organism, taxon):
    organism_list = readTaxDb()
    taxon_dict = {'kingdom': 0, 'phylum': 1, 'class': 2, 'order': 3}
    id = taxon_dict.get(taxon)
    match_list = []
    # temp = []
    anno = []
    for i in input_organism:
        for j in organism_list:
            if i == j[0]:
                # temp.append(i)
                # temp.append(j[1].split(';')[id].strip())
                temp_anno = j[1].split(';')[id].strip()
                anno.append(j[1].split(';')[id].strip())
                match_list.append([i, temp_anno])
                break
            else:
                pass
    unique_anno = list(set(anno))
    length_anno = len(unique_anno)
    color = random_color(length_anno)
    anno_dict = {}
    for line in range(length_anno):
        anno_dict[unique_anno[line]] = color[line]
    return match_list, anno_dict


def colorRange(input, output, taxon):
    if not os.path.exists(output):
        os.makedirs(output)
    fw_name = "range_color_by_" + taxon + ".txt"
    open_path = os.path.join(output, fw_name)
    fw = open(open_path, 'wb')
    fw.write('TREE_COLORS\nSEPARATOR TAB\nDATA\n')
    inputfile = checkFile(input)

    input_list = readIputFile(inputfile)
    match_list, anno_dict = matchInput(input_list, taxon)
    for line in match_list:
        color = anno_dict[line[1]]
        write_data = "{0}\trange\t{1}\t{2}\n".format(line[0], color, line[1])
        fw.write(write_data)
    fw.close()
