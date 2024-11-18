import api from "../../services/api"
import { useState, useEffect } from "react"
import { useParams } from "react-router-dom"


function ElementDetail() {
    const {pk} = useParams()
    const [element, setElement] =  useState({
        board: null,
        name: null,
        description: null,
        due_date: null,
        order: null,
        status: null})

        useEffect(() => {
            const fetchElement = async () => {
                try {
                    const response = await api.get(`boards/elements/${pk}/`);
                    setElement(response.data);
                } catch (error) {
                    if (error.response && error.response.status === 403) {
                        navigate("/not_auth");
                    } else {
                        alert("Failed to load element details");
                    }
                }
            };
    
            fetchElement();
        }, [pk]);

    return (
        <div>
            <p>{element.name}</p>
            <p>{element.description || "No description"}</p>
        </div>
    )
}

export default ElementDetail