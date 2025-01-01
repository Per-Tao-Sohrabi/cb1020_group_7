from MainModel import MainModel
import matplotlib.pyplot as plt

model = MainModel()

for i in range(30): #SPECIFY NUMBER OF STEPS IN range()
    model.step()

#COLLECTING STORED DATA
model_df = model.datacollector.get_model_vars_dataframe()
agent_df = model.datacollector.get_agent_vars_dataframe()

#model_df.head(5)

#agent_df

#DOWNLOAD DATA FILES
model_df.to_excel("model_data.xlsx", index=False)
agent_df.to_excel("agent_data.xlsx", index=False)


#PLOT DATA
model_df.plot( lw=3, figsize=(10, 6))

plt.ylabel("")
plt.xlabel("Time step")
plt.grid("on")
#plt.setp(plt.gca(), xlim=(-1, 1000), ylim=(0, 1))

plt.show()

model.plot_data_overlap()