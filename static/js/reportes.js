document.getElementById('reporte-diario').addEventListener('click', reporteDiario);
document.getElementById('reporte-semanal').addEventListener('click', reporteSemanal);
document.getElementById('reporte-mensual').addEventListener('click', reporteMensual);



function reporteDiario() {
    data = document.getElementById('date').value;
    if (data != "") {
        window.open("diario/" + data)
    }
}


function reporteSemanal() {
    data = document.getElementById('week').value;
    if (data != "") {
        console.log(data);
    }
}


function reporteMensual() {
    data = document.getElementById('month').value;
    if (data != "") {
        console.log(data);
    }
}