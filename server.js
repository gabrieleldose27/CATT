var express = require('express');

var app = express();

app.set('views', './views');
app.set('view engine', 'pug');

app.use(express.static('public'));
app.use('/static', express.static(__dirname + '/public'));

app.get('/', function(req, res) {
  res.render('index')
});


app.listen(31415, () => {
  console.log('Listning...')
});
