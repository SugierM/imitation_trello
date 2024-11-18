import api from "../../services/api"
import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"

function BoardCreate() {
    const [name, setName] = useState("")
    const [description, setDescription] = useState("")
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault();


        try {
            const response = await  api.post("/boards/boards_create/", {
                name: name,
                description: description,
            });
            navigate("/boards")
        } catch (error) {
            const errorMessages = Object.entries(error.response.data)
                .map(([field, messages]) => `${field}: ${messages}`)
                .join("\n");
            alert(errorMessages)
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <span><b>Name</b></span>
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Board name"
                />
                <br />
                <span><b>Description</b></span>
                <input
                    type="text"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
                <br />
                <button type="submit">Create</button>
            </form>
        </div>
    );
}

export default BoardCreate