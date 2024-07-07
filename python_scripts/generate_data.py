import sys
sys.path.append('./libs')
# j'ajoute faker depuis le répértoire du projet pour éviter d'avoir à le réinstaller.


from faker import Faker
import csv
import random
from datetime import datetime, timedelta


fake = Faker()

# faker genere aleatoirement des données cohérentes pour simuler les clients.

def generate_clients(num_clients):
    clients = []
    for i in range(1, num_clients + 1):
        client = {
            'client_id': i,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
            'gender': random.choice(['M', 'F']),
            'city': fake.city(),
            'country': fake.country(),
            # pour être un peu plus dans le thème:
            'rigide_purchased': random.randint(0,9),
            'retro_purchased': random.randint(0,5),
            'original_purchased': random.randint(0,3),
            'calendar_purchased': random.randint(0,2),
            'grand_purchased': random.randint(0,7),
            'magnets_purchased': random.randint(0,15),
            'cadre_purchased': random.randint(0,2),
            }
            #calcul du montant dépensé avec les prix du site.
        client['total_amount_spent'] = (
            35*client['rigide_purchased']
            +10*client['retro_purchased']
            +10*client['original_purchased']
            +15*client['calendar_purchased']
            +20*client['grand_purchased']
            +20*client['magnets_purchased']
            +15*client['cadre_purchased'])

        clients.append(client)
    return clients

# et pour créer le csv qui contient la data
def write_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f'data written in {filename}')


clients = generate_clients(100000)
write_csv('clients.csv', clients)
