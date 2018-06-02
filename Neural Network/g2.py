import matplotlib.pyplot as plt
import numpy as np

# Read from CSV file into numpy array
graph = np.genfromtxt('../log/log.txt', delimiter=",")
graph = graph.T
DR = graph[8]
FR = graph[9]
QR = graph[10]

runs = 10

l = 150

# Set x and y axis limit
plt.xlim(0, l - 1)
plt.ylim(0, 1)

# X and Y axis title
plt.xlabel('Epochs', size=20)
plt.ylabel('Rate', size=20)

DRa = []
FRa = []
QRa = []
DRt = []
FRt = []
QRt = []
x = []
for i in range(0, l):
    x.append(i)
for i in range(0, 10):
    DRt.append([DR[j] for j in range(i * l, i * l + l)])
    FRt.append([FR[j] for j in range(i * l, i * l + l)])
    QRt.append([QR[j] for j in range(i * l, i * l + l)])

DRa = np.mean(DRt, axis=0)
FRa = np.mean(FRt, axis=0)
QRa = np.mean(QRt, axis=0)

plt.plot(x, DRa,  marker='None', linestyle='-', color='b',
         markersize=4, label='Detection Rate')
plt.plot(x, QRa,  marker='None', linestyle='-',
         color='g', markersize=4, label='Quality Rate')
plt.plot(x, FRa,  marker='None', linestyle='-',
         color='r', markersize=4, label='False Rate')


#plt.plot(x, QR,  marker='o', linestyle='--', color = 'b', markersize=4, label = 'Quality Rate')
#plt.plot(x, FR,  marker='o', linestyle='--', color = 'r', markersize=4, label = 'False Rate')
plt.legend(loc='best')

plt.annotate('%0.3f' % DRa.max(), xy=(1, DRa.max()), xytext=(8, 0),
             xycoords=('axes fraction', 'data'), textcoords='offset points')
plt.annotate('%0.3f' % QRa.max(), xy=(1, QRa.max()), xytext=(8, 0),
             xycoords=('axes fraction', 'data'), textcoords='offset points')
plt.annotate('%0.3f' % FRa.min(), xy=(1, FRa.min()), xytext=(8, 0),
             xycoords=('axes fraction', 'data'), textcoords='offset points')

# Fig Text
#text = "No of Epochs in each run = " + str(70)
# plt.text(5, 20, text, color='white', fontsize=15,
#    bbox={'facecolor':'black', 'pad':4})

# Graph Title
plt.suptitle("Crater Detection (Average over 10 runs)", size=20)

# Graph Grid style
plt.grid(linestyle='dotted')

# Save Figure
plt.savefig('../log/Quality_Rate.png', dpi=300)

# Display Graph
plt.show()
