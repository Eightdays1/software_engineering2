setTimeout(function () {
    $('.alert').alert('close');
}, 4000);
function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId}),
    }).then((_res) => {
        window.location.href = "/";
    });
}

function deleteItem(item_id) {
    fetch('/delete-item', {
        method: 'POST',
        body: JSON.stringify({ item_id: item_id}),
    }).then((_res) => {
        window.location.href = "/list";
    });
}

function toggleItemState(item_id) {
    fetch('/toggle-item', {
        method: 'POST',
        body: JSON.stringify({ item_id: item_id}),
    }).then((_res) => {
        window.location.href = "/list";
    });
}

function editGroupName() {
  document.getElementById("group-name").removeAttribute('disabled');
  document.getElementById("group-name").removeAttribute('readonly');
}

document.getElementById("edit-button").addEventListener("click", editGroupName);
