for (var i = 1; i < product.length; i++) {
    document.getElementById("select1").innerHTML += `
    <option value="${i}">${product[i].title}</option>
    `;
    document.getElementById("select2").innerHTML += `
    <option value="${i}">${product[i].title}</option>
    `;
}

function item1(a) {
    var select2 = document.getElementById("select2").value;
    if (a != select2) {
        document.getElementById("img1").src = product[a].image
        document.getElementById("price1").innerHTML = "INR " + product[a].price
        document.getElementById("desc1").innerHTML = product[a].description
        document.getElementById("brand1").innerHTML = product[a].brand

    } else {
        document.getElementById("select1").selectedIndex = 0;
        document.getElementById("img1").src = product[0].image
        document.getElementById("price1").innerHTML = ""
        document.getElementById("desc1").innerHTML = ""
        document.getElementById("brand1").innerHTML = ""

    }
}

function item2(a) {
    var select1 = document.getElementById("select1").value;
    if (a != select1) {
        document.getElementById("img2").src = product[a].image
        document.getElementById("price2").innerHTML = "INR " + product[a].price
        document.getElementById("desc2").innerHTML = product[a].description
        document.getElementById("brand2").innerHTML = product[a].brand
    } else {
        document.getElementById("select2").selectedIndex = 0;
        document.getElementById("img2").src = product[0].image
        document.getElementById("price2").innerHTML = ""
        document.getElementById("desc2").innerHTML = ''
        document.getElementById("brand2").innerHTML = ""

    }
}
function showComparison() {
    // Get selected values
    const select1Value = document.getElementById('select1').value;
    const select2Value = document.getElementById('select2').value;

    // Get selected products
    const product1 = product.find(p => p.id == select1Value);
    const product2 = product.find(p => p.id == select2Value);

    // Get the container where product details will be displayed
    const detailsContainer = document.getElementById('productDetails');

    // Clear previous details
    detailsContainer.innerHTML = '';

    // Create HTML for product details
    if (product1) {
        detailsContainer.innerHTML += `
            <div>
                <h4>${product1.title}</h4>
                <img src="${product1.image}" alt="${product1.title}">
                <p><strong>Price:</strong> INR ${product1.price}</p>
                <p><strong>Description:</strong> ${product1.description}</p>
                <p><strong>Brand:</strong> ${product1.brand}</p>
            </div>
        `;
    }

    if (product2) {
        detailsContainer.innerHTML += `
            <div>
                <h4>${product2.title}</h4>
                <img src="${product2.image}" alt="${product2.title}">
                <p><strong>Price:</strong> INR ${product2.price}</p>
                <p><strong>Description:</strong> ${product2.description}</p>
                <p><strong>Brand:</strong> ${product2.brand}</p>
            </div>
        `;
    }
}