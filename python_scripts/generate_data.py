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
        clients.append({
            'client_id': i,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
            'gender': random.choice(['M', 'F']),
            'city': fake.city(),
            'country': fake.country(),
            'numer_of_purchases': random.randint(1,10),
            'total_amount_spent' : round(random.uniform(5.0, 500.0), 2)
        })
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