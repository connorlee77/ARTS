var connection = "postgres://connor:7777@localhost:5432:/arts";

var Knex = require('knex')({
    client: 'pg',
    connection: {
    	host: '127.0.0.1',
    	user: 'connor',
    	password: '7777',
    	port: '5432',
    	database: 'connor'
    }
});


var bookshelf = require('bookshelf')(Knex);

module.exports = bookshelf.Model.extend({
	tableName: 'arts'
})