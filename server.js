const patient = require('./controllers/patient.js');
const express = require('express');
const multer  = require('multer');
const bodyParser = require('body-parser');

let app = express();

app.set('views', './views');
app.set('view engine', 'pug');

app.use(express.static('public'));
app.use('/static', express.static(__dirname + '/public'));

app.use(bodyParser.json({limit: '100mb', extended: true}));
app.use(bodyParser.urlencoded({limit: '100mb', extended: true}));

app.use((req, res, next) => {
  console.log('Requesting: ['+req.method+']:\t'+req.originalUrl);
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

let storage = multer.diskStorage({
    destination: (req, file, next) => {
        next(null, 'public/uploads/')
    },
    filename: (req, file, next) => {
        next(null, file.originalname)
  }
})

let upload = multer({ storage: storage })

app.get('/', patient.getAll);
app.post('/', upload.single('photo'), patient.update);


app.listen(31415, '0.0.0.0', () => {
  console.log('Listning...')
});
