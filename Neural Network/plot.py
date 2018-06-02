import matplotlib.pyplot as plt
import numpy as np


def plot(stats):
    runs = len(stats)
    epochs = len(stats[0])
    # Set x and y axis limit
    plt.xlim(0, epochs - 1)
    plt.ylim(0, 1)
    plt.xticks(range(0, epochs, 10), fontsize=14)
    plt.xlabel('Epochs', size=20)
    plt.ylabel('Rate', size=20)

    TPt = []
    TNt = []
    FNt = []
    DRt = []
    FRt = []
    QRt = []
    x = []
    TPav = 0
    TNav = 0
    FNav = 0
    for i in range(0, epochs):
        x.append(i)
    for i in range(0, runs):
        TPt.append([(stats[i][j][0] / (stats[i][j][0] + stats[i][j][2]))
                    for j in range(0, epochs)])
        TNt.append([(stats[i][j][1] / (stats[i][j][1] + stats[i][j][6]))
                    for j in range(0, epochs)])
        FNt.append([(stats[i][j][2] / (stats[i][j][2] + stats[i][j][0]))
                    for j in range(0, epochs)])
        DRt.append([(stats[i][j][3]) for j in range(0, epochs)])
        FRt.append([(stats[i][j][4]) for j in range(0, epochs)])
        QRt.append([(stats[i][j][5]) for j in range(0, epochs)])

    TPa = np.mean(TPt, axis=0)
    TNa = np.mean(TNt, axis=0)
    FNa = np.mean(FNt, axis=0)
    DRa = np.mean(DRt, axis=0)
    FRa = np.mean(FRt, axis=0)
    QRa = np.mean(QRt, axis=0)
    print('\n======= Average values after final epoch over {} runs ========'.format(runs))
    print('True Positive : {:5.2f}%'.format(TPa[-1] * 100))
    print('True Negative : {:5.2f}%'.format(TNa[-1] * 100))
    print('False Negative: {:5.2f}%'.format(FNa[-1] * 100))
    print('Detection Rate: {:5.2f}%'.format(DRa[-1] * 100))
    print('False Rate    : {:5.2f}%'.format(FRa[-1] * 100))
    print('Quality Rate  : {:5.2f}%\n'.format(QRa[-1] * 100))

    plt.plot(x, TNa,  marker='None', linestyle='--',
             color='k', markersize=4, label='True Negative')
    plt.plot(x, DRa,  marker='None', linestyle='-',
             color='c', lw=4, markersize=8, label='Detection Rate')
    plt.plot(x, TPa,  marker='None', linestyle='--',
             color='b', markersize=4, label='True Positive')
    plt.plot(x, QRa,  marker='None', linestyle='-',
             color='g', lw=4, markersize=8, label='Quality Rate')
    plt.plot(x, FRa,  marker='None', linestyle='-',
             color='r', lw=4, markersize=8, label='False Rate')
    plt.plot(x, FNa,  marker='None', linestyle='--',
             color='m', markersize=4, label='False Negative')
    plt.annotate('%0.3f' % TPa[-1], xy=(1, TPa[-1] - .03), xytext=(8, 0), color='b',
                 xycoords=('axes fraction', 'data'), textcoords='offset points')
    plt.annotate('%0.3f' % TNa[-1], xy=(1, TNa[-1]), xytext=(8, 0), color='k',
                 xycoords=('axes fraction', 'data'), textcoords='offset points')
    plt.annotate('%0.3f' % FNa[-1], xy=(1, FNa[-1] + .02), xytext=(8, 0), color='m',
                 xycoords=('axes fraction', 'data'), textcoords='offset points')
    # plt.annotate('%0.3f' % DRa[-1], xy=(1, DRa[-1] - .03), xytext=(8, 0), color='c',
    # xycoords=('axes fraction', 'data'), textcoords='offset points')
    plt.annotate('%0.3f' % QRa[-1], xy=(1, QRa[-1] - .05), xytext=(8, 0), color='g',
                 xycoords=('axes fraction', 'data'), textcoords='offset points')
    plt.annotate('%0.3f' % FRa[-1], xy=(1, FRa[-1] - .04), xytext=(8, 0), color='r',
                 xycoords=('axes fraction', 'data'), textcoords='offset points')
    plt.legend(loc='best')

    # Graph Title
    plt.suptitle('Crater Detection (Average over {} runs)'.format(
        runs), size=20)

    # Graph Grid style
    plt.grid(linestyle='dotted')

    # Save Figure
    plt.savefig('../log/Quality_Rate.png', dpi=300)

    # Display Graph
    plt.show()
