# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset = pandas.DataFrame(undefined, undefined.1, undefined.2, undefined.3, undefined.4, undefined.5, undefined.6)
# dataset = dataset.drop_duplicates()

# Paste or type your script code here:
import matplotlib.pyplot as plt
import seaborn as sns

corr = dataset.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.show()
