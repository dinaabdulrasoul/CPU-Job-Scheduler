import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots()

start_time_1 = 0
end_time_1 = 3
start_time_2 = 3
end_time_2 = 5
start_time_3 = 5
end_time_3 = 7
total_burst = 3+2+2

ax.broken_barh([(start_time_1, end_time_1), (start_time_2, end_time_2), (start_time_2, end_time_3)], [10, 9], facecolors=('#6259D8', '#E53F08', '#FDB200'))
ax.set_ylim(0, 15)
ax.set_xlim(0, 100)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_yticks([0,20])
ax.set_xticks(np.arange(0, total_burst + 1, 1))

ax.set_axisbelow(True) 

ax.set_yticklabels(['Q1'])
ax.grid(axis='x')
#ax.text(never-6, 14.5, "54%", fontsize=8)
#ax.text((never+seldom)-6, 14.5, "43%", fontsize=8)
#ax.text((never+seldom+undecided)+2, 14.5, "3%", fontsize=8)

fig.suptitle('This is title of the chart', fontsize=16)
#leg1 = mpatches.Patch(color='#6259D8', label='Never')
#leg2 = mpatches.Patch(color='#E53F08', label='Seldom')
#leg3 = mpatches.Patch(color='#FDB200', label='Undecided')
#ax.legend(handles=[leg1, leg2, leg3], ncol=3)

plt.show()