// Constants
const removalModal = new bootstrap.Modal(document.getElementById("removalModal"));
const removeButtons = document.getElementsByClassName("btn-to-remove-item");
const removeConfirm = document.getElementById("removeConfirm");

// Gets the item's id to be removed from the basket and initiates the removal modal
for (let button of removeButtons) {
    button.addEventListener('click', (e) => {
        let itemId = e.target.getAttribute('data-basket_id');
        removeConfirm.href = `remove_from_basket/${itemId}`;
        removalModal.show();
    });
    
}