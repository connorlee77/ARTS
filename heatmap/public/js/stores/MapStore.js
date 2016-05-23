var Reflux  = require('reflux');
var $       = require('jquery');
var _       = require('underscore');
var actions = require('../actions/MapActions');


module.exports = Reflux.createStore({

	attributes: {
		items: [],
		time: '',
		date: ''
	},

	init: function() {
		this.listenToMany(actions);
	}, 

	onButtonClicked: function(item) {
		var obj = this;

		var i = obj.attributes['items'].indexOf(item);

		if(i >= 0) {
			obj.attributes['items'].splice(i, 1 );
		} else {
			obj.attributes['items'].push(item);
		}

		// Ajax call
		$.get({
			url: 'test',
			data: obj.attributes,
			success: function(data) {
				if(data != null || data != '' || data != []) {
					obj.trigger(data)
				}
			}
		});
	}, 

	onDateEntered: function(d) {
		var obj = this;
		obj.attributes['Date'] = d;

		$.get({
			url: 'https://pasadena-area-transport-system.herokuapp.com',
			data: obj.attributes,
			success: function(data) {
				if(data != null) {
					obj.trigger(data)
				}
			}
		});
	}, 

	onTimeEntered: function(Time) {
		var obj = this;
		obj.attributes['time'] = Time;

		$.get({
			url: 'https://pasadena-area-transport-system.herokuapp.com',
			data: obj.attributes,
			success: function(data) {
				if(data != null) {
					obj.trigger(data)
				}
			}
		});
	}
});