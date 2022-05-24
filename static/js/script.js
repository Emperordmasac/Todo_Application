/*!
 * TODOLISTS
 */
// CREATE A LIST OF TASKS
document.getElementById("list__form").onsubmit = function (e) {
    e.preventDefault();

    fetch("/lists/create", {
        method: "POST",
        body: JSON.stringify({
            name: document.getElementById("list__input").value,
        }),
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonResponse) {
            const liItem = document.createElement("LI");

            liItem.innerHTML = jsonResponse["name"];
            document.getElementById("lists").appendChild(liItem);
            window.location.reload(true);
        })
        .catch(function (err) {
            console.log(err);
        });
};

// DELETE TASKS
const delete_lists = document.querySelectorAll(".delete__list");
for (let i = 0; i < delete_lists.length; i++) {
    const delete_list = delete_lists[i];

    delete_list.onclick = function (e) {
        const list_id = e.target.dataset.id;

        fetch("/lists/" + list_id + "/delete", {
            method: "DELETE",
        })
            .then(function () {
                const element = e.target.parentElement;

                element.remove();
                window.location.reload(true);
            })
            .catch(function (err) {
                console.log(err);
            });
    };
}

// MARK TASKS
const listCheckboxes = document.querySelectorAll(".list__check");
for (let i = 0; i < listCheckboxes.length; i++) {
    const checkbox = listCheckboxes[i];

    checkbox.onchange = function (e) {
        if (e.target.checked) {
            const list_id = e.target.dataset.id;

            fetch("/lists/" + list_id + "/checked", {
                method: "POST",
            })
                .then(function () {
                    window.location.reload(true);
                })
                .catch(function (err) {
                    console.log(err);
                });
        }
    };
}

/*!
 * TODOS
 */

// CREATE A TODO
document.getElementById("todo__form").onsubmit = function (e) {
    e.preventDefault();

    fetch("/todos/create", {
        method: "POST",
        body: JSON.stringify({
            description: document.getElementById("description").value,
            list_id: document.getElementById("list_id").value,
        }),
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonResponse) {
            const liItem = document.createElement("LI");

            liItem.innerHTML = jsonResponse["description"];
            document.getElementById("todos").appendChild(liItem);
            window.location.reload(true);
        })
        .catch(function (err) {
            console.log(err);
        });
};

// DELETE A TODO
const delete_todos = document.querySelectorAll(".delete__todo");
for (let i = 0; i < delete_todos.length; i++) {
    const delete_todo = delete_todos[i];

    delete_todo.onclick = function (e) {
        const todo_id = e.target.dataset.id;

        fetch("/todos/" + todo_id + "/delete", {
            method: "DELETE",
        })
            .then(function () {
                const element = e.target.parentElement;

                element.remove();
                window.location.reload(true);
            })
            .catch(function (err) {
                console.log(err);
            });
    };
}

// MARK A TODO
const todocheckboxes = document.querySelectorAll(".todo__check");
for (let i = 0; i < todocheckboxes.length; i++) {
    const checkbox = todocheckboxes[i];

    checkbox.onchange = function (e) {
        const value = e.target.checked;
        const todo__id = e.target.dataset.id;

        fetch("/todos/" + todo__id + "/checked", {
            method: "POST",
            body: JSON.stringify({
                completed: value,
            }),
            headers: {
                "Content-type": "application/json",
            },
        }).catch(function (err) {
            console.log(err);
        });
    };
}
