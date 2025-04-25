import pandas as pd
import matplotlib.pyplot as plt

dataset={
    
    "Storage":[4,8,16],
    "Count":[2,3,4]
    }
a=[1,2,3]
var=pd.Series(a)
df = pd.DataFrame(dataset)
print(df,"\n\n",a,"\n\n",df.loc[[0,1]])

print(pd.__version__,"\n\n",pd.options.display.max_rows)

df.plot()
plt.show()


print(df.corr())
