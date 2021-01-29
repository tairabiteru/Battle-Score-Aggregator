function downloadCSV(csv, filename) {
  var csvFile = new Blob([csv], {type: "text/csv"});
}

function export_as_csv(judge) {
  var csv = [];
  var rows = document.getElementById(judge + "_table").rows;

  for (i=0; i<rows.length; i++) {
    var row = [];
    var cols = rows[i].querySelectorAll("td, th");

    for (j=0; j<cols.length; j++) {
      row.push(cols[j].innerText);
    }
    csv.push(row.join(","));
  }
  return csv.join("\n");
}

var totals_button = document.getElementById("download");
totals_button.download = "BSA-totals-table.html";
totals_button.href = "data:text/html," + document.getElementById("content").innerHTML;


document.addEventListener("DOMContentLoaded", function() {
  var judges = document.getElementsByClassName("judgeLink");
  for (judge of judges) {
    var csvFile = new Blob([export_as_csv(judge.id)], {type: "text/csv"});
    console.log(judge);
    judge.download = judge.id + " Score Table.csv";
    judge.href = window.URL.createObjectURL(csvFile);
  };
});
