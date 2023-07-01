function Click (str) {
    if (document.getElementById(str).classList.contains('selected')){
        // document.getElementById(str).classList.remove('selected');
    }
    else{
        document.getElementById(str).classList.add("selected")
        var products = document.getElementsByClassName('product');
        var selectedElements = document.querySelectorAll('.selected');
        var selectedElementIds = Array.from(selectedElements).map(function(element) {
            return element.id;
        });
        for (var i = 0; i < products.length; i ++) {
            products[i].style.display = 'none';
        }
        var p = document.getElementsByClassName(str);
        for (var i = 0; i < p.length; i ++) {
            p[i].style.display = 'block';
        }

        for (var i = 0; i < selectedElementIds.length; i ++) {
            console.log(selectedElementIds[i])
            var c = document.getElementsByClassName(selectedElementIds[i]);
            for (var j = 0; j < c.length; j ++) {
                c[j].style.display = 'block'
            }
        }
    }
}
function AddToChart(){
    document.getElementById("cart").style.display = 'inline';
}

function AddProduct(){
        document.getElementById('success').style.display= 'inline'
}
