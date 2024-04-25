import pandas as pd
from dimod import BinaryQuadraticModel
from dwave.system.composites import EmbeddingComposite
from dwave.system.samplers import DWaveSampler
import dwave.inspector as inspector

# Lire le fichier CSV avec un délimiteur de point-virgule
data = pd.read_csv('Qubo_4valeurs.csv', delimiter=';')

# Extraire les colonnes de poids et de valeurs
values = data.iloc[:, 0].values
weights = data.iloc[:, 1].values

# CALCUL DU POIDS TOTAL MAXIMUM
max_weight = 0
for i in range(len(weights)):
    max_weight += weights[i]

# Créer un modèle quadratique binaire
bqm = BinaryQuadraticModel('BINARY')

# Ajouter les variables binaires au modèle
for i in range(len(values)):
    bqm.add_variable(i, -values[i])

# Ajouter une contrainte linéaire
bqm.add_linear_inequality_constraint(
    [(i, weight) for i, weight in enumerate(weights)], constant=0, lagrange_multiplier=max_weight, ub=10, lb=0, label='')



# Utiliser un sampler D-Wave
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample(bqm, num_reads=1000)

# Afficher les résultats
best_solution = response.first.sample
best_energy = response.first.energy

print("Meilleure solution:", best_solution)
print("Meilleure énergie:", best_energy)

# Afficher la valeur totale et le poids total de la meilleure solution
total_value = sum(values[i] for i in range(len(values)) if best_solution[i] == 1)
total_weight = sum(weights[i] for i in range(len(values)) if best_solution[i] == 1)
print("Valeur totale:", total_value)
print("Poids total:", total_weight)

# Afficher l'inspecteur D-Wave
inspector.show(response)



