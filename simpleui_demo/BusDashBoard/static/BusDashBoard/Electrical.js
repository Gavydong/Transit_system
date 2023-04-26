

eletrical_init_menu()


var bus_info = {
  
    "BYD K9":{
     Battery_capacity :"324 kWh",
     Max_passengers: "37",
     Max_speed: "100.584 km/h",
     Weight: "43,431 lbs",
     Charging_Time : "2-3 hrs"
    },
    "Volvo 7900 12m":{
     Battery_capacity :"470 kWh",
     Max_passengers: "38",
     Max_speed: "50 kw/h",
     Weight: "41,887.83 lbs",
     Charging_Time : "2-3 hrs"
    },
    "Proterra ZX5":{
 
     Battery_capacity :"220 kWh",
     Max_passengers: "40",
     Max_speed: "104.6 kw/h",
     Weight: "26,649 lbs",
     Charging_Time : "2.9 hrs"
    }
 
 
 
 }


$("#buses_id li").click(function() {

    console.log("Clicking on selection of buses")
        
    var button = document.getElementById("dropdown_button")
    var id = $(this).attr("id");
    button.innerHTML = id;


   console.log("Filling the textfields")
    var id = $(this).attr("id");
    console.log(id)

    var input = document.getElementsByClassName('my_input-d')
    console.log(input)

    if(id.toString() == "BYD K9") {
      input[0].value = "324 Kwh"
      input[1].value = "37"
      input[2].value = "100.84 km/h"
      input[3].value = " 43,431 Ibs"
      input[4].value = "2-3 hrs"

      
      document.getElementById("Bus-icon").src = "https://www.electrive.com/wp-content/uploads/2018/08/byd-k9-electric-bus-elektrobus-usa-canada.png"

    } else if(id.toString() == "Volvo 7900")
    {
      input[0].value = "470 kwh"
      input[1].value = "38"
      input[2].value = "50 kw/h"
      input[3].value = "41, 887.83 Ibs"
      input[4].value = "2-3 hrs"

      document.getElementById("Bus-icon").src = "https://electriccarsreport.com/wp-content/uploads/2015/09/Volvo-7900-Electric.jpg"


    } else if(id.toString() == "Proterra ZX5"){

      input[0].value = "220kwh"
      input[1].value = "40"
      input[2].value = "104.6 kw/h"
      input[3].value = "26,649 Ibs"
      input[4].value = "2.9 hrs"

      
      document.getElementById("Bus-icon").src = "https://www.sustainable-bus.com/wp-content/uploads/2020/09/ZX5_40_PRODUCT-PAGE.jpg"

    }


    
    



 });


function eletrical_init_menu(){
  var button = document.getElementById("dropdown_button")

  button.innerHTML = "BYD K9";
 
  var input = document.getElementsByClassName('my_input-d')
 
  input[0].value = "324 Kwh"
  input[1].value = "37"
  input[2].value = "100.84 km/h"
  input[3].value = " 43,431 Ibs"
  input[4].value = "2-3 hrs"
}