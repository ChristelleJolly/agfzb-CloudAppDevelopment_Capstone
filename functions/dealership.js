/**
 * Get all dealerships
 * Possible params : State or Id
 */

 const Cloudant = require('@cloudant/cloudant');

 function main(params) {
 
     const cloudant = Cloudant({
         url: params.COUCH_URL,
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
     });
 
     if (params.id) {
          return getDocById(cloudant, params.id);
     }
     if (params.state) {
         return getDocsByState(cloudant, params.state);
     }
     return getDocs(cloudant);
 }
 
 function getDocs(cloudant) {
     return new Promise((resolve, reject) => {
         var db = cloudant.db.use('dealerships')
         db.list({
           include_docs: true,
         }).then(body => {
                 resolve(body);
             })
             .catch(err => {
                 reject({ err: err });
             });
     });
 }
 
 function getDocsByState(cloudant, state) {
     return new Promise((resolve, reject) => {
         var db = cloudant.db.use('dealerships')
         db.find({
           selector: {st:state},
         }).then(body => {
                 resolve(body);
             })
             .catch(err => {
                 reject({ err: err });
             });
     });
 }
 
 function getDocById(cloudant, id) {
     return new Promise((resolve, reject) => {
         var db = cloudant.db.use('dealerships')
         db.get(id
         ).then(body => {
                 resolve({ dealership: body });
             })
             .catch(err => {
                 reject({ err: err });
             });
     });
     
 }