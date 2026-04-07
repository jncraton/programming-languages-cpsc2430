const https = require('https');

junk_foods = [
  'Pizza',
  'Popcorn',
  'Hamburger',
  'Pepsi',
  'Potato_chip',
  'Cake',
]

url = 'https://en.wikipedia.org/w/api.php?action=parse&format=json&page='

junk_foods.forEach((food) => {
    console.log("Send request", food)
    https.get({
        host: 'en.wikipedia.org',
        path: '/w/api.php?action=parse&format=json&page=' + food,
        headers: {
              'User-Agent': 'EventsExample/1.0'
            },
    }, function(res) {
        let body = ''
        res.on('data', function(d) {
            body += d
        })
        res.on('end', function() {
            console.log(`${food}: ${JSON.parse(body).parse.properties[0]['*']}`)
        })
    })
})
