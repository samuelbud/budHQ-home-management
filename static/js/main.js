    function taskDone(taskId, checkbox) {
      const row = checkbox.closest("tr");
      const table = row.parentNode;

      if (checkbox.checked) {
        const tasksDoneTable = document.getElementById("tasks-done");
        tasksDoneTable.appendChild(row);
      } else {
        const firstRow = table.rows[0];
        table.insertBefore(row, firstRow);
      }

      fetch(`/update/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                done: checkbox.checked
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('There was an error updating the task');
            }
        })
        .catch(error => {
            console.error(error);
            alert(error.message);
            checkbox.checked = !checkbox.checked;
        });
    }
