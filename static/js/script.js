function checkLogin() {
    alert("You must be logged in to view the cart.");
}


$(".addtocart").click(function() {
    Swal.fire({
        position: 'top-end',
        icon: 'success',
        title: 'Items is already in the cart',
        showConfirmButton: false,
        timer: 1000
      })
});