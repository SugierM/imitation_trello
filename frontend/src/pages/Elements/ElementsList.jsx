import React, { useEffect, useState } from "react";
import api from "../../services/api";
import fetchList from "../../services/helpFunctions";
import { Link } from "react-router-dom";

function ElementsList({ boardId }) {
    const [elements, setElements] = useState([]);
    const [nextUrl, setNextUrl] = useState(null);
    const [prevUrl, setPrevUrl] = useState(null);
    const [error, setError] = useState("");

    const fetchElements = (url) => {
        fetchList(
            url,
            setElements,
            setNextUrl,
            setPrevUrl,
            "elements"
        )
    }

    useEffect(() => {
        const initialUrl = `/boards/elements_list/${boardId}`;
        fetchElements(initialUrl);
    }, [boardId]);

    return (
        <div style={{margin: "2px 2px 40px 2px"}}>
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
            {(prevUrl || nextUrl) && (
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
            )}
            
                    
            </div>
        </div>
    );
}

export default ElementsList