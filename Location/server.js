const express = require('express')
const app = express()
const mysql = require('mysql')
var bodyParser = require('body-parser');

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({extended:true}))
app.use(express.static('./template'));
// const cors = require('cors')
// app.use(cors());

function dbResult(results) {
    var positions = []
    
    for (var i = 0; i < results.length; i++) {
        positions[i] = {title: results[i].businessName,latLng: (results[i].latitude,results[i].longitude)}
    }
    console.log(positions[0].title,positions[0].latLng)
}
// Database connection
const db = mysql.createConnection({
    host: "127.0.0.1",
    user: "root",
    password: "제출용이라 가렸습니다.",
    database: "CommercialAreaInformation"
})

db.connect(function (err) {
    if (err) {
        return console.error('error: ' + err.message);
    }
    console.log('Connected to the MySQL server.');
})

app.post('/big', function(req,res) {
    let { lat, lon, categoryVal} = req.body 
    console.log(lat, lon, categoryVal)
    db.query(`SELECT businessName, latitude, longitude, highCategoryName, (6371*acos(cos(radians(${lat}))*cos(radians(latitude))*cos(radians(longitude)-radians(${lon}))+sin(radians(${lat}))*sin(radians(latitude)))) AS distance FROM CommercialAreaInformation HAVING distance <= 1 AND highCategoryName = '${categoryVal}' ORDER BY distance;`,
    function (error, results, fields) {
       if (error) throw error;
       // console.log('The solution is: ', results.businessName);
       // console.log(results[0].businessName)
    //    console.log(results);
       res.json(results);
    });

    
    
})

//create connection
const PORT = process.env.PORT || 5500
app.listen(PORT, () => console.log(`Server is running at port ${PORT}`))