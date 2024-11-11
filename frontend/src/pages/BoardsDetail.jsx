import { useNavigate, useParams } from "react-router-dom";
import api from "../services/api";
import { useState, useEffect } from "react";

function BoardsDetail() {
    const { pk } = useParams()
    const [board, setBoard] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const navigate = useNavigate()

    useEffect(() => {
        const fetchBoardDetail = async () => {
            try {
                const response = await api.get(`/boards/boards/${pk}`);
                setBoard(response.data);
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
                    <p>Description: {board.description || "No description provided"}</p>
                    <p>Status: {board.status === 0 ? "Ongoing" : "Done"}</p>
                    <p>Creator: {board.creator?.username || "Unknown"}</p>
                </div>
            ) : (
                <p>No board data available</p>
            )}
        </div>
    );
}

export default BoardsDetail;