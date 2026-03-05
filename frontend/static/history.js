let history = JSON.parse(localStorage.getItem("foodHistory")) || [];

let tableBody = document.getElementById("historyTable");

history.forEach((item, index) => {

    let row = document.createElement("tr");

    row.innerHTML = `
        <td>${item.food}</td>
        <td>${item.result}</td>
        <td>
            <button onclick="deleteItem(${index})" class="delete-btn">Delete</button>
        </td>
    `;

    tableBody.appendChild(row);

});

function deleteItem(index){
    history.splice(index, 1); // remove item
    localStorage.setItem("foodHistory", JSON.stringify(history)); // update storage
    location.reload(); // refresh table
}

function clearHistory(){
    localStorage.removeItem("foodHistory");
    location.reload();
}