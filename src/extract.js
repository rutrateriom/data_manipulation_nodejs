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

            // calcul de l'age à partir de la date de naissance
            const birthDate = new Date(data.birth_date);
            const ageDifMs = Date.now() - birthDate.getTime();
            const ageDate = new Date(ageDifMs);
            data.age = Math.abs(ageDate.getUTCFullYear() - 1970);

            results.push(data);
        })
        .on('end', () => {
            console.log('Nombre de clients:', results.length);

            // CA et depense moyenne
            let totalRevenue = 0;
            for (let i = 0; i < results.length; i++) {
                totalRevenue += results[i].total_amount_spent;
            }
            console.log('CA:', totalRevenue.toFixed(2));
            console.log('Dépense moyenne:', (totalRevenue / results.length).toFixed(2));

            // clients les plus dépenseurs
            let maxSpender = results[0];
            for (let i = 1; i < results.length; i++) {
                if (results[i].total_amount_spent > maxSpender.total_amount_spent) {
                    maxSpender = results[i];
                }
            }
            console.log('Le meilleur client:', maxSpender.first_name, maxSpender.last_name, '-', maxSpender.total_amount_spent);

            // ventes par produit
            let productTotals = {
                rigide: 0,
                retro: 0,
                original: 0,
                calendar: 0,
                grand: 0,
                magnets: 0,
                cadre: 0
            };
            for (let i = 0; i < results.length; i++) {
                productTotals.rigide += results[i].rigide_purchased;
                productTotals.retro += results[i].retro_purchased;
                productTotals.original += results[i].original_purchased;
                productTotals.calendar += results[i].calendar_purchased;
                productTotals.grand += results[i].grand_purchased;
                productTotals.magnets += results[i].magnets_purchased;
                productTotals.cadre += results[i].cadre_purchased;
            }
            console.log('Ventes par produit:', productTotals);

            // produits ayant rapporté le plus
            let productRevenue = {
                rigide: 0,
                retro: 0,
                original: 0,
                calendar: 0,
                grand: 0,
                magnets: 0,
                cadre: 0
            };
            for (let i = 0; i < results.length; i++) {
                productRevenue.rigide += results[i].rigide_purchased * 35;
                productRevenue.retro += results[i].retro_purchased * 10;
                productRevenue.original += results[i].original_purchased * 10;
                productRevenue.calendar += results[i].calendar_purchased * 15;
                productRevenue.grand += results[i].grand_purchased * 20;
                productRevenue.magnets += results[i].magnets_purchased * 20;
                productRevenue.cadre += results[i].cadre_purchased * 15;
            }
            console.log('Contribution au CA par produit:', productRevenue);

            // calcul de l'age ayant le plus acheté
            let ageCounts = {};
            for (let i = 0; i < results.length; i++) {
                if (ageCounts[results[i].age]) {
                    ageCounts[results[i].age]++;
                } else {
                    ageCounts[results[i].age] = 1;
                }
            }
            let maxAge = Object.keys(ageCounts).reduce((a, b) => ageCounts[a] > ageCounts[b] ? a : b);
            console.log('Âge le plus représenté:', maxAge);

            // Calcul du sexe le plus représenté
            let genderCounts = { 'M': 0, 'F': 0 };
            for (let i = 0; i < results.length; i++) {
                if (genderCounts[results[i].gender]) {
                    genderCounts[results[i].gender]++;
                } else {
                    genderCounts[results[i].gender] = 1;
                }
            }
            let maxGender = genderCounts['M'] > genderCounts['F'] ? 'M' : 'F';
            console.log('Sexe le plus représenté:', maxGender);

            // Les 3 pays ayant acheté le plus
            let countryCounts = {};
            for (let i = 0; i < results.length; i++) {
                if (countryCounts[results[i].country]) {
                    countryCounts[results[i].country] += results[i].total_amount_spent;
                } else {
                    countryCounts[results[i].country] = results[i].total_amount_spent;
                }
            }
            let sortedCountries = Object.keys(countryCounts).sort((a, b) => countryCounts[b] - countryCounts[a]);
            let top3Countries = sortedCountries.slice(0, 3);
            console.log('Les 3 pays ayant acheté le plus:', top3Countries);
        });
}

// affichage sur le cmd
const args = minimist(process.argv.slice(2));
const filePath = args.file || 'clients.csv';

extractData(filePath);
