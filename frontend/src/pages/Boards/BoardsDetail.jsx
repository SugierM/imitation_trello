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
    const navigate = useNavigate()

    useEffect(() => {
        const fetchBoardDetail = async () => {
            try {
                const response = await api.get(`/boards/boards/${pk}`);
                setBoard(response.data);
                setCreator(response.data.creator)
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
                    <h2>{board.name}</h2>
                    {console.log(board)}
                    <p>Description: {board.description || "No description provided"}</p>
                    <p>Status: {board.status === 0 ? "Ongoing" : "Done"}</p>
                    <p>Creator: {creator.nickname || creator.first_name + " " + creator.last_name ||"Unknown"}</p>
                    <p>Earliest to end element: {board.first_to_end_name || "None"}</p>
                    <p>Ends in: {board.first_to_end_date || "YYYY-MM-DD"}</p>
                    <p>Total number of elements: {board.total_elements || "0"}</p>
                    <p>Number of completed elements: {board.completed_elements || "0"}</p>
                </div>
            ) : (
                <p>No board data available</p>
            )}
            <ElementsList boardId={pk}></ElementsList>
        </div>
    );
}

export default BoardsDetail;