import { useState, useEffect } from "react"
import api from "../../services/api"
import { useParams } from "react-router-dom"

function TasksDetails() {
    const {pk} = useParams()
    const [task, setTask] =  useState({
        element: null,
        name: null,
        description: null,
        due_date: null,
        priority: null,
        status: null,
        labels: null,
    })
        

        useEffect(() => {
            const fetchTask = async () => {
                try {
                    const response = await api.get(`boards/tasks/${pk}/`);
                    setTask(response.data);

                } catch (error) {
                    if (error.response && error.response.status === 403) {
                        navigate("/not_auth");
                    } else {
                        alert("Failed to load task details");
                    }
                }
            };
    
            fetchTask();
        }, [pk]);

    return (
        <div>
            <p>{task.name}</p>
            <p>{task.description || "No description"}</p>
        </div>
    )
}

export default TasksDetails