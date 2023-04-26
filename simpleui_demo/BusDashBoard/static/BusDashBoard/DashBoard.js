
console.log("I am active")

var element = document.getElementById("liquid-fuel-buses");
console.log("Here..")
console.log(element)
element.classList.remove("item")
element.classList.add("item-active")
$("#Content_switch_screen").load("Electrical");







$("#bus_menu li").click(function() {

  var fuel_buses = document.getElementById("liquid-fuel-buses");
  var elect_buses = document.getElementById("Electrical-buses");

  console.log(this)
  var id = $(this).attr("id");
  
  if("Electrical-buses" == id.toString())
   {
     console.log("Electrical bus")

     $("#Content_switch_screen").load("Electrical");

     elect_buses.classList.remove("item-active")
     elect_buses.classList.add("item")
 
     fuel_buses.classList.remove("item")
     fuel_buses.classList.add("item-active")

     
   }

  else if ("liquid-fuel-buses" == id.toString())
  {
    console.log("fuel bus")
   
    $("#Content_switch_screen").load("Fuel");

    fuel_buses.classList.remove("item-active")
    fuel_buses.classList.add("item")

    elect_buses.classList.remove("item")
    elect_buses.classList.add("item-active")
    

    
  }


});



function show_list_bus() {
    
  var courses = document.getElementById("buses_id");
  
            
            if (courses.style.display == "block") {
                courses.style.display = "none";
            } else {
                courses.style.display = "block";
            }
        }

        window.onclick = function (event) {
            if (!event.target.matches('#dropdown_button')) {
                document.getElementById('buses_id').style.display = "none";
            }
  }  

   


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






console.log("Reached the dashboard end")