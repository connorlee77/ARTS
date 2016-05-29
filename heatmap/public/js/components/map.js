var $        = require('jquery');
var _        = require('underscore');
var React    = require('react');
var ReactDOM = require('react-dom');
var Reflux   = require('reflux');
var MapStore = require('../stores/MapStore');
var Actions  = require('../actions/MapActions');
var latlng   = require('./latlng');
var moment   = require('moment');
moment().format();
require('bootstrap');


var Selector = React.createClass({

	handleClick: function(event) {
		Actions.buttonClicked(this.props.label);
	},

	render: function() {
		return (
			<label className="btn btn-default" onClick={this.handleClick}>
				<input type="checkbox" autocomplete='off'></input>{this.props.label}
			</label>
		);
	}
});


var DateRange = React.createClass({

	getInitialState: function() {
		return {
			dateRange :'',
			timeRange: ''
		}
	},

	componentDidMount: function() {
		$('.ok').hide();
	},

	handleTimeChange: function() {
		var inputValue = this.refs.timeRange.value;

		times = inputValue.split('-');
		$('.ok').hide()

		var validate = "HH:mm:ss";
		var start = moment($.trim(times[0]), validate, true);
		var end = moment($.trim(times[1]), validate, true);

		if((start.isValid() && end.isValid()) || times == '') {
			
			if (times == '') {
				Actions.timeEntered('', '');
			} else {
				Actions.timeEntered(
					$.trim(times[0]), 
					$.trim(times[1]));
				$('.ok').show()
			}
		}
	},

	render: function() {
		return (
			<div>
				<div className='input-group ranges'>
					<span className="sr-only" for="timeRange">Time Range</span>
					<input type="text" ref='timeRange' className="form-control" id="timeRange" placeholder="Time range: ex. 9:00:00 - 14:00:00" onChange= {this.handleTimeChange}></input>
					<span className='ok'></span>
				</div>
			</div>
		);
	}
});


var Form = React.createClass({


	render: function() {

		var buttonLabels = ['Reg SV College', 'PS CTW', 'EZ Pass S/D Z2', 'EZ Pass S/D Z3', 'EZ Pass S/D Z0', 'EZ Pass S/D Z1', 'PS Try Tran Mon', 'DCFS EZ (New)', 'EZ PassS/D Repl', 'Reg SV Student', 'EZ Annual Z0', 'EZ Annual Z1', 'EZ Annual Z5', 'Reg Senior 60', 'EZ Pass AdultZ1', 'EZ Pass AdultZ0', 'EZ Pass AdultZ2', 'ASI', 'EZ Pass AD Repl', 'Reg SV Sr/Dis', 'Reg SV Regular'];

		return (
			<div className='row' id='selectors'>
				<div className='col-md-'>
					
					<DateRange/>
					
					<div className='btn-group' data-toggle="buttons">
						{buttonLabels.map(function(txt) {
							return <Selector key={txt} label={txt}/>;
						})}
					</div>
				</div>

				

			</div>
		);
	}
});

var Heatmap = React.createClass({

	mixins: [Reflux.listenTo(MapStore,"onStateChange")],

	onStateChange: function(resp) {

		var env = this;
		
		// env.setMapOnAll(null);
		// env.markers = [];

		if (env.heatmap != undefined) {
			env.heatmap.setMap(null);
		}

		var heatmapData = [];
		_.each(resp.rows, function(obj) {

			var count = obj.count;
			var address = obj.station;
			
			if (address in latlng) {
				var lat = latlng[address][0];
				var lng = latlng[address][1];

				// var marker = new google.maps.Marker({
				// 	map: env.map,
				// 	position: {
				// 		lat: lat,
				// 		lng: lng
				// 	}
				// });
				// env.markers.push(marker);

				for (var i = 0; i < count; i++) {
					heatmapData.push(new google.maps.LatLng(lat + Math.random() * 0.001, lng + Math.random() * 0.001));
				}
			}
		});

		env.heatmap = new google.maps.visualization.HeatmapLayer({
			data: heatmapData
		});

		env.heatmap.setMap(env.map);
		env.heatmap.set('radius', env.heatmap.get('radius') ? null : 20);
	},

	setMapOnAll: function(map) {
		for (var i = 0; i < this.markers.length; i++) {
	    	this.markers[i].setMap(map);
	  	}
	},

	componentDidMount: function() {
		// this.markers = [];
		this.map = new google.maps.Map($('#heatmap')[0], {
			center: {
				lat: 34.149885, 
				lng: -118.145605
			},
			mapTypeId: google.maps.MapTypeId.HYBRID,
			zoom: 14
		});

	},

	render: function() {
		return (
			<div id='heatmap'></div>
		);
	}

});

var MapContainer = React.createClass({

	render: function() {
		return (

			<div className='row'>
				<div className='col-md-12'>
					<Form/>
				</div>
				<div className='col-md-12'> 
					<Heatmap/>
				</div>

				
			</div>

		);
	}
});

ReactDOM.render( <MapContainer/>, $('#map')[0]);

