import pandas as pd

def csv_to_lp(input_csv, output_lp):
    # Charger les données du fichier CSV avec pandas en spécifiant le séparateur
    df = pd.read_csv(input_csv, sep=';', header=None)

    # Ouvrir le fichier LP en mode écriture
    with open(output_lp, 'w') as lp_file:
        # Écrire l'en-tête du fichier LP
        lp_file.write("Maximize\n")
        lp_file.write("   ")

        # Écrire la fonction objective
        first_term = 1  # Pour suivre le premier terme
        for index, row in df.iterrows():
            if row == 0:
                row += 1
                first_term = 2
            if first_term == 2:
                lp_file.write(" + ")
            else:
                first_term = 1
            lp_file.write("{} x{}".format(row[0], index+1))
        lp_file.write("\n")

        # Écrire les contraintes
        lp_file.write("Subject To\n")
        lp_file.write("   ")
        first_term = 1  # Pour suivre le premier terme
        for index, row in df.iterrows():
            if row == 0:
                row += 1
                first_term = 2
            if first_term == 2:
                lp_file.write(" + ")
            else:
                first_term = 1
            lp_file.write("{} x{}".format(row[1], index+1))
        lp_file.write(" <= 10\n")

        # Écrire la déclaration des variables
        lp_file.write("Binary\n")
        for index in range(1, len(df) + 1):
            lp_file.write(" x{}\n".format(index))

        # Écrire la déclaration de l'end
        lp_file.write("End\n")

# Appeler la fonction avec le nom de votre fichier CSV d'entrée et le fichier LP de sortie
csv_to_lp('Qubo_4valeurs.csv', 'knapsack.lp')
