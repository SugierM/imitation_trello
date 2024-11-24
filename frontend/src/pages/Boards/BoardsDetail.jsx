import { useNavigate, useParams } from "react-router-dom";
import api from "../../services/api";
import { useState, useEffect } from "react";
import ElementsList from "../Elements/ElementsList";

function BoardsDetail() {
    const { pk } = useParams()
    const [board, setBoard] = useState({})
    const [creator, setCreator] = useState({})
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [firstElement, setFirstElement] = useState({
        name: "",
        due_date: "",
        pk: ""
    })
    const navigate = useNavigate()

    useEffect(() => {
        const fetchBoardDetail = async () => {
            try {
                const response = await api.get(`/boards/boards/${pk}`);
                setBoard(response.data);
                setCreator(response.data.creator)
                if (response.data.first_element != null){
                    setFirstElement(response.data.first_element)
                }
                setLoading(false); 
            } catch (error) {
                if (error.status === 403) {
                    navigate("/not_auth")
                }
                console.error("Error fetching board details:", error);
                setError("Failed to load board details");
                setLoading(false);
            }
        };

        fetchBoardDetail();
    }, [pk]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div>
            <h1>Board Details</h1>
            {board ? (
                <div>
                    <h2>{board.name || "Board - Name"}</h2>
                    <p>Description: {board.description || "No description provided"}</p>
                    <p>Status: {board.status === 0 ? "Ongoing" : "Done"}</p>
                    <p>Creator: {creator.nickname || creator.first_name + " " + creator.last_name ||"Unknown"}</p>
                    <p>Earliest to end element: {firstElement.name || "None"}</p>
                    <p>Ends in: {firstElement.due_date || "YYYY-MM-DD"}</p>
                    <p>Total number of elements: {board.total_elements || "0"}</p>
                    <p>Number of completed elements: {board.completed_elements || "0"}</p>
                </div>
            ) : (
                <p>No board data available</p>
            )}
            <h2>Elements for Board {board.name}</h2>
            <ElementsList boardId={pk}></ElementsList>
        </div>
    );
}

export default BoardsDetail;