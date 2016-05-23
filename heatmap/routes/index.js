var express = require('express');
var router = express.Router();
var trip = require('./arts');
var _ = require('underscore');

var knex = require('knex')({
    client: 'pg',
    connection: {
    	host: '127.0.0.1',
    	user: 'connor',
    	password: '7777',
    	port: '5432',
    	database: 'connor'
    }
});

/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('index', { title: 'Pasadena ARTS' });
});

router.get('/test', function(req, res, next) {

	if (req.query['items'] == undefined) {
		res.status(200).send([]);
		return;
	}

	var rawQuery = 'SELECT COUNT(*), arts.station FROM arts WHERE';

	_.each(req.query['items'], function(item) {
		var tempQuery = " arts.fareproduct = \'" + item + '\' or';
		rawQuery += tempQuery; 
	});

	rawQuery = rawQuery.substring(0, rawQuery.length - 2);

/*	var time = req.query['time'] 
	if(req.query['time'] != '') {

		var time = time.split(' - ');
		console.log(time);
		var tempQuery = " (arts.tapdata >= " + time[0] + " and arts.tapdata <=" + time[1] + ')'
	}

	if(req.query['date'] != '') {
		
	}*/
	rawQuery += 'GROUP BY arts.station'
	console.log(rawQuery);

    knex.schema.raw(rawQuery).then(function(resp) {
    	res.send(resp);
    });
});

module.exports = router;
