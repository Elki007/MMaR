import numpy as np
import matplotlib.pyplot as plt

#tabelle = np.genfromtxt("wetterdaten.txt", skip_header=3, missing_values=('nan'))
#tabelle = np.loadtxt("wetterdaten.txt", skiprows=3)

tabelle = np.loadtxt("wetterdaten2.txt", delimiter=';',skiprows=1, usecols=np.arange(15))
#tabelle = tabelle[0:5,:]

#print(tabelle)


spalte_tx = tabelle[:,6]
spalte_rr = tabelle[:,14]
xAchse = np.arange(len(spalte_rr))

# Achsen
fig, plot_tx = plt.subplots()
plot_tx.plot(xAchse, spalte_tx, 'b-', label="Max Temp. 2m über dem Erdboden")
plt.legend()
# aus xlabel und xlim wird set_xlabel und set_xlim
plot_tx.set_xlabel('Punkte')

# Färben der y-Achse
plot_tx.tick_params('y', colors='b')

# zweite y-Achse (mit der gleichen x-Achse)
plot_rr = plot_tx.twinx()
plot_rr.plot(xAchse, spalte_rr, 'g-', label="Niederschlagsmenge")

plot_rr.tick_params('y', colors='g')

# Zeichnen und Anzeige
#plt.plot(xAchse, spalte_tx, '.')
#plt.plot(xAchse, spalte_rr, '--')
plt.legend()
plt.show()
