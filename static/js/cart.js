var cartBtns = document.getElementsByClassName('update-cart');

for(var i=0;i<cartBtns.length;i++){
    cartBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId: ',productId,'action: ',action);
        if(user == 'AnonymousUser'){
            addCookieItem(productId,action);
        }else{
            console.log('User is logged in')
            console.log('USER',user);
            updateUserOrder(productId,action);
        }
    })
}
function addCookieItem(productId,action){
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] = cart[productId]['quantity'] + 1;
        }
    }
    if(action == 'remove'){
        cart[productId]['quantity'] = cart[productId]['quantity'] - 1;
        if(cart[productId]['quantity'] <= 0 ){
            delete cart[productId];
        }
    }
    console.log('Cart',cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/';
    location.reload();
}


function updateUserOrder(productId,action){
    console.log('User is logged in.Sending data ...');
    var url = '/update_item/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })
    .then(response => response.json())
    .then(data =>{
        console.log('data:',data);
        location.reload();
    });
}