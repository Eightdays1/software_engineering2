setTimeout(function () {
    $('.alert').alert('close');
}, 4000);

function deleteNote(id) {
    fetch('/api/delete-note', {
        method: 'POST',
        body: JSON.stringify({ note_id: id}),
    }).then((_res) => {
        window.location.href = "/";
    });
}

function deleteItem(id) {
    fetch('/api/delete-item', {
        method: 'POST',
        body: JSON.stringify({ item_id: id}),
    }).then((_res) => {
        window.location.href = "/list";
    });
}

function deleteUser(id){
    fetch('/api/delete-user', {
        method: 'POST',
        body: JSON.stringify({ user_id: id}),
    }).then((_res) => {
        window.location.href = "/login";
    });
}

function deleteTask(id){
    fetch('/api/delete-task', {
        method: 'POST',
        body: JSON.stringify({ task_id: id}),
    }).then((_res) => {
        window.location.href = "/tasks";
    });
}

function toggleItemState(id) {
    fetch('/api/toggle-item', {
        method: 'POST',
        body: JSON.stringify({ item_id: id}),
    }).then((_res) => {
        window.location.href = "/list";
    });
}

function toggleTaskState(id) {
    fetch('/api/toggle-task', {
        method: 'POST',
        body: JSON.stringify({ task_id: id}),
    }).then((_res) => {
        window.location.href = "/tasks";
    });
}

function leaveGroup(id) {
    fetch('/api/leave-group', {
        method: 'POST',
        body: JSON.stringify({ group_id: id}),
    }).then((_res) => {
        window.location.href = "/household";
    });
}

function editGroupName() {
  document.getElementById("group-name").removeAttribute('disabled');
  document.getElementById("group-name").removeAttribute('readonly');
  document.getElementById("group-name").focus();
}

function addGroupName() {
  document.getElementById("new-group-name").focus();

}

function editEmail() {
  document.getElementById("email_address").removeAttribute('disabled');
  document.getElementById("email_address").focus();
}

function editName() {
  document.getElementById("first_name").removeAttribute('disabled');
  document.getElementById("first_name").focus();
}

function submit_addEvent() {
  document.getElementById('addEventForm').submit();
}

function submit_addTask() {
  document.getElementById('addTaskForm').submit();
}

function submit_addTaskDynamic(id) {
    console.log(id)
  var element = 'addTaskForm_' + String(id)
  console.log(String(element))
  document.getElementById(String(element)).submit();
}

function removeDisabledRepeatTill() {
    var value = document.getElementById('repeat_input').value
    if (value > 0){
        document.getElementById('repeat-till_input').removeAttribute('disabled');
    } else {
        document.getElementById('repeat-till_input').setAttribute('disabled', 'true');
    }
}