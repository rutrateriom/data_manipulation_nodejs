const fs = require('fs');
const csv = require('csv-parser');
const minimist = require('minimist');

function extractData(filePath) {
    const results = [];

    fs.createReadStream(filePath)
        .pipe(csv())
        .on('data', (data) => {
            data.total_amount_spent = parseFloat(data.total_amount_spent);
            data.rigide_purchased = parseInt(data.rigide_purchased, 10);
            data.retro_purchased = parseInt(data.retro_purchased, 10);
            data.original_purchased = parseInt(data.original_purchased, 10);
            data.calendar_purchased = parseInt(data.calendar_purchased, 10);
            data.grand_purchased = parseInt(data.grand_purchased, 10);
            data.magnets_purchased = parseInt(data.magnets_purchased, 10);
            data.cadre_purchased = parseInt(data.cadre_purchased, 10);

            // Calculer l'âge
            const birthDate = new Date(data.birth_date);
            const ageDifMs = Date.now() - birthDate.getTime();
            const ageDate = new Date(ageDifMs);
            data.age = Math.abs(ageDate.getUTCFullYear() - 1970);

            results.push(data);
        })
        .on('end', () => {
            console.log('Nombre de clients:', results.length);

            // CA et dépense moyenne
            let totalRevenue = 0;
            results.forEach(client => {
                totalRevenue += client.total_amount_spent;
            });
            console.log('CA:', totalRevenue.toFixed(2));
            console.log('Dépense moyenne:', (totalRevenue / results.length).toFixed(2));

            // Clients les plus dépenseurs
            let maxSpender = results[0];
            results.forEach(client => {
                if (client.total_amount_spent > maxSpender.total_amount_spent) {
                    maxSpender = client;
                }
            });
            console.log('Le meilleur client:', maxSpender.first_name, maxSpender.last_name, '-', maxSpender.total_amount_spent);

            // Ventes par produit
            let productTotals = {
                rigide: 0,
                retro: 0,
                original: 0,
                calendar: 0,
                grand: 0,
                magnets: 0,
                cadre: 0
            };
            results.forEach(client => {
                productTotals.rigide += client.rigide_purchased;
                productTotals.retro += client.retro_purchased;
                productTotals.original += client.original_purchased;
                productTotals.calendar += client.calendar_purchased;
                productTotals.grand += client.grand_purchased;
                productTotals.magnets += client.magnets_purchased;
                productTotals.cadre += client.cadre_purchased;
            });
            console.log('Ventes par produit:', productTotals);

            // Produits ayant rapporté le plus
            let productRevenue = {
                rigide: 0,
                retro: 0,
                original: 0,
                calendar: 0,
                grand: 0,
                magnets: 0,
                cadre: 0
            };
            results.forEach(client => {
                productRevenue.rigide += client.rigide_purchased * 35;
                productRevenue.retro += client.retro_purchased * 10;
                productRevenue.original += client.original_purchased * 10;
                productRevenue.calendar += client.calendar_purchased * 15;
                productRevenue.grand += client.grand_purchased * 20;
                productRevenue.magnets += client.magnets_purchased * 20;
                productRevenue.cadre += client.cadre_purchased * 15;
            });
            console.log('Contribution au CA par produit:', productRevenue);

            // Calcul de l'âge le plus représenté
            let ageCounts = {};
            results.forEach(client => {
                if (ageCounts[client.age]) {
                    ageCounts[client.age]++;
                } else {
                    ageCounts[client.age] = 1;
                }
            });
            let maxAge = Object.keys(ageCounts).reduce((a, b) => ageCounts[a] > ageCounts[b] ? a : b);
            console.log('Âge le plus représenté:', maxAge);

            // Calcul du sexe le plus représenté
            let genderCounts = { 'M': 0, 'F': 0 };
            results.forEach(client => {
                if (genderCounts[client.gender]) {
                    genderCounts[client.gender]++;
                } else {
                    genderCounts[client.gender] = 1;
                }
            });
            let maxGender = genderCounts['M'] > genderCounts['F'] ? 'M' : 'F';
            console.log('Sexe le plus représenté:', maxGender);

            // Les 3 pays ayant acheté le plus
            let countryCounts = {};
            results.forEach(client => {
                if (countryCounts[client.country]) {
                    countryCounts[client.country] += client.total_amount_spent;
                } else {
                    countryCounts[client.country] = client.total_amount_spent;
                }
            });
            let sortedCountries = Object.keys(countryCounts).sort((a, b) => countryCounts[b] - countryCounts[a]);
            let top3Countries = sortedCountries.slice(0, 3);
            console.log('Les 3 pays ayant acheté le plus:', top3Countries);
        });
}

// Affichage sur le cmd
const args = minimist(process.argv.slice(2));
const filePath = args.file || 'clients.csv';

extractData(filePath);
