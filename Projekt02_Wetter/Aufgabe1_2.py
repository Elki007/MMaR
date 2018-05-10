import numpy as np
import matplotlib.pyplot as plt

tabelle = np.loadtxt("wetterdaten2.txt", delimiter=';',skiprows=1, usecols=np.arange(15))

spalte_tx = np.linspace(2.0, 20.0, num=2)
xAchse = np.arange(len(spalte_tx))
print(spalte_tx)
print(np.linspace(2.0, 20.0, num=2))

# Achsen
fig, plot_tx = plt.subplots()
plot_tx.plot(xAchse, spalte_tx, 'o', label="Max Temp. 2m über dem Erdboden")
plt.legend()

# aus xlabel und xlim wird set_xlabel und set_xlim
plot_tx.set_xlabel('Punkte')


# Färben der y-Achse
plot_tx.tick_params('y', colors='g')

# Zeichnen und Anzeige
plt.legend()
plt.show()