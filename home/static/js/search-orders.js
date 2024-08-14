



const searchField = document.querySelector( "#search-orders");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector("#app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");
const editBaseUrl = document.getElementById('ordersTable').dataset.editUrl;


searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    tbody.innerHTML = "";
    fetch("/search-orders/", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        appTable.style.display = "none";
        appTable.classList.remove("table-responsive");
        tableOutput.style.display = "block";

        console.log("data.length", data.length);

        if (data.length === 0) {
          noResults.style.display = "block";
          tableOutput.style.display = "none";
        } else {
          noResults.style.display = "none";
          
          data.forEach((item) => {
            // Removed forward slash
            const editUrl = `${editBaseUrl}${item.id}`;

            tbody.innerHTML += `
            <tr>
              <td class="cell">${item.id}</td>
              <td class="cell"><span class="truncate">${item.name}</span></td>
              <td class="cell">${item.contact}</td>
              <td class="cell"><span>${item.location}</span><span class="note">(description)</span></td>
              <td class="cell">${item.quantity}Pcs</td>
              <td class="cell"><span>${item.date_ordered}</span><span class="note">${item.date_due}</span></td>
              <td class="cell"><span class="badge bg-${getStatusColor(item.status)}">${item.status}</span></td>
              <td class="cell"><span>${item.amount}</span><span class="note">${item.pay_form}</span></td>
              <td class="cell"><a class="btn-sm app-btn-secondary" href="${editUrl}">View</a></td>
            </tr>
          `;
          });
          function getStatusColor(status) {
            switch (status) {
              case 'Pending':
                return 'warning';
              case 'Settled':
                return 'success';
              case 'RollOver':
                return 'danger';
              default:
                return 'default';
            }
          }
        }
      });
    } else {
        window.location.href = "/orders/";
        
     }
});


/* ====

appTable.style.display = "block";
        appTable.style.width = "100%";
        tableOutput.style.display = "none";
        
        noResults.style.display = "none";
        paginationContainer.style.display = "block";

tbody.innerHTML += `
                <tr>
                <td>${item.id}</td>
                <td>${item.name}</td>
                <td>${item.contact}</td>
                <td>${item.location}</td>
                <td>${item.quantity}</td>
                <td>${item.date_ordered}</td>     
                <td>${item.status}</td>
                <td>${item.amount}</td>
                </tr>`; ====== */




