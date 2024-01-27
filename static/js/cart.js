var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var product_id = this.dataset.product
        var action = this.dataset.action
        console.log('product_id:', product_id, 'action:', action)

        console.log('USER', user)
        if (user === 'AnonymousUser') {
            console.log('No logged in')
        } else {
            updateUserOrder(product_id, action)
        }
    })
}

function updateUserOrder(product_id, action) {
    var url = '/update_item/'
    console.log('URL:', url)
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'product_id': product_id, 'action': action})
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            location.reload()
        });
}