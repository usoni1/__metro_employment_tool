import csv
import numpy
import re
import pprint as pp

reader = csv.reader(open("/PyCharm Projects/__metro_employment_tool/app/main/suit/data.csv", "r"), delimiter=",")
x = list(reader)
pp.pprint(x)