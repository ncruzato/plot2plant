import pandas as pd

labeltxt="CS18-DG2F-{}.{}"
labels=[]

for i in range (0,1024):
    if i%2==0:
        label=labeltxt.format(int(i/2+1),1)
    else:
        label= labeltxt.format(int((i-1)/2+1),2)
    labels.append(label)
   
pd.DataFrame(labels).to_csv("labels.csv")