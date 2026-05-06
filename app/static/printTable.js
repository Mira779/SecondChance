function printTable() {
    let tableContent = document.getElementById('myTable').outerHTML;
    let original = document.body.innerHTML;
    document.body.innerHTML = tableContent;
    window.print();
    document.body.innerHTML = original;
}
