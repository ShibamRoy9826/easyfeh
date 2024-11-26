import matplotlib.pyplot as plt
from subprocess import run
from sys import argv

amount=argv[-1]

opt=eval(run(f"python -m easyfeh.easyfeh -gc {amount}",capture_output=True,shell=True).stdout.decode("utf-8").replace("\n",""))

plt.imshow([[opt[i] for i in range(int(amount))]])

plt.show()

