import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

dico = [{"type": 'man_', "seq": 1, "result": 35}, { "type": 'woman_',"seq": 1, "result": 45},
{"type": 'boy_', "seq": 1,"result": 25}, {"type": 'girl_', "seq":1,"result" : 15},
{"type": 'man_', "seq": 2, "result": 32}, { "type": 'woman_',"seq": 2, "result": 42},
{"type": 'boy_', "seq": 2,"result": 22}, {"type": 'girl_', "seq":2,"result" : 12}]
df = pd.DataFrame(dico)

sns.barplot(data = df, x = "type", y = "result", hue = "seq")
plt.show()
