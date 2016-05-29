var Reflux  = require('reflux');
var $       = require('jquery');
var _       = require('underscore');
var actions = require('../actions/MapActions');
var moment  = require('moment');
moment().format();


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

	onTimeEntered: function(Time1, Time2) {
		var obj = this;

		obj.attributes['start'] = Time1;
		obj.attributes['end'] = Time2

		$.get({
			url: 'test',
			data: obj.attributes,
			success: function(data) {
				if(data != null || data != '' || data != []) {
					obj.trigger(data)
				}
			}
		});
	}
});