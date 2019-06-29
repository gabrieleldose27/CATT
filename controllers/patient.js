let db = require('../schema');

module.exports.getAll = async (req, res, next) => {
  let result = new Promise((resolve, reject) => {
    db.find({}, (err, patients) => {
      if (err) {
        reject(err);
      } else {
        resolve(patients);
      }
    });
  });
  result.then(patients => {
    res.render('../views/index', {patients: patients});
  }).catch(err => {
    console.err(err);
  })
}
module.exports.update = async (req, res, next) => {
  console.log(req.body, req.file);
  let result = new Promise((resolve, reject) => {
    db.update({bed: req.body.bed}, {
        temperature: 37.2,
        filePath: req.file.originalname
      }, {}, (err) => {
      if (err) {
        reject(err);
      } else {
        resolve(true);
      }
    });
  });
  result.then(res => {
    res.redirect('/');
  }).catch(err => {
    console.log(err);
  });
}
module.exports.create = async (req, res, next) => {
  console.log(req.body, req.file);
  let result = new Promise((resolve, reject) => {
    db.insert(req, (err, res) => {
      if (err) {
        reject(err);
      } else {
        resolve(res);
      }
    });
  });
  result.then(res => {
    res.redirect('/');
  }).catch(err => {
    console.log(err);
  });
}
