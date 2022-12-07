#!/home/violachenyt/miniconda3/bin/python
import sys,os


for filename in os.listdir("./"):
  if not filename.endswith(".txt"): continue
  idx = (filename.split(".")[0]).split("_")[1]
  if int(idx) > 100: continue
  path = f"group_{idx}_graphs"
  # if not os.path.exists(path):
  #   os.makedirs(path)
    # print(filename,idx)
    
  with open(filename) as f:
    lines = "".join(f.readlines())
    lines = lines.split("\nGraph ")
    for line in lines:
      graph_id = line.split(",")[0]
      # print(graph_id)
      el = "  ".join(line.split("\n")[2:])
      el = el.split("  ")[:-1]
      with open(f"{path}/{graph_id}.txt","w") as gf:
        gf.write("\n".join(el))
      gf.close()
  
  f.close()

