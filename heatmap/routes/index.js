var express = require('express');
var router = express.Router();
var _ = require('underscore');

var knex = require('knex')({
    client: 'pg',
    connection: {
    	host: 'ec2-54-225-100-236.compute-1.amazonaws.com',
    	user: 'cwlsijpetpmljf',
    	password: 'jrU8kUKuU7AdBzyDjqHyVGBaBt',
    	port: '5432',
    	database: 'd3bkl6mc1pdi72'
    }
});

/*var knex = require('knex')({
    client: 'pg',
    connection: {
    	host: 'localhost',
    	user: 'connor',
    	password: '7777',
    	port: '5432',
    	database: 'connor'
    }
});*/

/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('index', { title: 'Pasadena ARTS' });
});

router.get('/test', function(req, res, next) {
	console.log(req.query['items']);

	if ((req.query['items'] == [] || req.query['items'] === undefined) && (req.query['start'] === undefined || req.query['start'] === '')) {
		res.send([]);
		return;
	}
	// Buttons
	var rawQuery = '';

	if (req.query['items'] == [] || req.query['items'] === undefined) {

		if(req.query['start'] !== undefined && req.query['start'] !== '') {
			rawQuery = 'SELECT COUNT(*), arts.station FROM arts WHERE   ';
		}

	} else if(req.query['items'].length > 0){
		rawQuery = 'SELECT COUNT(*), arts.station FROM arts WHERE (';
	}


	var tempQuery = '';
	_.each(req.query['items'], function(item) {
		tempQuery = " arts.fareproduct = \'" + item + '\' or';
		rawQuery += tempQuery; 
	});

	if (tempQuery === '') {
		rawQuery = rawQuery.substring(0, rawQuery.length - 2);
	} else {
		rawQuery = rawQuery.substring(0, rawQuery.length - 2) + ') ';
	} 

	// Time
	var start = req.query['start'];
	var end = req.query['end'];

	tempQuery = '';
	if(start != '' && end != '' && start != undefined && end != undefined) {
		tempQuery = " (arts.tapdate::time >= " + '\'' + start + '\'' + " and arts.tapdate::time <=" + '\'' + end + '\''  + ') ';
	} 

	if (req.query['items'] == [] || req.query['items'] === undefined) {
		rawQuery += tempQuery;
	} else if(req.query['items'].length > 0 && tempQuery != ''){
		rawQuery += ' AND ' + tempQuery;
	}
	
	
	rawQuery += 'GROUP BY arts.station';
	console.log(rawQuery);

    knex.schema.raw(rawQuery).then(function(resp) {
    	res.send(resp);
    });
});

module.exports = router;
