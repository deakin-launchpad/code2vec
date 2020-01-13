//Javascript to submit the form and print appropriate response
//Written by: Somanshu Kalra
//Date: 14th November 2019


$(document).ready(function() {

//Clear textArea upon reload of application
$('#clause').val('');


//Function to load example 1
$('#airbnb').click(function(){
	$('#airbnb').parent().addClass('active');
	$('#apple').parent().removeClass('active');
	$('#facebook').parent().removeClass('active');
	$('#amazon').parent().removeClass('active');
	$('#clause').val(airbnb);
});

//Function to load example 2
$('#facebook').click(function(){
	$('#airbnb').parent().removeClass('active');
        $('#facebook').parent().addClass('active');
        $('#amazon').parent().removeClass('active');
        $('#apple').parent().removeClass('active');

        $('#clause').val(facebook);
});


//Function to load example 3
$('#amazon').click(function(){
	$('#airbnb').parent().removeClass('active');
        $('#facebook').parent().removeClass('active');
        $('#amazon').parent().addClass('active');
        $('#apple').parent().removeClass('active');

        $('#clause').val(amazon);
});


//Function to load example 4
$('#apple').click(function(){
	$('#airbnb').parent().removeClass('active');
        $('#facebook').parent().removeClass('active');
        $('#amazon').parent().removeClass('active');
        $('#apple').parent().addClass('active');
        $('#clause').val(apple);
});

//Function to make API call
function sendData(e) {
var output = [];
var vulnerability = [];
 var xhr = new XMLHttpRequest();
 xhr.open("POST", "http://203.101.226.215/clauseAnalysis");  //Send the proper header information along with the request
 xhr.setRequestHeader("Content-Type", "application/text");  
xhr.onreadystatechange = function() {
   // Call a function when the state changes.
   if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
     // Request finished.
	var json_response = jQuery.parseJSON(event.target.responseText);
	console.log(json_response)
	$.each(json_response, function(key,value){
		$.each(value, function(key1, value1){
			output += key1 + " : " + value1 + "\n\n"
	});
			output += "\n"
});


$('#compliance').val(output);
$('#information-alert').hide();
$('#success-alert').show();
	console.log(vulnerability);
/*
	if(vulnerability.indexOf("CWE-120 ") !== -1){
		$('#cwe-120').show();
	}
	if(vulnerability.indexOf("CWE-119 ") !== -1){
		$('#cwe-119').show();
	}
	if(vulnerability.indexOf("CWE-469 ") !== -1){
		$('#cwe-469').show();
	}
	if(vulnerability.indexOf("CWE-476 ") !== -1){
		$('#cwe-476').show();
	}*/
     setTimeout(function(){ $('#success-alert').hide(); }, 4000);
   }if(this.status !== 200 ){
	$('#information-alert').hide();
	$('#danger-alert').show();
	setTimeout(function(){ $('#danger-alert').hide();}, 4000);
}

 };  var functions = document.getElementById("clause");
 xhr.send(functions.value);
$('#information-alert').show();
}
 var form = document.getElementById("clause-analysis-form");
 // ...and take over its submit event.
$( "#submit-button" ).click(function() {
  $( "#clause-analysis-form" ).submit();
});

 form.onsubmit = function(e) {
e.preventDefault();
$('#full-information').hide();
$('#insufficient-information').hide();
$('#unclear-language').hide();
$('#problematic-processing').hide();
   sendData();
 };
});
