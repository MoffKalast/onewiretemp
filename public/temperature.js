var temperature;

class Temperature{

	init(){
		this.data = {};

		let topicsClient = new ROSLIB.Service({
			ros : ros,
			name : '/rosapi/topics',
			serviceType : 'rosapi/Topics'
		});

		topicsClient.callService(new ROSLIB.ServiceRequest(), function(result) {

			for (let i = 0; i < result.topics.length; i++) {
				let name = result.topics[i];
				if(name.startsWith("/temp")){
					let temp_topic = new ROSLIB.Topic({
						ros : ros,
						name : name,
						messageType : 'std_msgs/Float32'
					});

					temp_topic.subscribe(function(msg) {
						temperature.data[name] = msg.data;		
					});
				}
			}
		});

		this.interval = setInterval(Temperature.update, 1000);
	}

	static update(){

		let avgtemp = 0;
		let htmlstring = "";
		let keys = Object.keys(temperature.data).sort();
		for(let i in keys){
			avgtemp += temperature.data[keys[i]];
			let displayname = keys[i].replace("/temp/","").replace("_"," ");
			let val = (Math.round(temperature.data[keys[i]] * 10) / 10).toFixed(1);

			htmlstring +="<h3 style='display:inline-block; margin-right: 10px; text-transform: capitalize;''>"+displayname+": </h3>";
			htmlstring +="<h3 style='display:inline-block;'>"+val+"°C</h3>";
			htmlstring +="<br>";
		}

		avgtemp /= keys.length;

		let img = "hot";

		if(avgtemp < 10){
			img = "unknown";
		}
		else if(avgtemp < 40){
			img = "cold";
		}
		else if(avgtemp < 60){
			img = "nominal";
		}


		document.getElementById("temperature_list").innerHTML = htmlstring;
		document.getElementById("ltemperatureicon").src = "assets/img/temperature/"+img+".svg";
		document.getElementById("ptemperatureicon").src = "assets/img/temperature/"+img+".svg";
	}

}

window.addEventListener('load', function() {
	temperature = new Temperature();
	temperature.init()
});
