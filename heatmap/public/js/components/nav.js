var $     = require('jquery');
var _     = require('underscore');
var React = require('react');
var ReactDOM = require('react-dom');
require('bootstrap');


var Nav = React.createClass({
	render: function() {
		return (
			<div className='navbar navbar-default'>
				<div className='container-fluid'>
					<div className='navbar-header'>
						<a className='navbar-brand'>Pasadena ARTS</a>
					</div>
				</div>
			</div>
		);
	}
});

ReactDOM.render(
	<Nav/>,
	document.getElementById('nav')
);