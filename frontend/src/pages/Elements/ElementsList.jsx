import React, { useEffect, useState } from "react";
import api from "../../services/api";
import { Link } from "react-router-dom";

function ElementsList({ boardId }) {
    const [elements, setElements] = useState([]);
    const [nextUrl, setNextUrl] = useState(null);
    const [prevUrl, setPrevUrl] = useState(null);
    const [error, setError] = useState("");

    const fetchElements = async (url) => {
        try {
            const response = await api.get(url);
            setElements(response.data.results);
            setNextUrl(response.data.next);
            setPrevUrl(response.data.previous);
        } catch (error) {
            console.error("Error fetching elements:", error);
            setError("Failed to load elements.");
        }
    };

    useEffect(() => {
        const initialUrl = `/boards/elements_list/${boardId}`;
        fetchElements(initialUrl);
    }, [boardId]);

    return (
        <div style={{margin: "2px 2px 40px 2px"}}>
            <h2>Elements for Board {boardId}</h2>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <ul>
                {elements.map((element, index) => (
                    <li key={index}>
                        <Link to={`/element/${element.pk}`}>{element.name}</Link> <br />
                        {element.description || "No description"}
                        {element.due_date && <p>Due Date: {element.due_date}</p>}
                    </li>
                ))}
            </ul>
            <div>
                <button 
                    onClick={() => fetchElements(prevUrl)} 
                    disabled={!prevUrl}
                >
                    Previous
                </button>
                <button 
                    onClick={() => fetchElements(nextUrl)} 
                    disabled={!nextUrl}
                >
                    Next
                </button>
            </div>
        </div>
    );
}

export default ElementsList