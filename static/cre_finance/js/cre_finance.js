let costForm = document.querySelectorAll(".cost-form");
let container = document.querySelector("#form-container");
let addButton = document.querySelector("#add-form");
let totalForms = document.querySelector("#id_form-TOTAL_FORMS");
let formNum = costForm.length-1;

function addForm(e) {
        e.preventDefault()

        let newForm = costForm[0].cloneNode(true)
        let formRegex = RegExp(`form-(\\d){1}-`,'g') //Regex to find all instances of the form number

        formNum++
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`) //Update the new form to have the correct form number
        container.insertBefore(newForm, addButton) //Insert the new form at the end of the list of forms

        totalForms.setAttribute('value', `${formNum+1}`) //Increment the number of total forms in the management form

        console.log("formNum:", formNum)
        console.log("totalForms:", totalForms)

};

if (addButton) {
  addButton.addEventListener('click', addForm);
};



// < ==== JS toggle class

// window.onload = function(){
//   var hideElements = document.querySelectorAll("th");
//   console.log("onload");
//   console.log(hideElements);
// }

// window.addEventListener('DOMContentLoaded', (event) => {
//   var hideElements = document.querySelectorAll("th");
//   console.log("onload");
//   console.log(hideElements);
// })


function toggleHide(){
  var hideElements = document.querySelectorAll(".coordinates");
  var toggleCoordinates = document.getElementById('toggleCoordinates');

hideElements.forEach((el) => {
    const elemHidden = el.classList.toggle('hide');
    if(elemHidden) {
      toggleCoordinates.innerHTML = "Show Coordinates"
    } else {
      toggleCoordinates.innerHTML = "Hide Coordinates"
    }
  });
  }
