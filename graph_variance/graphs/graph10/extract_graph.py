#!/home/violachenyt/miniconda3/bin/python
import sys,os


for filename in os.listdir("./"):
  if len(filename) < 5:
    continue
  idx = (filename.split(".")[0]).split("_")[1]
  with open(filename) as f:
    lines = f.readlines()
    print(lines)
  path = f"group_{idx}_graphs"
  if not os.path.exists(path):
    os.makedirs(path)
    print(filename,idx)
  f.close()

