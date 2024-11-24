import React, { useEffect, useState } from "react";
import api from "../../services/api";
import fetchList from "../../services/helpFunctions";
import { Link } from "react-router-dom";

function TasksList({ elementId }) {
    const [tasks, setTasks] = useState([]);
    const [nextUrl, setNextUrl] = useState(null);
    const [prevUrl, setPrevUrl] = useState(null);
    const [error, setError] = useState("");

    const fetchTasks = (url) => {
        fetchList(
            url,
            setTasks,
            setNextUrl,
            setPrevUrl,
            "tasks"
        )
    }

    useEffect(() => {
        const initialUrl = `/boards/tasks_list/${elementId}/`;
        fetchTasks(initialUrl);
    }, [elementId]);

    return (
        <div style={{margin: "2px 2px 40px 2px"}}>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <ul>
                {tasks.map((task, index) => (
                    <li key={index}>
                        <Link to={`/task/${task.pk}`}>{task.name}</Link> <br />
                        {task.description || "No description"}
                        {task.due_date && <p>Due Date: {task.due_date}</p>}
                    </li>
                ))}
            </ul>
            <div>
            {(prevUrl || nextUrl) && (
                <div>
                    <button 
                        onClick={() => fetchTasks(prevUrl)} 
                        disabled={!prevUrl}
                    >
                        Previous
                    </button>
                    <button 
                        onClick={() => fetchTasks(nextUrl)} 
                        disabled={!nextUrl}
                    >
                        Next
                    </button>
                </div>
            )}
            
                    
            </div>
        </div>
    );
}

export default TasksList