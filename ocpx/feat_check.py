#!/usr/bin/env python
# -*- coding:utf-8 -*-


def check_file(f1, f2):
    input_schema = []
    true_in_use = set()

    with open(f1, "r") as fin1:
        for line in fin1:
            if line[:13] == "input_schema=":
                ins = line[13:].strip()
                input_schema = set(ins.split(","))
                break
    with open(f2, "r") as fin2:
        for line in fin2:
            line = line.strip()
            if line == "" or line[0] == "#":
                continue
            else:
                tks = line.split(";")
                for tk in tks:
                    if "depend=" in tk:
                        dps = tk.split("=")
                        true_in_use.add(dps[-1])
                        break
    # print(input_schema)
    # print(true_in_use)
    print(len(input_schema), len(true_in_use))
    diff = input_schema.difference(true_in_use)
    diff2 = true_in_use.difference(input_schema)
    same = input_schema.intersection(true_in_use)
    print(len(diff), len(diff2), len(same))
    print(diff)
    print(diff2)
    print(same)


if __name__ == "__main__":
    check_file("E:\coding\python\ocpx_analysis\data\conf\suning_features_cvr.conf",
               "E:\coding\python\ocpx_analysis\data\conf\suning_features_list_cvr.conf")
