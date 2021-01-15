function checkPassword() {
  if (document.getElementById("password").value != document.getElementById("password-repeat").value) {
    document.getElementById("addjudge").disabled = true;
    document.getElementById("passwordnomatch").style.visibility = "visible";
  } else {
    document.getElementById("addjudge").disabled = false;
    document.getElementById("passwordnomatch").style.visibility = "hidden";
  }
}

function addTeam() {
  var form = document.getElementById("newjudge");
  var label = document.createElement('label');
  var input = document.createElement('input');
  var listitems = form.getElementsByClassName("teaminput");

  input.type = "text";
  input.id = "team" + (listitems.length + 1);
  input.name = "team" + (listitems.length + 1);
  input.placeholder = "Team name";
  input.className = "teaminput";

  label.for = "team" + (listitems.length + 1) + ": ";
  label.innerHTML = "Team " + (listitems.length + 1) + ": ";

  var spacer = document.getElementById("spacer");

  form.insertBefore(label, spacer);
  form.insertBefore(input, spacer);
  form.insertBefore(document.createElement('br'), spacer);
}
