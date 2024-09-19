function showComparison() {
    const url1 = document.getElementById('url1').value;
    const url2 = document.getElementById('url2').value;

    if (url1 && url2) {
        fetch('http://127.0.0.1:5000/compare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url1: url1, url2: url2 })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('API Response:', data);

            const price1 = data.url1_price !== null && data.url1_price !== undefined ? data.url1_price : 'Unavailable';
            const price2 = data.url2_price !== null && data.url2_price !== undefined ? data.url2_price : 'Unavailable';

            const domain1 = data.domain1;
            const domain2 = data.domain2;

            const productDetails = document.getElementById('productDetails');
            productDetails.innerHTML = `
                <div class="product-info">
                    <h5 class="domain">${domain1}</h5>
                    <p class="price">Price: ₹${price1}</p>
                </div>
                <div class="product-info">
                    <h5 class="domain">${domain2}</h5>
                    <p class="price">Price: ₹${price2}</p>
                </div>
            `;

            // Optional: Add some transition or animation for smoother display
            productDetails.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            const productDetails = document.getElementById('productDetails');
            productDetails.innerHTML = `<div>Error: ${error.message}</div>`;
        });
    } else {
        alert("Please enter both URLs!");
    }
}

