//Javascript to submit the form and print appropriate response
//Written by: Somanshu Kalra
//Date: 14th November 2019


$(document).ready(function() {

//Clear textArea upon reload of application
$('#functionTextArea').val('');


//Function to load example 1
$('#example1').click(function(){
	$('#example1').parent().addClass('active');
	$('#example2').parent().removeClass('active');
	$('#example3').parent().removeClass('active');
	$('#example4').parent().removeClass('active');
	$('#functionTextArea').val(example1);
});

//Function to load example 2
$('#example2').click(function(){
	$('#example1').parent().removeClass('active');
        $('#example2').parent().addClass('active');
        $('#example3').parent().removeClass('active');
        $('#example4').parent().removeClass('active');

        $('#functionTextArea').val(example2);
});


//Function to load example 3
$('#example3').click(function(){
	$('#example1').parent().removeClass('active');
        $('#example2').parent().removeClass('active');
        $('#example3').parent().addClass('active');
        $('#example4').parent().removeClass('active');

        $('#functionTextArea').val(example3);
});


//Function to load example 4
$('#example4').click(function(){
	$('#example1').parent().removeClass('active');
        $('#example2').parent().removeClass('active');
        $('#example3').parent().removeClass('active');
        $('#example4').parent().addClass('active');
        $('#functionTextArea').val(example4);
});

//Function to make API call
function sendData(e) {
var output = [];
var vulnerability = [];
 var xhr = new XMLHttpRequest();
 xhr.open("POST", "http://203.101.226.215");  //Send the proper header information along with the request
 xhr.setRequestHeader("Content-Type", "application/text");  
xhr.onreadystatechange = function() {
   // Call a function when the state changes.
   if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
     // Request finished.
	var json_response = jQuery.parseJSON(event.target.responseText);
	$.each(json_response, function(key,value){
	jsonObject = [];
	$.each(value, function(key1,value1){
		jsonObject.push(key1 + ":" + value1)
		vulnerability.push(key1);
})
	output.push(key + '\n' + jsonObject.join(''));
});


$('#vulnerabilityTextArea').val(output.join("\n"));
$('#information-alert').hide();
$('#success-alert').show();
	console.log(vulnerability);
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
	}
     setTimeout(function(){ $('#success-alert').hide(); }, 4000);
   }if(this.status !== 200 ){
	$('#information-alert').hide();
	$('#danger-alert').show();
	setTimeout(function(){ $('#danger-alert').hide();}, 4000);
}

 };  var functions = document.getElementById("functionTextArea");
 xhr.send(functions.value);
$('#information-alert').show();
}
 var form = document.getElementById("static-analysis-form");
 // ...and take over its submit event.
 form.onsubmit = function(e) {
e.preventDefault();
$('#cwe-120').hide();
$('#cwe-119').hide();
$('#cwe-469').hide();
$('#cwe-476').hide();
   sendData();
 };
});
