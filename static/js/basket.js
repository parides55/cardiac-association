// Constants
const removalModal = new bootstrap.Modal(document.getElementById("removalModal"));
const removeButtons = document.getElementsByClassName("btn-to-remove-item");
const removeConfirm = document.getElementById("removeConfirm");

// Gets the item's id to be removed from the basket and initiates the removal modal
if (removalModal && removeConfirm) {
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('btn-to-remove-item')) {
            e.preventDefault();
            let itemId = e.target.getAttribute('data-basket_id');
            removeConfirm.href = `remove_from_basket/${itemId}`;
            removalModal.show();
            removeConfirm.focus();
        }
    });
}
