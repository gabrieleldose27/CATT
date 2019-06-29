const Datastore = require('nedb');

let db = new Datastore({
  filename: 'database/catt.db',
  autoload: true
});
let patients = [
  {fullName: 'Khettat Brahim', age: 10, bed: 1, temperature: 37.2},
  {fullName: 'Nezli Amara', age: 12, bed: 2, temperature: 38.5}
];
module.exports = db;
