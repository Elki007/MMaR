import numpy as np
import matplotlib.pyplot as plt

# Tabelle aus Datei lesen
tabelle = np.loadtxt("wetterdaten2.txt", delimiter=';',skiprows=1, usecols=np.arange(15))

# 2 Spalten der Tabelle zuweisen
spalte_tx = tabelle[:,6]
spalte_rr = tabelle[:,14]

# x-Achse von Zeilenanzahl abhängig machen
xAchse = np.arange(len(spalte_rr))

# Achsen
fig, plot_tx = plt.subplots()
plot_tx.plot(xAchse, spalte_tx, 'b-', label="Max Temp. 2m über dem Erdboden")

# Legende darstellen
# ! was fehlt, um beide Labels in einer Legende darzustellen?
plt.legend()

# aus xlabel und xlim wird set_xlabel und set_xlim
# ! Wozu ist diese Zeile?
plot_tx.set_xlabel('Punkte')

# zweite y-Achse (mit der gleichen x-Achse)
plot_rr = plot_tx.twinx()
plot_rr.plot(xAchse, spalte_rr, 'g-', label="Niederschlagsmenge")

# Färben der y-Achsen
plot_tx.tick_params('y', colors='b')
plot_rr.tick_params('y', colors='g')

# Zeichnen und Anzeige
#plt.plot(xAchse, spalte_tx, '.')
#plt.plot(xAchse, spalte_rr, '--')
plt.legend()
plt.show()

# ! Wozu diese Zeile?
x= np.linspace(3, 9, 10)
