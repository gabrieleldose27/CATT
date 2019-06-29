const Datastore = require('nedb');

let db = new Datastore({
  filename: 'database/catt.db',
  autoload: true
});
let patients = [
  {fullName: 'Nezli Amara', age: 12, bed: 2, temperature: 38.5}
];

module.exports = db;
